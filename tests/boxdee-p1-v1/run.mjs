#!/usr/bin/env node
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import { verify, jcs } from '../../tools/boxdee_p1_verifier_v1.mjs';

const H = 'a'.repeat(64);

function receipt(id, binding, cls='RECEIPT', extra={}) {
  return {id, type:'HASH', class:cls, binding, value:{observed:true}, sha256:H, ...extra};
}

function base(overrides={}) {
  const v = {
    standard:'GBS-BOXDEE-BURDEN-V001',
    contractVersion:'INPUT_EVIDENCE_V1',
    claimant:'tester',
    claim:'bounded claim',
    claimClass:'FACT_CLAIM',
    source:{surface:'fixture',url:null,status:'OBSERVED'},
    object:{identifier:'object-1',description:null,status:'OBSERVED'},
    time:{value:'2026-08-24T00:00:00Z',timezone:'UTC',status:'OBSERVED'},
    action:{assertedTransition:'state A -> state B',status:'OBSERVED'},
    readback:{status:'MATCH',value:'state B',source:'fixture'},
    receipts:[
      receipt('r-source','SOURCE'),
      receipt('r-object','OBJECT'),
      receipt('r-time','TIME'),
      receipt('r-action','ACTION'),
      receipt('r-readback','READBACK')
    ],
    replay:{chainStatus:'COMPLETE',replayStatus:'COMPLETE'}
  };
  return Object.assign(v, overrides);
}

const cases = [
  ['01_all_observed_match_complete_pass', base(), 'PASS'],
  ['02_missing_source_hold', base({source:{surface:'fixture',url:null,status:'UNOBSERVED'}}), 'HOLD'],
  ['03_search_miss_hold', base({source:{surface:'fixture',url:null,status:'SEARCH_MISS'}}), 'HOLD'],
  ['04_unavailable_readback_hold', base({readback:{status:'UNAVAILABLE',value:null,source:null}}), 'HOLD'],
  ['05_partial_chain_hold', base({replay:{chainStatus:'PARTIAL',replayStatus:'COMPLETE'}}), 'HOLD'],
  ['06_partial_replay_hold', base({replay:{chainStatus:'COMPLETE',replayStatus:'PARTIAL'}}), 'HOLD'],
  ['07_bound_mismatch_delta', base({readback:{status:'MISMATCH',value:'state C',source:'fixture'}}), 'DELTA'],
  ['08_contradictory_receipts_fail', base({receipts:[
    receipt('r-source-a','SOURCE','RECEIPT',{assertionKey:'source.identity',assertionValue:'A'}),
    receipt('r-source-b','SOURCE','RECEIPT',{assertionKey:'source.identity',assertionValue:'B'}),
    receipt('r-object','OBJECT'),receipt('r-time','TIME'),receipt('r-action','ACTION'),receipt('r-readback','READBACK')
  ]}), 'FAIL'],
  ['09_caller_result_injection_fail', {...base(), authority:true}, 'FAIL'],
  ['10_visualization_only_hold', base({receipts:[
    receipt('r-source','SOURCE','VISUALIZATION'),receipt('r-object','OBJECT','VISUALIZATION'),receipt('r-time','TIME','VISUALIZATION'),receipt('r-action','ACTION','VISUALIZATION'),receipt('r-readback','READBACK','VISUALIZATION')
  ]}), 'HOLD'],
  ['11_draft_only_hold', base({receipts:[
    receipt('r-source','SOURCE','DRAFT'),receipt('r-object','OBJECT','DRAFT'),receipt('r-time','TIME','DRAFT'),receipt('r-action','ACTION','DRAFT'),receipt('r-readback','READBACK','DRAFT')
  ]}), 'HOLD'],
  ['12_pass_authority_false', base({claimClass:'SELF_REPORT',claim:'speaker reports this'}), 'PASS'],
  ['13_mixed_requires_decomposition_hold', base({claimClass:'MIXED',claim:'contains multiple claim classes'}), 'HOLD']
];

const outputs = [];
for (const [id,input,expected] of cases) {
  const result = verify(input);
  assert.equal(result.derivedResult, expected, `${id}: disposition`);
  assert.equal(result.authority, false, `${id}: authority`);
  if (id === '05_partial_chain_hold') assert.equal(result.internalFlags.hasPartialChain, true);
  if (id === '06_partial_replay_hold') assert.equal(result.internalFlags.hasPartialReplay, true);
  if (id === '03_search_miss_hold') assert.ok(result.reasons.includes('SEARCH_MISS_NOT_ABSENCE'));
  if (id === '13_mixed_requires_decomposition_hold') assert.ok(result.reasons.includes('MIXED_REQUIRES_DECOMPOSITION'));
  outputs.push({id,result});
}

const deterministicInput = base();
const a = jcs(verify(deterministicInput));
const b = jcs(verify(JSON.parse(jcs(deterministicInput))));
assert.equal(a,b,'identical canonical input must emit byte-identical canonical output');
const digest = crypto.createHash('sha256').update(Buffer.from(a,'utf8')).digest('hex');

process.stdout.write(JSON.stringify({
  schema:'P1_CONFORMANCE_RECEIPT_V1',
  vectorsPassed:cases.length,
  vectorsTotal:cases.length,
  deterministicCanonicalOutputSha256:digest,
  authority:false,
  outputs
}, null, 2) + '\n');
