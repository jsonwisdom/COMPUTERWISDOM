import {ROLES,assert,canonical,digest,inputContract,verifyHandoff} from './contracts.mjs';
import {roles} from './roles.mjs';
function mergeMemory(memory, handoffs) {
  const next=structuredClone(memory);
  for(const h of handoffs){
    for(const category of ['facts','decisions','open_questions'])next[category].push(...h.memory_updates[category].map(x=>({...x,agent:h.agent})));
  }
  return next;
}
async function boundedParallel(names,concurrency,job){
  const result={};let cursor=0;
  await Promise.all(Array.from({length:Math.min(names.length,concurrency)},async()=>{
    while(cursor<names.length){const name=names[cursor++];result[name]=await job(name)}
  }));
  return result;
}
export async function runSwarm(caseInput,{concurrency=4,agentOverride={}}={}){
  const c=inputContract(structuredClone(caseInput));
  assert(Number.isInteger(concurrency)&&concurrency>=1&&concurrency<=4,'CONCURRENCY_CAP_4');
  const names=ROLES.slice(0,6);
  const prior=await boundedParallel(names,concurrency,async(name)=>{
    const fn=agentOverride[name]||roles[name];
    const out=await fn(structuredClone(c));
    verifyHandoff(out,name);
    return out;
  });
  let memory=mergeMemory({facts:[],decisions:[],open_questions:[]},names.map(name=>prior[name]));
  prior.synthesis=await (agentOverride.synthesis||roles.synthesis)(structuredClone(c),structuredClone(prior),structuredClone(memory));
  verifyHandoff(prior.synthesis,'synthesis');
  memory=mergeMemory(memory,[prior.synthesis]);
  prior.supervisor=await (agentOverride.supervisor||roles.supervisor)(structuredClone(c),structuredClone(prior),structuredClone(memory));
  verifyHandoff(prior.supervisor,'supervisor');
  memory=mergeMemory(memory,[prior.supervisor]);
  const handoffs=ROLES.map(name=>prior[name]);
  const receipt={
    schema:'computerwisdom.ci-first.swarm-receipt.v1',case_id:c.case_id,mode:c.mode,
    agents:ROLES.length,concurrency,agent_order:ROLES,case_sha256:digest(c),
    verdict:prior.supervisor.verdict,production_verification:'UNKNOWN',
    evaluation_scope:'OFFLINE_FIXTURE_ONLY',mock_model_calls:0,model_api_calls:0,
    tokens_used:0,api_cost_usd:0,performance_vs_single_agent:'UNKNOWN',
    memory, handoffs,
    canon:false,authority_created:false,signing:false,payment:false,deployment:false
  };
  return {...receipt,sha256:digest(receipt)};
}
export function verifyReceipt(receipt,caseInput){
  inputContract(caseInput);
  const {sha256:hash,...body}=receipt;
  assert(digest(body)===hash,'RECEIPT_HASH_MISMATCH');
  assert(receipt.case_sha256===digest(caseInput),'CASE_HASH_MISMATCH');
  assert(receipt.handoffs.length===ROLES.length,'AGENT_COUNT_MISMATCH');
  receipt.handoffs.forEach((h,i)=>verifyHandoff(h,ROLES[i]));
  assert(receipt.canon===false && receipt.authority_created===false,'RECEIPT_UNAUTHORIZED');
  assert(receipt.production_verification==='UNKNOWN','FALSE_PRODUCTION_CLAIM');
  return true;
}
