import { hash, bytesHash, insist, decimalMicroUSD, costMicroUSD } from './canonical.mjs';
import { CONTRACT_VERSION, ADAPTER_VERSION, validateBudgetRecord, validatePrice, validateEnvelope, invocationHashes } from './contracts.mjs';
import { Journal } from './ledger.mjs';

/** No external fetch is available to this adapter. Caller passes an explicitly mock-only provider. */
export class MockProvider {
  constructor({mode='success',reported_revision='revision-pinned-001',endpoint='mock-endpoint-01',usage={input_tokens:100,output_tokens:20},response='mock response',stream_completed=true,response_truncated=false}={}){
    this.mode=mode;this.reported_revision=reported_revision;this.endpoint=endpoint;this.usage=usage;
    this.response=response;this.stream_completed=stream_completed;this.response_truncated=response_truncated;this.calls=0;this.seen=new Map();this.preparations=0;
  }
  async prepare(){this.preparations++;return {can_dispatch:this.mode!=='preflight_denied',non_dispatch_proven:this.mode==='preflight_denied'};}
  async invoke(e){this.calls++;
    if(this.mode==='error_after_dispatch'){this.seen.set(e.idempotency_key,{status:'ambiguous'});throw Error('MOCK_TRANSPORT_TIMEOUT_AFTER_DISPATCH');}
    if(this.mode==='failure_reported'){this.seen.set(e.idempotency_key,{status:'failed_billing_unknown'});return {error:'MOCK_PROVIDER_ERROR'};}
    this.seen.set(e.idempotency_key,{status:'completed'});
    return {provider_request_id:'mock-req-'+e.invocation_id,model_revision_reported:this.reported_revision,endpoint_id:this.endpoint,usage:this.mode==='missing_usage'?undefined:this.usage,bytes:Buffer.from(this.response,'utf8'),stream_completed:this.stream_completed,response_truncated:this.response_truncated,price_schedule_sha256:this.mode==='price_changed'?hash({changed:true}):e.price_schedule_sha256};
  }
  async queryIdempotency(key) { return {provider:'MOCK_ONLY',idempotency_key:key,status:this.seen.get(key)?.status??'NOT_FOUND',authoritative_mock:true}; }
}
export class Breaker {
  constructor({threshold=3,window_ms=60000,open_ms=30000,reset='automatic',clock=()=>Date.now()}={}){
    insist(['automatic','manual'].includes(reset),'BREAKER_RESET_POLICY');
    this.threshold=threshold;this.window_ms=window_ms;this.open_ms=open_ms;this.reset=reset;this.clock=clock;this.failures=[];this.opened_at=null;this.halfOpenInFlight=false;
  }
  allow(){const now=this.clock();if(this.opened_at!==null){
    if(this.reset==='manual'||now-this.opened_at<this.open_ms)throw Error('CIRCUIT_OPEN');
    if(this.halfOpenInFlight)throw Error('CIRCUIT_HALF_OPEN_BUSY');
    this.halfOpenInFlight=true;return;
  }}
  success(){this.failures=[];this.opened_at=null;this.halfOpenInFlight=false;}
  failure(){const now=this.clock();if(this.halfOpenInFlight){this.opened_at=now;this.halfOpenInFlight=false;return;}
    this.failures=this.failures.filter(t=>now-t<this.window_ms);this.failures.push(now);
    if(this.failures.length>=this.threshold)this.opened_at=now;
  }
  manualReset(){insist(this.reset==='manual','BREAKER_NOT_MANUAL');this.success();}
}
export class MockAdapter {
  constructor({dir, budget, price, authenticatedCaller, provider, clock=()=>new Date().toISOString(),breaker}={}){
    validateBudgetRecord(budget);validatePrice(price);
    insist(provider instanceof MockProvider,'REAL_PROVIDER_FORBIDDEN_IN_MOCK_ADAPTER');
    insist(authenticatedCaller===budget.owner,'AUTH_OWNER_MISMATCH');
    this.journal=new Journal({dir,budget,clock});this.budget=structuredClone(budget);this.price=structuredClone(price);
    this.authenticatedCaller=authenticatedCaller;this.provider=provider;this.clock=clock;this.breaker=breaker??new Breaker();
  }
  close(){this.journal.close();}
  async call(envelope,{system_prompt,user_prompt,tool_schemas=[],tool_allowlist=[],parameters={}}){
    const now=this.clock();
    validateEnvelope(envelope,{budget:this.budget,price:this.price,authenticatedCaller:this.authenticatedCaller,nowISO:now});
    const actualHashes=invocationHashes({system_prompt,user_prompt,tool_schemas,tool_allowlist,parameters});
    for(const [field,value]of Object.entries(actualHashes))insist(envelope[field]===value,'PAYLOAD_HASH_MISMATCH_'+field);
    const invHash=hash({...envelope,...actualHashes});
    const previous=this.journal.getByKey(envelope.idempotency_key);
    if(previous){insist(previous.invocation_id===envelope.invocation_id&&previous.invocation_hash===invHash,'IDEMPOTENCY_CONFLICT');
      const receipts=this.journal.receipts(envelope.case_id);
      return receipts.find(x=>x.invocation_id===envelope.invocation_id)??{schema:'computerwisdom.ci-first.pending.v0.3',invocation_id:envelope.invocation_id,status:previous.state,verdict:'UNKNOWN',reenqueued:false,canon:false,authority_created:false};
    }
    this.breaker.allow();
    const inputRate=decimalMicroUSD(this.price.input_usd_per_1k),outputRate=decimalMicroUSD(this.price.output_usd_per_1k);
    const maxCost=costMicroUSD(envelope.max_input_tokens,envelope.max_output_tokens,inputRate,outputRate);
    this.journal.reserve({invocation_id:envelope.invocation_id,idempotency_key:envelope.idempotency_key,agent_id:envelope.agent_id,invocation_hash:invHash,amount:maxCost,reservation_ttl_seconds:envelope.reservation_ttl_seconds});
    const preflight=await this.provider.prepare(envelope);
    if(!preflight.can_dispatch){
      insist(preflight.non_dispatch_proven===true,'NON_DISPATCH_PROOF_MISSING');
      this.journal.add({type:'FAILED_DISPATCH',invocation_id:envelope.invocation_id,reason:'MOCK_PREFLIGHT_REJECTED'});
      this.breaker.failure();
      return this.writeReceipt(envelope,{verdict:'FAIL',cost_outcome:'FAILED_DISPATCH',response:null,revision_verification:'unverified',maxCost});
    }
    // Durable intent is required BEFORE provider calls. A failed journal append prevents dispatch.
    this.journal.add({type:'DISPATCHED',invocation_id:envelope.invocation_id});
    let result;
    try{result=await this.provider.invoke(envelope);}catch(err){
      this.journal.add({type:'UNKNOWN_COST',invocation_id:envelope.invocation_id,reason:'DISPATCH_OUTCOME_AMBIGUOUS'});
      this.breaker.failure();
      return this.writeReceipt(envelope,{verdict:'UNKNOWN',cost_outcome:'UNKNOWN_COST',response:null,revision_verification:'unverified',maxCost,error:'TRANSPORT_OUTCOME_AMBIGUOUS'});
    }
    let verification='unverified';
    if(result?.model_revision_reported!==envelope.model_revision_requested||!result?.model_revision_reported)verification='mismatch';
    const mismatch=verification==='mismatch'||result?.endpoint_id!==envelope.endpoint_id;
    const complete=result?.stream_completed===true&&result?.response_truncated===false;
    const tokensValid=Number.isSafeInteger(result?.usage?.input_tokens)&&Number.isSafeInteger(result?.usage?.output_tokens)&&result.usage.input_tokens>=0&&result.usage.output_tokens>=0&&result.usage.input_tokens<=envelope.max_input_tokens&&result.usage.output_tokens<=envelope.max_output_tokens;
    const priceLocked=result?.price_schedule_sha256===envelope.price_schedule_sha256;
    const safe=result&&!result.error&&!mismatch&&complete&&tokensValid&&priceLocked;
    let costOutcome,verdict;
    if(safe){
      const actual=costMicroUSD(result.usage.input_tokens,result.usage.output_tokens,inputRate,outputRate);
      insist(actual<=maxCost,'COST_EXCEEDS_RESERVATION');
      this.journal.add({type:'RECONCILED',invocation_id:envelope.invocation_id,charged_micro_usd:actual});
      costOutcome='RECONCILED';verdict='UNKNOWN'; // Provider self-reported revision ≠ independently verified revision.
      this.breaker.success();
    }else{
      this.journal.add({type:'RECONCILIATION_FAILED',invocation_id:envelope.invocation_id,reason:mismatch?'PROVIDER_IDENTITY_MISMATCH':!priceLocked?'PRICE_SCHEDULE_MISMATCH':!complete?'INCOMPLETE_STREAM':!tokensValid?'USAGE_MISSING_OR_OVER_CAP':'PROVIDER_ERROR'});
      costOutcome='RECONCILIATION_FAILED';verdict=mismatch?'FAIL':'UNKNOWN';
      this.breaker.failure();
    }
    return this.writeReceipt(envelope,{verdict,cost_outcome:costOutcome,response:result,revision_verification:verification,maxCost});
  }
  writeReceipt(envelope,{verdict,cost_outcome,response,revision_verification,maxCost,error=null}){
    const actualCost=this.journal.active.get(envelope.invocation_id)?.charged??0;
    const body={schema:'computerwisdom.ci-first.adapter-receipt.v0.3',contract_version:CONTRACT_VERSION,adapter_version:ADAPTER_VERSION,
      invocation_id:envelope.invocation_id,idempotency_key:envelope.idempotency_key,model_id:envelope.model_id,
      model_revision_requested:envelope.model_revision_requested,model_revision_reported:response?.model_revision_reported??null,
      model_revision_verification:revision_verification,endpoint_id_requested:envelope.endpoint_id,endpoint_id_reported:response?.endpoint_id??null,
      provider_request_id:response?.provider_request_id??null,provider_claim_scope:'MOCK_ONLY_NOT_ATTESTED',
      prompt_sha256:envelope.prompt_sha256,parameters_sha256:envelope.parameters_sha256,tool_allowlist_sha256:envelope.tool_allowlist_sha256,
      price_schedule_sha256:envelope.price_schedule_sha256,response_bytes_sha256:response?.bytes?bytesHash(response.bytes):null,
      stream_completed:response?.stream_completed===true,response_truncated:response?.response_truncated??null,
      usage_reported:response?.usage??null,reserved_micro_usd:maxCost,charged_micro_usd:actualCost,
      cost_outcome,verdict,error,canon:false,authority_created:false,payment:false,wallet_signing:false,model_api_calls:0};
    return this.journal.appendReceipt(envelope.case_id,body);
  }
  /** MOCK-ONLY absence proof, never a production release authorization. */
  async releaseExpiredUndispatched(key){
    const rec=this.journal.getByKey(key);insist(!!rec,'UNKNOWN_KEY');
    insist(['RESERVED','FAILED_DISPATCH'].includes(rec.state),'MAY_HAVE_DISPATCHED');
    const expiry=Date.parse(rec.reserved_at)+rec.ttl_seconds*1000;
    insist(Date.parse(this.clock())>=expiry,'TTL_NOT_EXPIRED');
    const query=await this.provider.queryIdempotency(key);
    insist(query.authoritative_mock===true&&query.idempotency_key===key&&query.status==='NOT_FOUND','NON_DISPATCH_NOT_PROVEN');
    this.journal.add({type:'EXPIRED_UNDISPATCHED',invocation_id:rec.invocation_id,proof:'MOCK_QUERY_NO_MATCH_CONFIRMED'});
    return {status:'EXPIRED_UNDISPATCHED',scope:'MOCK_ONLY',released_micro_usd:rec.reserved};
  }
}
