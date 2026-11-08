import {readFileSync,writeFileSync} from 'node:fs';
import {runSwarm,verifyReceipt} from './swarm.mjs';
import {canonical} from './contracts.mjs';
const argv=process.argv.slice(2);
if(argv.length<1) {console.error('Usage: node src/cli.mjs <input.json> [--expect PASS|FAIL|UNKNOWN] [--output receipt.json]');process.exit(2)}
const option=(flag)=>{const idx=argv.indexOf(flag);return idx<0?undefined:argv[idx+1]};
const file=argv[0];const input=JSON.parse(readFileSync(file,'utf8'));
const result=await runSwarm(input);
verifyReceipt(result,input);
const bytes=JSON.stringify(result,null,2)+'\n';
if(option('--output')) writeFileSync(option('--output'),bytes,'utf8');
console.log(JSON.stringify({schema:result.schema,case_id:result.case_id,agents:result.agents,verdict:result.verdict,production_verification:result.production_verification,sha256:result.sha256}));
const expected=option('--expect');
if(expected && !['PASS','FAIL','UNKNOWN'].includes(expected)){console.error('BAD_EXPECTED_VERDICT');process.exit(2)}
process.exitCode=expected?Number(result.verdict!==expected):Number(result.verdict==='FAIL');
