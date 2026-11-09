import { mkdirSync, openSync, closeSync, unlinkSync, readFileSync, writeSync, fsyncSync, existsSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { hash, insist, HEX64 } from './canonical.mjs';
import { STATES, validateBudgetRecord } from './contracts.mjs';
const ZERO='0'.repeat(64);
export function readJsonLines(file) {
  if (!existsSync(file)) return [];
  const content=readFileSync(file,'utf8');
  if (!content) return [];
  insist(content.endsWith('\n'),'TRUNCATED_APPEND_ONLY_JOURNAL');
  return content.trimEnd().split('\n').map(line=>JSON.parse(line));
}
function appendDurable(path,value) {
  const fd=openSync(path,'a',0o600);
  try {
    const buffer=Buffer.from(JSON.stringify(value)+'\n','utf8');
    let done=0;
    while(done<buffer.length) done+=writeSync(fd,buffer,done,buffer.length-done);
    fsyncSync(fd);
  } finally {closeSync(fd);}
}
/** Single writer protected across local processes. Stale locks are NEVER auto-stolen. */
export class Journal {
  constructor({dir,budget,clock=()=>new Date().toISOString()}) {
    validateBudgetRecord(budget);
    mkdirSync(dir,{recursive:true});
    this.dir=dir; this.path=join(dir,'events.jsonl'); this.lock=join(dir,'writer.lock');
    this.budget=structuredClone(budget); this.clock=clock; this.failNextAppend=false;
    try { this.lockFd=openSync(this.lock,'wx',0o600); } catch { throw Error('EXCLUSIVE_WRITER_LOCK_HELD'); }
    try { this.load(); } catch(e) { this.close(); throw e; }
  }
  close() { if (this.lockFd !== undefined) {closeSync(this.lockFd); this.lockFd=undefined; unlinkSync(this.lock);} }
  load() {
    this.events=readJsonLines(this.path);this.active=new Map();this.keyToInvocation=new Map();this.lastHash=ZERO;
    for(let i=0;i<this.events.length;i++){
      const e=this.events[i],{sha256,...body}=e;
      insist(e.seq===i+1 && e.prev_sha256===this.lastHash && hash(body)===sha256,'LEDGER_CHAIN_BROKEN');
      this.apply(e);this.lastHash=e.sha256;
      insist(this.balance().global_remaining_micro_usd>=0,'LEDGER_OVERSPEND');
      insist(e.budget_remaining_micro_usd===this.balance().global_remaining_micro_usd,'LEDGER_BALANCE_DRIFT');
    }
  }
  apply(e) {
    if(e.type==='RESERVED'){
      insist(!this.active.has(e.invocation_id) && !this.keyToInvocation.has(e.idempotency_key),'DUPLICATE_RESERVATION');
      this.active.set(e.invocation_id,{agent_id:e.agent_id,invocation_hash:e.invocation_hash,key:e.idempotency_key,reserved:e.reserved_micro_usd,charged:0,state:'RESERVED',reserved_at:e.timestamp,ttl_seconds:e.reservation_ttl_seconds});
      this.keyToInvocation.set(e.idempotency_key,e.invocation_id);
    } else if(e.type==='REJECTED') {
      insist(!this.active.has(e.invocation_id) && !this.keyToInvocation.has(e.idempotency_key),'DUPLICATE_RESERVATION');
      this.active.set(e.invocation_id,{agent_id:e.agent_id,invocation_hash:e.invocation_hash,key:e.idempotency_key,reserved:0,charged:0,state:'REJECTED'});
      this.keyToInvocation.set(e.idempotency_key,e.invocation_id);
    } else {
      const old=this.active.get(e.invocation_id);insist(!!old,'MISSING_RESERVATION');
      if(e.type==='DISPATCHED')insist(old.state==='RESERVED','DISPATCH_SEQUENCE');
      if(e.type==='RECONCILED')insist(['DISPATCHED','UNKNOWN_COST','RECONCILIATION_FAILED'].includes(old.state),'RECONCILE_SEQUENCE');
      if(e.type==='EXPIRED_UNDISPATCHED')insist(['RESERVED','FAILED_DISPATCH'].includes(old.state),'EXPIRE_SEQUENCE');
      if(e.type==='FAILED_DISPATCH')insist(old.state==='RESERVED','FAILED_DISPATCH_SEQUENCE');
      if(e.type==='UNKNOWN_COST'||e.type==='RECONCILIATION_FAILED')insist(['DISPATCHED','UNKNOWN_COST','RECONCILIATION_FAILED'].includes(old.state),'UNKNOWN_SEQUENCE');
      if(e.type==='RECONCILED') {insist(Number.isSafeInteger(e.charged_micro_usd)&&e.charged_micro_usd>=0,'BAD_CHARGE');old.charged=e.charged_micro_usd;}
      old.state=e.type;
    }
  }
  balance() {
    let spent=0,held=0;const perAgent={};
    for(const rec of this.active.values()){
      const current=perAgent[rec.agent_id]??{spent:0,held:0};
      if(rec.state==='RECONCILED'){current.spent+=rec.charged;spent+=rec.charged;}
      else if(!['REJECTED','EXPIRED_UNDISPATCHED'].includes(rec.state)){current.held+=rec.reserved;held+=rec.reserved;}
      perAgent[rec.agent_id]=current;
    }
    return {global_remaining_micro_usd:this.budget.global_cap_micro_usd-spent-held,perAgent};
  }
  getByKey(key) { const id=this.keyToInvocation.get(key);return id?{invocation_id:id,...this.active.get(id)}:null; }
  add(e) {
    insist(STATES.includes(e.type),'BAD_LEDGER_EVENT');
    const event={...e,seq:this.events.length+1,timestamp:this.clock(),prev_sha256:this.lastHash};
    const oldA=this.active,oldK=this.keyToInvocation;
    this.active=new Map([...oldA].map(([k,v])=>[k,{...v}])); this.keyToInvocation=new Map(oldK);
    try {this.apply(event);event.budget_remaining_micro_usd=this.balance().global_remaining_micro_usd;}catch(err){this.active=oldA;this.keyToInvocation=oldK;throw err;}
    event.sha256=hash(event);
    try{
      if(this.failNextAppend){this.failNextAppend=false;throw Error('INJECTED_LEDGER_APPEND_FAILURE');}
      appendDurable(this.path,event);
    }catch(err){this.active=oldA;this.keyToInvocation=oldK;throw err;}
    this.events.push(event);this.lastHash=event.sha256;
    return event;
  }
  reserve({invocation_id,idempotency_key,agent_id,invocation_hash,amount,reservation_ttl_seconds}){
    const matching=this.getByKey(idempotency_key);
    if(matching){insist(matching.invocation_id===invocation_id && matching.invocation_hash===invocation_hash,'IDEMPOTENCY_CONFLICT');return {existing:true,record:matching};}
    insist(!this.active.has(invocation_id),'INVOCATION_ID_REUSED');
    const balance=this.balance();
    const agent=balance.perAgent[agent_id]??{spent:0,held:0};
    const remaining=this.budget.agent_caps_micro_usd[agent_id]-agent.spent-agent.held;
    if(amount>balance.global_remaining_micro_usd||amount>remaining){
      this.add({type:'REJECTED',invocation_id,idempotency_key,agent_id,invocation_hash,reserved_micro_usd:0,reason:'BUDGET_EXHAUSTED'});
      throw Error('BUDGET_EXHAUSTED');
    }
    this.add({type:'RESERVED',invocation_id,idempotency_key,agent_id,invocation_hash,reserved_micro_usd:amount,reservation_ttl_seconds});
    return{existing:false,record:this.getByKey(idempotency_key)};
  }
  appendReceipt(caseId, receipt) {
    insist(/^[a-z0-9][a-z0-9._-]{2,79}$/.test(caseId),'RECEIPT_CASE_ID');
    const path=join(this.dir,'case-'+caseId+'.jsonl');
    const prev=readJsonLines(path); this.verifyReceiptChain(prev);
    const body={...receipt,case_id:caseId,sequence:prev.length+1,prev_receipt_sha256:prev.length?prev.at(-1).receipt_sha256:ZERO};
    const rec={...body,receipt_sha256:hash(body)};
    appendDurable(path,rec);
    return rec;
  }
  verifyReceiptChain(receipts,expectedHead) {
    let last=ZERO;
    for(let i=0;i<receipts.length;i++){
      const r=receipts[i],{receipt_sha256,...body}=r;
      insist(r.sequence===i+1&&r.prev_receipt_sha256===last&&hash(body)===receipt_sha256,'RECEIPT_CHAIN_BROKEN');
      last=receipt_sha256;
    }
    if(expectedHead!==undefined)insist(expectedHead===last,'EXTERNAL_ANCHOR_MISMATCH');
    return last;
  }
  receipts(caseId,anchorHead) { const r=readJsonLines(join(this.dir,'case-'+caseId+'.jsonl'));this.verifyReceiptChain(r,anchorHead);return r; }
  checkpoint() {
    const case_heads={};
    for(const f of readdirSync(this.dir).filter(x=>x.startsWith('case-')&&x.endsWith('.jsonl')).sort()){
      const id=f.slice(5,-6);case_heads[id]=this.verifyReceiptChain(readJsonLines(join(this.dir,f)));
    }
    const body={schema:'computerwisdom.ci-first.checkpoint.v0.3',ledger_head_sha256:this.lastHash,case_heads,authority_created:false,canon:false};
    return {...body,checkpoint_sha256:hash(body)};
  }
}
