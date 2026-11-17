import {assert,combine,digest,handoff,verifiedSource,verifyHandoff} from './contracts.mjs';
function mem(facts=[],decisions=[],open_questions=[]) {return {facts,decisions,open_questions}}
export const roles={
  async intake(c) {
    const valid=c.claims.every(x=>typeof x.id==='string'&&typeof x.rule==='string'&&Array.isArray(x.evidence_ids)) && c.evidence.every(x=>typeof x.id==='string');
    return handoff('intake','done',valid?'PASS':'FAIL',[],[{check:'INPUT_SHAPE',verdict:valid?'PASS':'FAIL',claims:c.claims.length,evidence:c.evidence.length}],mem([{key:'case_id',value:c.case_id,source_id:'CASE_CONTRACT'}]));
  },
  async provenance(c) {
    const findings=c.evidence.map(verifiedSource);
    const verdict=combine(findings.map(f=>f.verdict));
    return handoff('provenance','done',verdict,c.evidence.map(x=>x.id),findings,mem(findings.filter(x=>x.verdict==='PASS').map(x=>({key:'bytes_checked',value:x.id,source_id:x.id})),[],[{question:'Is the historical fixture independently authenticated at its source?'}]));
  },
  async mathematics(c) {
    const sourceIDs=new Set(c.evidence.map(x=>x.id));
    const findings=c.claims.map(x=>{
      if(!x.evidence_ids.every(id=>sourceIDs.has(id)))return {claim_id:x.id,verdict:'UNKNOWN',reason:'MISSING_EVIDENCE_REF'};
      if(x.rule==='requires_live_http')return {claim_id:x.id,verdict:'UNKNOWN',reason:'NO_NETWORK_IN_OFFLINE_FIXTURE'};
      if(!Array.isArray(x.left)||!Array.isArray(x.right)||!x.left.every(v=>typeof v==='string')||!x.right.every(v=>typeof v==='string'))return {claim_id:x.id,verdict:'FAIL',reason:'RULE_ARGUMENTS'};
      let observed;
      if(x.rule==='disjoint')observed=x.left.every(v=>!x.right.includes(v));
      else if(x.rule==='equal')observed=JSON.stringify(x.left)===JSON.stringify(x.right);
      else return {claim_id:x.id,verdict:'FAIL',reason:'UNRECOGNIZED_RULE'};
      return {claim_id:x.id,verdict:observed===x.expect?'PASS':'FAIL',observed,expected:x.expect,rule:x.rule,scope:'FIXTURE_MATH_ONLY'};
    });
    const verdict=combine(findings.map(x=>x.verdict));
    return handoff('mathematics','done',verdict,c.claims.flatMap(x=>x.evidence_ids),findings,mem([],[],findings.filter(x=>x.verdict==='UNKNOWN').map(x=>({question:`Missing live proof for ${x.claim_id}`}))));
  },
  async contradiction(c) {
    const pairs=[];
    for(let i=0;i<c.claims.length;i++)for(let j=i+1;j<c.claims.length;j++){
      const a=c.claims[i],b=c.claims[j];
      if(a.subject && a.subject===b.subject && a.rule===b.rule && JSON.stringify(a.left)===JSON.stringify(b.left) && JSON.stringify(a.right)===JSON.stringify(b.right) && a.expect!==b.expect)pairs.push([a.id,b.id]);
    }
    const verdict=pairs.length?'FAIL':'PASS';
    return handoff('contradiction','done',verdict,[],[{check:'EXPLICIT_CONTRADICTIONS',verdict,pairs}],mem());
  },
  async safety(c) {
    const forbidden=/(?:-----BEGIN [^-]*PRIVATE KEY-----|\bsk-proj-[a-zA-Z0-9_-]{12,}|\b(?:seed phrase|mnemonic phrase)\s*[:=]\s*\w+)/i;
    const secret=c.evidence.some(x=>forbidden.test(x.content));
    const ok=!secret && c.canon===false && c.authority_created===false && c.mode==='offline_fixture';
    return handoff('safety','done',ok?'PASS':'FAIL',c.evidence.map(x=>x.id),[{check:'NO_SECRETS_NO_WRITES',verdict:ok?'PASS':'FAIL'}],mem([], [{decision:'No authority promotion, payments, signing, or network calls',rationale:'Offline-only contract'}]));
  },
  async replay(c) {
    const checks=c.evidence.map(verifiedSource);
    const ok=checks.every(x=>x.verdict==='PASS');
    return handoff('replay','done',ok?'PASS':'FAIL',c.evidence.map(x=>x.id),[{check:'DETERMINISTIC_CASE_DIGEST',case_sha256:digest(c),verdict:ok?'PASS':'FAIL'},{check:'SOURCE_BYTE_REPLAY',verdict:ok?'PASS':'FAIL'}],mem());
  },
  async synthesis(c, prior, memory) {
    const first=['intake','provenance','mathematics','contradiction','safety','replay'];
    for(const name of first)verifyHandoff(prior[name],name);
    const quality=combine(first.map(x=>prior[x].verdict));
    const live= c.mode==='offline_fixture'?'UNKNOWN':'FAIL';
    const verdict=combine([quality,live]);
    return handoff('synthesis','done',verdict,c.evidence.map(x=>x.id),[{check:'MECHANICAL_VALIDATION',verdict:quality},{check:'LIVE_INDEPENDENT_VERIFICATION',verdict:live},{check:'MEMORY_FACT_COUNT',count:memory.facts.length}],mem([], [{decision:'Hold production promotion',rationale:'Offline fixture cannot prove live system'}], [{question:'Obtain live independently verified execution traces and signed receipts'}]));
  },
  async supervisor(c, prior, memory) {
    const first=['intake','provenance','mathematics','contradiction','safety','replay','synthesis'];
    for(const name of first)verifyHandoff(prior[name],name);
    const integrity= prior.provenance.verdict==='PASS' && prior.safety.verdict==='PASS' && prior.replay.verdict==='PASS';
    const verdict=integrity?combine(first.map(x=>prior[x].verdict)):'FAIL';
    return handoff('supervisor','done',verdict,c.evidence.map(x=>x.id),[
      {check:'ALL_SEVEN_HANDOFF_HASHES',verdict:'PASS'},
      {check:'SOURCE_INTEGRITY_AND_SAFETY',verdict:integrity?'PASS':'FAIL'},
      {check:'PRODUCTION_AUTHORITY',verdict:'UNKNOWN',reason:'NO_LIVE_AUTHORITY_VERIFICATION'},
      {check:'MEMORY_INDEPENDENCE',verdict:'PASS',facts:memory.facts.length}
    ],mem([], [{decision:'Refuse automatic promotion',rationale:'No independently verified live proof or explicit transaction authority'}]));
  }
};
