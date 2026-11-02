import assert from 'node:assert/strict';
import {method,review} from './wisdom-method.mjs';
const fresh=()=>method.steps.map(step=>({step,state:'ESTABLISHED',reason:'Synthetic source pointer supplied',evidence_refs:['synthetic:record-1'],mandatory:true}));
const cases=[['duplicate-source inflation','FIND','CONFLICT'],['unknown denominator','COMPARE','NOT_ESTABLISHED'],['conflicting rules','COMPARE','CONFLICT'],['missing eligibility','ASK','NOT_ESTABLISHED'],['staged but unsettled payment','LABEL','NOT_ESTABLISHED'],['reversed settlement','LABEL','CONFLICT'],['wrong-scope receipt','RECEIPT','CONFLICT'],['allegation vs conviction','LABEL','CONFLICT'],['privacy leakage','PROTECT','CONFLICT'],['correct HOLD','REPLAY','NOT_ESTABLISHED']];
for(const [name,step,state] of cases){const dims=fresh();Object.assign(dims.find(d=>d.step===step),{state,reason:'Declared synthetic condition: '+name});const r=review({dimensions:dims});assert.equal(r.outcome,'HOLD');assert.equal(r.numeric_score,null);assert.ok(r.blockers.includes(step));console.log('PASS '+name)}
assert.equal(review({dimensions:fresh()}).outcome,'READY_FOR_HUMAN_REVIEW');
assert.equal(review({dimensions:fresh().slice(0,7)}).outcome,'HOLD');
const bad=fresh();bad[0].state='PASS';assert.throws(()=>review({dimensions:bad}));
const noReason=fresh();noReason[0].reason='';assert.throws(()=>review({dimensions:noReason}));
console.log(JSON.stringify({passed:14,failed:0,scope:'LOCAL_SYNTHETIC_REVIEW_POLICY; not live legal/financial classification'}));
