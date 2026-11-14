import test from 'node:test';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {checkMnk003Candidate,CLOCKS} from '../tools/mnk003_source_clock_check_v0_1.mjs';

const source=CLOCKS.map((k,i)=>k+': 2026-10-'+String(i+10)+'T12:00:00Z').join('\n');
const packet={
 gate:'MNK-003',jurisdiction:'Minnesota',
 source_url:'https://example.org/fictional-clock-fixture',
 expected_source_sha256:createHash('sha256').update(source).digest('hex'),
 clocks:Object.fromEntries(CLOCKS.map((key,i)=>[key,{
  value:'2026-10-'+String(i+10)+'T12:00:00Z',
  quote:key+': 2026-10-'+String(i+10)+'T12:00:00Z',
  locator:'line '+String(i+1)
 }])),
 comparisons:[{before:'event_time',after:'document_time',reason:'Fixture-only ordering rule'}]
};
const copy=x=>JSON.parse(JSON.stringify(x));
test('source byte check cannot advance real Minnesota coverage',()=>{
 const r=checkMnk003Candidate(packet,source);
 assert.equal(r.source_bytes_sha256,packet.expected_source_sha256);
 assert.equal(r.comparisons[0].check,'ORDER_COMPATIBLE');
 assert.deepEqual(Object.keys(r.original_clocks),CLOCKS);
 assert.equal(r.status,'HOLD');
 assert.equal(r.gate_exercised,false);assert.equal(r.coverage_increment,0);
 assert.equal(r.primary_source_authenticated,false);
 assert.equal(r.authority_created,false);
});
test('missing source bytes remains HOLD',()=>{
 const r=checkMnk003Candidate(packet,null);
 assert.equal(r.status,'HOLD');assert.ok(r.issues.includes('SOURCE_BYTES_UNAVAILABLE'));
});
test('source byte mismatch remains visible',()=>{
 const r=checkMnk003Candidate(packet,source+'\nchanged');
 assert.ok(r.issues.includes('SOURCE_BYTES_HASH_MISMATCH'));
 assert.equal(r.status,'HOLD');
});
test('missing effective clock stays UNKNOWN',()=>{
 const p=copy(packet);delete p.clocks.effective_time;
 const r=checkMnk003Candidate(p,source);
 assert.equal(r.original_clocks.effective_time,'UNKNOWN');
 assert.ok(r.issues.includes('CLOCK_UNBOUND:effective_time'));
});
test('invalid calendar dates cannot normalize silently',()=>{
 const p=copy(packet);p.clocks.document_time.value='2026-02-30T12:00:00Z';
 const r=checkMnk003Candidate(p,source);
 assert.ok(r.issues.includes('CLOCK_INVALID_OR_UNBOUND:document_time'));
});
test('inverted chronology becomes candidate, never proof',()=>{
 const p=copy(packet);
 p.comparisons=[{before:'document_time',after:'event_time',reason:'Fictional reverse order'}];
 const r=checkMnk003Candidate(p,source);
 assert.equal(r.comparisons[0].check,'INVERSION_CANDIDATE');
 assert.ok(r.issues.includes('CLOCK_CONFLICT_CANDIDATE_NEEDS_CONTEXT'));
 assert.equal(r.status,'HOLD');assert.equal(r.proof_admission,false);
});
test('unanchored source quote and locator remain visible',()=>{
 const p=copy(packet);p.clocks.event_time.quote='absent phrase';delete p.clocks.event_time.locator;
 const r=checkMnk003Candidate(p,source);
 assert.ok(r.issues.includes('CLOCK_QUOTE_UNANCHORED:event_time'));
 assert.ok(r.issues.includes('CLOCK_LOCATOR_UNBOUND:event_time'));
});
test('meaningless comparison rule is invalid',()=>{
 const p=copy(packet);
 p.comparisons=[{before:'event_time',after:'document_time',reason:''}];
 const r=checkMnk003Candidate(p,source);
 assert.ok(r.issues.includes('INVALID_COMPARISON_RULE'));
});
