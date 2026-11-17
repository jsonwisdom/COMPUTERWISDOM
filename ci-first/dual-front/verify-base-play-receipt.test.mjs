// Synthetic fixture key ONLY: not Jason, not a production wallet, not an onchain transaction.
import {test} from 'node:test'
import assert from 'node:assert/strict'
import {privateKeyToAccount} from 'viem/accounts'
import {messageFor,verifyReceipt,HIST,ORIGIN} from './verify-base-play-receipt.mjs'
const account=privateKeyToAccount('0x'+'11'.repeat(32))
async function sample(){
const r={schema:'ci-first-base-play-supersession-eip191-v1',timestamp:'2026-11-09T15:00:30.000Z',origin:ORIGIN,chain_id:8453,signature_method:'personal_sign',signer_claimed:account.address,historical_wallet:HIST,current_play_destination_requested:account.address,batch_pattern:[3,6,9],nonce:'ab'.repeat(16),issued_at:'2026-11-09T15:00:00.000Z',expires_at:'2026-11-09T15:10:00.000Z',receipt_status:'SIGNATURE_CAPTURED',ecdsa_recovery_verified:false,onchain_change_executed:false,transfer_executed:false}
r.message=messageFor(r,account.address);r.signature=await account.signMessage({message:r.message});return r
}
test('valid synthetic signature recovery (not Jason)',async()=>{const r=await sample();const x=await verifyReceipt(r,account.address);assert.equal(x.result,'PASS');assert.equal(x.recovered_signer.toLowerCase(),account.address.toLowerCase());assert.equal(x.global_single_use_proven,false)})
test('synthetic signature cannot verify as PC signer',async()=>{const r=await sample();assert.equal((await verifyReceipt(r)).result,'FAIL')})
const errors=[
['different chain',r=>r.chain_id=1],
['different origin',r=>r.origin='https://attacker.example'],
['tampered message',r=>r.message+=' tamper'],
['tampered nonce',r=>r.nonce='ff'.repeat(16)],
['wrong signature',r=>r.signature='0x'+'00'.repeat(65)],
['bad capture timestamp',r=>r.timestamp='2026-11-09T15:20:00.000Z'],
['bad expiry',r=>r.expires_at='2026-11-09T16:10:00.000Z'],
['unexpected spend claim',r=>r.transfer_executed=true],
['wrong historical wallet',r=>r.historical_wallet=account.address]
]
for(const [title,change] of errors)test('reject '+title,async()=>{const r=await sample();change(r);assert.equal((await verifyReceipt(r,account.address)).result,'FAIL')})
