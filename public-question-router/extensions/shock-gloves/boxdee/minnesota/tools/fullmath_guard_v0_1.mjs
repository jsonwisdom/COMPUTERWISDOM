// THE ART OF LEARING: local, dependency-free receipt metadata and synthetic clock checks.
// Read-only, no networking/payments/authority/proof admission.
export function auditRegistry(registry){
 const all=Array.from({length:13},(_,i)=>`MNK-${String(i+1).padStart(3,"0")}`);
 const allowed=new Set(all),seen=new Set(),receipts=new Set(),errors=[];
 if(registry?.registry_id!=="MINNESOTA_REPLAY_VALIDATION_REGISTRY_V0_1")errors.push("REGISTRY_ID");
 if(!Array.isArray(registry?.receipts))errors.push("MISSING_RECEIPTS");
 for(const r of registry?.receipts||[]){
  if(receipts.has(r.receipt_id))errors.push("DUPLICATE_RECEIPT");
  receipts.add(r.receipt_id);
  if(!Array.isArray(r.exercised)||r.exercised.some(id=>!allowed.has(id)))errors.push("UNKNOWN_GATE");
  else for(const id of r.exercised)seen.add(id);
  if(r.overall_disposition!=="HOLD")errors.push("RECEIPT_NOT_HOLD");
 }
 const exercised=[...seen].sort(),unexercised=all.filter(id=>!seen.has(id)),s=registry?.cumulative_gate_state||{};
 const equal=(a,b)=>Array.isArray(a)&&JSON.stringify([...a].sort())===JSON.stringify([...b].sort());
 if(s.tests_total!==13)errors.push("TOTAL");
 if(s.distinct_exercised!==exercised.length)errors.push("EXERCISED_COUNT");
 if(s.distinct_unexercised!==unexercised.length)errors.push("UNEXERCISED_COUNT");
 if(!equal(s.exercised_ids,exercised))errors.push("EXERCISED_SET");
 if(!equal(s.unexercised_ids,unexercised))errors.push("UNEXERCISED_SET");
 if(s.coverage_fraction!==`${exercised.length}/13`)errors.push("COVERAGE_FRACTION");
 if(registry?.no_fake_green?.overall_disposition!=="HOLD")errors.push("PARENT_HOLD");
 return {status:errors.length?"CONFLICT":"CONSISTENT_METADATA_ONLY",errors,receipt_count:receipts.size,defined:13,exercised_ids:exercised,unexercised_ids:unexercised,exercised:exercised.length,unexercised:unexercised.length,coverage_percent:Number((100*exercised.length/13).toFixed(4)),parent_disposition:"HOLD",independent_reexecution:false,proof_admission:false,authority_created:false};
}

export function inspectClockFixture(fixture){
 const keys=["event_time","document_time","publication_time","effective_time","update_time","retrieval_time"];
 const base={real_mn_gate_exercised:false,coverage_increment:0,proof_admission:false,authority_created:false,wrongdoing_finding_created:false,parent_disposition:"HOLD"};
 if(fixture?.classification!=="SYNTHETIC_ONLY"||fixture?.proof_admission!==false||fixture?.authority_created!==false)return {...base,status:"HOLD",reason:"NOT_AUTHORIZED_SYNTHETIC_FIXTURE"};
 const clocks=fixture?.clocks||{},missing=keys.filter(k=>typeof clocks[k]!=="string");
 if(missing.length)return {...base,status:"HOLD",reason:"MISSING_CLOCKS",missing};
 const strict=/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/;
 if(keys.some(k=>!strict.test(clocks[k])||!Number.isFinite(Date.parse(clocks[k]))))return {...base,status:"HOLD",reason:"INVALID_CLOCK"};
 const order=fixture?.expected_order;
 if(!Array.isArray(order)||!order.length)return {...base,status:"HOLD",reason:"MISSING_ORDER_RULES"};
 const conflicts=[];
 for(const pair of order){
  if(!Array.isArray(pair)||pair.length!==2||!keys.includes(pair[0])||!keys.includes(pair[1]))return {...base,status:"HOLD",reason:"INVALID_ORDER_RULE"};
  if(Date.parse(clocks[pair[0]])>Date.parse(clocks[pair[1]]))conflicts.push({before:pair[0],after:pair[1],left:clocks[pair[0]],right:clocks[pair[1]]});
 }
 return {...base,status:conflicts.length?"CONFLICT":"SIMULATION_PASS",fixture_id:fixture.fixture_id,original_clocks:clocks,order_rules_checked:order.length,conflicts};
}
