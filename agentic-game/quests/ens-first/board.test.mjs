import test from 'node:test';
import assert from 'node:assert/strict';
import {score,manifest} from './board.mjs';
const review = id => ({quest_id:id,kind:'LEARNING_REVIEW',review_ref:'fixture:review',reflection:'A name alone did not prove control.'});
test('ENS comes first and all later quests start locked',()=>{
 const r=score(); assert.equal(r.score,0); assert.equal(r.quests[0].status,'AVAILABLE');
 assert.ok(r.quests.slice(1).every(q=>q.status==='LOCKED'));
});
test('cannot skip ENS, award for a CI PASS, or repeat a quest',()=>{
 const r=score([review('CI_REPLAY'),{...review('ENS_MAP'),kind:'CI_PASS'},review('ENS_MAP'),review('ENS_MAP')]);
 assert.equal(r.score,10); assert.equal(r.rejected.length,3);
});
test('missing review or reflection does not earn points',()=>{
 assert.equal(score([{...review('ENS_MAP'),review_ref:''},{...review('ENS_MAP'),reflection:''}]).score,0);
});
test('full learning progression never verifies evidence or creates authority',()=>{
 const r=score(manifest.quests.map(q=>review(q.id)));
 assert.equal(r.score,100); assert.equal(r.evidence_verified,false); assert.equal(r.authority_created,false);
});
