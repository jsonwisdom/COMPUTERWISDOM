/** Computer Wisdom Registered Proofs v1. SHA256 binds public bytes, not identity or truth. */
import { createHash } from 'node:crypto';
import { readFile, readdir, writeFile, mkdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
export const ROOT = path.dirname(fileURLToPath(import.meta.url));
export const SHA256 = bytes=>createHash('sha256').update(bytes).digest('hex');
export const CI = new Set(['PASS','FAIL','UNKNOWN']);
export function effective(checks){
  if(!Array.isArray(checks)||checks.length===0) throw Error('Empty check inventory');
  if(checks.some(c=>!CI.has(c.status))) throw Error('Unsupported CI status');
  return checks.some(c=>c.status==='FAIL')?'FAIL':checks.some(c=>c.status==='UNKNOWN')?'UNKNOWN':'PASS';
}
export function validateRecord(r){
  if(r?.schema!=='CW_REGISTERED_PROOF_V1')throw Error('Invalid schema');
  if(!/^[A-Z][A-Z0-9_-]{5,70}$/.test(r.id))throw Error('Invalid proof ID');
  if(!r.claim||!r.scope||!r.record_created_utc||!r.evidence||!r.checks)throw Error('Missing required fields');
  if(!/^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z$/.test(r.record_created_utc)||!Number.isFinite(Date.parse(r.record_created_utc)))throw Error('UTC required');
  if(!Array.isArray(r.evidence)||r.evidence.length===0)throw Error('Source evidence required');
  for(const e of r.evidence){
    if(typeof e.source!=='string'||!/^https:\/\//.test(e.source))throw Error('HTTPS source locator required');
    if(e.raw_bytes_sha256!==null&&!/^[a-f0-9]{64}$/.test(e.raw_bytes_sha256||''))throw Error('Bad source digest; use null when exact bytes not captured');
    if(typeof e.assertion!=='string'||!e.assertion) throw Error('Evidence assertion required');
  }
  if(!Array.isArray(r.checks)||r.checks.length===0) throw Error('Checks required');
  for(const c of r.checks){if(typeof c.id!=='string'||!c.id||!CI.has(c.status)||typeof c.reason!=='string'||!c.reason) throw Error('Invalid scoped check')}
  if(r.ci_verdict!==effective(r.checks))throw Error('Verdict disagrees with checks');
  if(r.authority_created!==false||r.external_certification!==false||r.payment_authorized!==false)throw Error('Human authority, certification, and payment must not be minted');
  if(!Array.isArray(r.not_proven)||r.not_proven.length===0)throw Error('Explicit exclusions required');
  if(r.scope==='HARDWARE_ATTESTATION'&&r.ci_verdict==='PASS')throw Error('No hardware PASS without trusted independent quote verification');
  if(JSON.stringify(r).match(/(?:\b\d{6}-){7}\d{6}\b/)) throw Error('Possible 48-digit recovery key; refuse');
  return r;
}
const rawLeaf = (id,digest)=>Buffer.concat([Buffer.from('CW_PROOF_LEAF_V1\0'+id+'\0','utf8'),Buffer.from(digest,'hex')]);
export const leafHash=(id,digest)=>SHA256(rawLeaf(id,digest));
const parentHash=(a,b)=>SHA256(Buffer.concat([Buffer.from('CW_PROOF_NODE_V1\0'),Buffer.from(a,'hex'),Buffer.from(b,'hex')]));
export function tree(leaves){
  if(!Array.isArray(leaves)||leaves.length===0)throw Error('No leaves');
  const levels=[leaves];let curr=leaves;
  while(curr.length>1){const next=[];for(let i=0;i<curr.length;i+=2){next.push(parentHash(curr[i],curr[i+1]||curr[i]))}levels.push(next);curr=next}
  return levels;
}
export function inclusion(levels,index){const siblings=[];for(let l=0;l<levels.length-1;l++){const row=levels[l],sib=index^1;siblings.push({hash:row[sib]||row[index],side:index%2?'left':'right'});index=Math.floor(index/2)}return siblings}
export function verifyInclusion(id,digest,proof,root){let value=leafHash(id,digest);for(const s of proof){if(!/^[a-f0-9]{64}$/.test(s.hash))return false;value=s.side==='left'?parentHash(s.hash,value):s.side==='right'?parentHash(value,s.hash):'';if(!value)return false}return value===root}
export async function createSnapshot(dir=ROOT){
  const names=(await readdir(path.join(dir,'records'))).filter(x=>x.endsWith('.json')).sort();if(!names.length)throw Error('No proofs');
  const entries=[];
  for(const name of names){const raw=await readFile(path.join(dir,'records',name));const r=validateRecord(JSON.parse(raw.toString('utf8')));if(name!==r.id+'.json')throw Error('Filename/ID mismatch '+name);entries.push({id:r.id,sha256:SHA256(raw),ci_verdict:r.ci_verdict,scope:r.scope})}
  if(new Set(entries.map(e=>e.id)).size!==entries.length)throw Error('Duplicate ID');
  const levels=tree(entries.map(e=>leafHash(e.id,e.sha256)));
  return {schema:'CW_REGISTERED_PROOFS_MANIFEST_V1',hashing:'SHA-256 of exact raw record bytes (no normalization)',merkle_spec:'SHA256(CW_PROOF_LEAF_V1\\0 + id + \\0 + digest bytes); nodes SHA256(CW_PROOF_NODE_V1\\0 + left 32 bytes + right 32 bytes), duplicate last on odd level',root_sha256:levels.at(-1)[0],records:entries.map((e,i)=>({...e,inclusion_proof:inclusion(levels,i)})),authority_created:false,external_certification:false};
}
export function validateManifest(claimed,actual){if(JSON.stringify(claimed)!==JSON.stringify(actual))throw Error('Manifest differs from raw record hashes, verdicts, or Merkle root');return true}
async function main(){const command=process.argv[2]||'verify';const result=await createSnapshot();if(command==='build'){
  const p=path.join(ROOT,'manifest.json');await writeFile(p,JSON.stringify(result,null,2)+'\n');console.log('CREATED '+p);
}else if(command==='verify'){
  const claimed=JSON.parse(await readFile(path.join(ROOT,'manifest.json'),'utf8'));validateManifest(claimed,result);
  for(const e of result.records)if(!verifyInclusion(e.id,e.sha256,e.inclusion_proof,result.root_sha256))throw Error('Merkle inclusion mismatch');
  const scope=Object.fromEntries(result.records.map(x=>[x.id,x.ci_verdict]));
  const receipt={schema:'CW_PROOF_CI_RECEIPT_V1',ci_status:'PASS',what_passed:'local bytes, schema, scoped statuses, Merkle inclusion; NOT third-party certification',manifest_root_sha256:result.root_sha256,checks:scope,source_verification:'UNKNOWN',proof_domain_http_reachability:'UNKNOWN',hardware_attestation:'UNKNOWN'};
  await mkdir(path.join(ROOT,'ci-out'),{recursive:true});await writeFile(path.join(ROOT,'ci-out','verification.json'),JSON.stringify(receipt,null,2)+'\n');console.log(JSON.stringify(receipt));
}else throw Error('Use build or verify')}
if(process.argv[1] && path.resolve(process.argv[1])===fileURLToPath(import.meta.url))main().catch(e=>{console.error('CI-FIRST FAIL:',e.message);process.exitCode=1});
