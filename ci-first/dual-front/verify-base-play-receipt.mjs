// CI-FIRST independent historical EIP-191 verifier. No signing, no transactions.
// Uses viem; an ERC-1271/6492 contract wallet requires a separate chain verification.
import { recoverMessageAddress } from 'viem'
import { readFile } from 'node:fs/promises'
import { createHash } from 'node:crypto'
export const PC='0x65891F97db01C8fC9F76f4DFE65Bd44F8261f1B0'
export const HIST='0xA380552a27b0a5a2874Ea7AA52CAC09f542002E8'
export const ORIGIN='https://cw-base-play-sign-20261109.jaywisdom44.workers.dev'
export const CHAIN=8453
export function messageFor(r,signer=PC){
return [
'CI-FIRST BASE PLAY NOW - OPERATOR DECLARATION',
'Version: 1',
'Origin: '+ORIGIN,
'Chain ID: 8453 (Base)',
'Signer: '+signer,
'Scope: PLAY NOW | BATCHES | BUILDS',
'Batch pattern: 3, 6, 9 (declaration only)',
'Historical wallet: '+HIST,
'Historical wallet designation: NOT THE FUTURE PLAY DESTINATION',
'Requested current project destination: '+signer,
'Wallet control transferred: NO',
'ENS or Basename records changed: NO',
'Smart-contract authority granted: NO',
'USDC, tokens, money transferred: NO',
'Permissions, approvals or asset custody: NONE',
"Children's data or registration: NONE",
'Meaning: I declare a preferred future Base play/build operator and destination. This signed message is evidence only.',
'Nonce: '+r.nonce,
'Issued At: '+r.issued_at,
'Expires At: '+r.expires_at].join('\n')
}
export async function verifyReceipt(r,signer=PC){
const issues=[]
const gate=(condition,error)=>{if(!condition)issues.push(error)}
const isStr=x=>typeof x==='string'
gate(r?.schema==='ci-first-base-play-supersession-eip191-v1','SCHEMA')
gate(r?.chain_id===CHAIN,'CHAIN')
gate(r?.origin===ORIGIN,'ORIGIN')
gate(isStr(r?.signer_claimed)&&r.signer_claimed.toLowerCase()===signer.toLowerCase(),'CLAIMED_SIGNER')
gate(r?.historical_wallet===HIST,'HISTORICAL_WALLET')
gate(isStr(r?.current_play_destination_requested)&&r.current_play_destination_requested.toLowerCase()===signer.toLowerCase(),'PROPOSED_DESTINATION')
gate(JSON.stringify(r?.batch_pattern)==='[3,6,9]','BATCH')
gate(r?.signature_method==='personal_sign','METHOD')
gate(r?.receipt_status==='SIGNATURE_CAPTURED','CAPTURE_STATUS')
gate(r?.ecdsa_recovery_verified===false,'ORIGINAL_VERIFIER_FLAG')
gate(r?.onchain_change_executed===false&&r?.transfer_executed===false,'NONTRANSACTION_FLAG')
gate(isStr(r?.nonce)&&/^[a-f0-9]{32}$/.test(r.nonce),'NONCE_FORMAT')
gate(isStr(r?.signature)&&/^0x[0-9a-fA-F]{130}$/.test(r.signature),'SIGNATURE_FORMAT')
const t0=Date.parse(r?.issued_at),t1=Date.parse(r?.expires_at),ts=Date.parse(r?.timestamp)
gate(Number.isFinite(t0)&&Number.isFinite(t1)&&t1-t0===600000,'TEN_MINUTE_WINDOW')
gate(Number.isFinite(ts)&&ts>=t0&&ts<=t1,'SIGNATURE_CAPTURE_TIME_WINDOW')
gate(isStr(r?.message)&&r.message===messageFor(r,signer),'EXACT_SIGNED_MESSAGE')
let recovered=null
if(!issues.length){
try{recovered=await recoverMessageAddress({message:r.message,signature:r.signature})}catch(e){issues.push('ECDSA_RECOVERY_ERROR')}
if(recovered&&recovered.toLowerCase()!==signer.toLowerCase())issues.push('ECDSA_RECOVERED_SIGNER_MISMATCH')
}
return {schema:'ci-first-quadruple-onion-verdict-v1',result:issues.length?'FAIL':'PASS',issues,recovered_signer:recovered,expected_signer:signer,chain_id:8453,scope:'HISTORICAL_EIP191_EOA_MESSAGE_ONLY',server_issued_nonce:false,global_single_use_proven:false,erc1271_verified:false,ens_changed:false,usdc_moved:false}
}
if(process.argv[1]&&process.argv[1].endsWith('/verify-base-play-receipt.mjs')){
const file=process.argv[2]
if(!file){console.error('Usage: node verify-base-play-receipt.mjs signed.json');process.exit(2)}
try{const b=await readFile(file);const v=await verifyReceipt(JSON.parse(b.toString('utf8')));v.input_file_sha256=createHash('sha256').update(b).digest('hex');console.log(JSON.stringify(v,null,2));if(v.result!=='PASS')process.exitCode=1}catch(e){console.error('FAIL: '+String(e?.message||e));process.exitCode=1}
}
