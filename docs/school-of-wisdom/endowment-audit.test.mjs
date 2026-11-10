import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';

const root=new URL('./',import.meta.url);
const doc=JSON.parse(readFileSync(new URL('endowment-audit-v0.1.json',root),'utf8'));
const readme=readFileSync(new URL('endowment-audit-v0.1.md',root),'utf8');
const app=readFileSync(new URL('../jason-on-base/index.html',root),'utf8');

assert.equal(doc.schema,'COMPUTERWISDOM_SCHOOL_ENDOWMENT_AUDIT_V0_1');
assert.equal(doc.status,'DRAFT_REVIEW_ONLY');
for(const key of ['authority_created','public_release_authorized','school_enrollment_or_partnership'])assert.equal(doc[key],false);
const id = doc.controls.map(x=>x.id);
assert.equal(id.length,12);
assert.equal(new Set(id).size,12,'Control IDs must be unique');
assert.deepEqual(id,[
 '01-entity-scope','02-collection-provenance','03-fund-type','04-donor-intent',
 '05-reconciliation','06-investment','07-related-party','08-cross-entity',
 '09-outcome','10-foreign-disclosure','11-privacy','12-review'
]);
for(const c of doc.controls){assert.ok(c.test.length>=80,c.id);assert.ok(c.failure.length>20,c.id);}
assert.ok(/for sustained institutional use/.test(doc.taxonomy.endowment));
assert.ok(/not necessarily/.test(doc.taxonomy.ordinary_donation));
assert.ok(/separate legal reporting entity/.test(doc.taxonomy.foundation));
assert.ok(doc.roles.student.includes('de-identified'));
assert.ok(doc.roles.librarian.includes('never infer private donor names'));
const m=doc.calculation_definition;
assert.equal(m.unit,'integer cents');
assert.equal(m.gross_return_includes_fees,false);
assert.equal(m.sample.type,'SYNTHETIC_CLASSROOM_FIXTURE');
assert.equal(m.sample.verified_source,false);
assert.equal(m.sample.real_transaction,false);
const s=m.sample;
const result=s.opening_cents+s.received_gifts_cents+s.gross_investment_return_cents+s.signed_transfers_cents-s.spending_cents-s.fees_cents;
assert.equal(result,133000);
assert.equal(result,s.closing_cents);
assert.equal(result-s.received_gifts_cents-s.gross_investment_return_cents-s.signed_transfers_cents+s.spending_cents+s.fees_cents,s.opening_cents,'Reverse exact integer cents');
assert.equal(doc.historical_evidence.source_observation_count,'UNKNOWN');
assert.equal(doc.historical_evidence.eligible_day_coverage,'UNKNOWN');
assert.equal(doc.ci_first.institutional_financial_audit,'NOT_PERFORMED');
assert.equal(doc.ci_first.release,'HOLD');
assert.ok(doc.excluded.includes('No children or family lineage mapped'));
assert.ok(doc.excluded.includes('No automatically published donor identities'));
assert.ok(doc.source_registry.length>=8);
for(const source of doc.source_registry){assert.equal(source.type,'OFFICIAL');assert.match(source.url,/^https:\/\//);assert.ok(readme.includes(source.url));}
assert.match(readme,/not every charitable donation/i);
assert.match(readme,/not a universal K–12 rule/i);
assert.match(readme,/FERPA/);
assert.match(readme,/UNKNOWN/);
assert.match(app,/href="\.\.\/school-of-wisdom\/endowment-audit-v0\.1\.md"/);
console.log('ENDOWMENT_RULES: PASS | 12 bounded controls | 8 official locator references | donor/student privacy | no authority');
console.log('SYNTHETIC_ROLLFORWARD: PASS | 100000+30000+10000-6000-1000 = 133000 cents | reverse PASS');
console.log('THREE_YEAR_REAL_CORPUS: UNKNOWN | REAL ENDOWMENT AUDIT: NOT PERFORMED | PUBLICATION: HOLD');
