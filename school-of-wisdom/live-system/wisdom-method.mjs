export const method={schema:'classes-with-glasses-method/0.1',status:'DRAFT_IMPLEMENTATION',steps:['ASK','FIND','PROTECT','COMPARE','LABEL','RECEIPT','REPLAY','EXPLAIN'],dimension_states:['ESTABLISHED','NOT_ESTABLISHED','CONFLICT','NOT_APPLICABLE'],numeric_weights:null,pass_threshold:null,authority_created:false,truth_from_score:false};
export function review(input){
 if(!input||!Array.isArray(input.dimensions)||!input.dimensions.length)throw Error('Dimensions required');
 const seen=new Set();for(const d of input.dimensions){if(!method.steps.includes(d.step)||seen.has(d.step)||!method.dimension_states.includes(d.state)||typeof d.reason!=='string'||!d.reason.trim()||!Array.isArray(d.evidence_refs)||d.evidence_refs.some(x=>typeof x!=='string')||typeof d.mandatory!=='boolean')throw Error('Invalid dimension');seen.add(d.step);if(d.mandatory&&d.state==='NOT_APPLICABLE')throw Error('Mandatory dimension needs an explicit review disposition');}
 const blockers=input.dimensions.filter(d=>d.mandatory&&d.state!=='ESTABLISHED').map(d=>d.step);
 const missing=method.steps.filter(s=>!seen.has(s));
 return {method:method.schema,outcome:blockers.length||missing.length?'HOLD':'READY_FOR_HUMAN_REVIEW',blockers,missing_dimensions:missing,authority_created:false,numeric_score:null,meaning:'Review completeness only; evidence references are not independently authenticated by this evaluator'};
}
