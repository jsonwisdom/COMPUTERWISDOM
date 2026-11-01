import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { DatabaseSync } from 'node:sqlite';
import { Wallet, TypedDataEncoder } from 'ethers';
import { CONTRACT, __testing as cryptoTesting } from './verify-base-signatures.mjs';
import { __testing as ledgerTesting, reserveBaseBatch } from './replay-ledger.mjs';

// Public deterministic TEST ONLY key. No real private key, live wallet or funds.
const TEST_SIGNER=new Wallet('0x'+'77'.repeat(32));
const WRONG_SIGNER=new Wallet('0x'+'88'.repeat(32));
const NOW=1793560818;
const DOMAIN_FIELDS=[
  {name:'name',type:'string'},{name:'version',type:'string'},
  {name:'chainId',type:'uint256'},{name:'salt',type:'bytes32'}
];
const CONTROL_FIELDS=[
  {name:'origin',type:'string'},{name:'wallet',type:'address'},
  {name:'purpose',type:'string'},{name:'nonce',type:'bytes32'},
  {name:'issuedAt',type:'uint256'},{name:'expiresAt',type:'uint256'},
  {name:'policy',type:'string'}
];
async function signedProof(n){
  const domain={name:CONTRACT.name,version:CONTRACT.version,
    chainId:CONTRACT.chainId,salt:CONTRACT.salt};
  const message={origin:CONTRACT.origin,wallet:TEST_SIGNER.address,
    purpose:CONTRACT.purpose,
    nonce:'0x'+n.toString(16).padStart(64,'0'),
    issuedAt:NOW-10,expiresAt:NOW+290,policy:CONTRACT.policy};
  const signature=await TEST_SIGNER.signTypedData(domain,{WalletControl:CONTROL_FIELDS},message);
  return {expectedSigner:TEST_SIGNER.address,typedData:{
    types:{EIP712Domain:DOMAIN_FIELDS,WalletControl:CONTROL_FIELDS},
    primaryType:'WalletControl',domain,message},signature};
}
function counts(file){
  const db=new DatabaseSync(file);
  try{
    return {
      batches:Number(db.prepare('SELECT COUNT(*) n FROM replay_batches').get().n),
      nonces:Number(db.prepare('SELECT COUNT(*) n FROM consumed_nonces').get().n)
    };
  }finally{db.close();}
}
const reserve=(p,dbPath)=>ledgerTesting.reserveSyntheticSignedBatch(p,{
  dbPath,nowSec:NOW,testSignerSet:[TEST_SIGNER.address]
});

test('REPLAY007 §4: true EIP712 verification precedes atomic durable SQLite replay prevention',async()=>{
  const dir=mkdtempSync(join(tmpdir(),'coinbasekid-007-realcrypto-'));
  const file=join(dir,'nonces.sqlite');
  try{
    const good=await signedProof(1);
    const typedDataDigest=TypedDataEncoder.hash(good.typedData.domain,
      {WalletControl:CONTROL_FIELDS},good.typedData.message).toLowerCase();

    // 1. Genuine EIP-712 recovery, exact Base domain and an allowlisted
    // synthetic signer. NOT the production account's private key.
    const verified=cryptoTesting.verifyBaseProofBatch([good],{
      nowSec:NOW,testSignerSet:[TEST_SIGNER.address]});
    assert.equal(verified.status,'CANDIDATE_ROOT_READY');
    assert.equal(verified.items[0].digest,typedDataDigest);
    assert.equal(existsSync(file),false);

    // 2. The identical real cryptographic verifier runs inside the reservation
    // entrypoint; all rows commit in one SQLite BEGIN IMMEDIATE transaction.
    const accepted=reserve([good],file);
    assert.equal(accepted.status,'LOCAL_CANDIDATE_RESERVED');
    assert.equal(accepted.root,verified.root);
    assert.deepEqual(counts(file),{batches:1,nonces:1});
    const db=new DatabaseSync(file);
    try{
      const row=db.prepare('SELECT chain_id,signer,nonce,typed_data_digest,batch_root FROM consumed_nonces').get();
      assert.equal(row.chain_id,8453);
      assert.equal(row.signer,TEST_SIGNER.address.toLowerCase());
      assert.equal(row.nonce,good.typedData.message.nonce);
      assert.equal(row.typed_data_digest,typedDataDigest);
      assert.equal(row.batch_root,verified.root);
      const batch=db.prepare('SELECT root,policy_version,signer_set_version,item_count FROM replay_batches').get();
      assert.equal(batch.root,verified.root);
      assert.equal(batch.item_count,1);
      assert.equal(batch.policy_version,CONTRACT.policyVersion);
    }finally{db.close();}

    // 3. A second submission of precisely the same real signature is replay.
    const replay=reserve([good],file);
    assert.equal(replay.status,'HOLD');
    assert.equal(replay.reason,'NONCE_REPLAY');
    assert.deepEqual(counts(file),{batches:1,nonces:1});

    // 4. New nonce, tampered cryptographic signer. NO database side effect.
    const invalid=await signedProof(2);
    invalid.signature=await WRONG_SIGNER.signTypedData(
      invalid.typedData.domain,{WalletControl:CONTROL_FIELDS},
      invalid.typedData.message);
    const before=counts(file);
    const rejected=reserve([invalid],file);
    assert.equal(rejected.status,'HOLD');
    assert.equal(rejected.reason,'PROOF_INVALID');
    assert.deepEqual(counts(file),before);
    const candidate=cryptoTesting.verifyBaseProofBatch([invalid],{
      nowSec:NOW,testSignerSet:[TEST_SIGNER.address]});
    assert.equal(candidate.status,'HOLD');
    assert.equal(candidate.items[0].reason,'INVALID_RECOVERED_SIGNER');
    // Stronger ordering guard: for a fresh path, a cryptographically invalid
    // proof must not even OPEN SQLite (no file, no WAL, no lock acquisition).
    const unopened=join(dir,'invalid-must-not-open.sqlite');
    assert.equal(existsSync(unopened),false);
    const unopenedResult=reserve([invalid],unopened);
    assert.equal(unopenedResult.status,'HOLD');
    assert.equal(unopenedResult.reason,'PROOF_INVALID');
    assert.equal(existsSync(unopened),false);
    assert.equal(existsSync(unopened+'-wal'),false);
    assert.equal(existsSync(unopened+'-shm'),false);

    // 5. Second independent SQLite connection. Same proof remains rejected,
    // and an attempted direct INSERT with a different digest demonstrates that
    // SQLite's composite PRIMARY KEY itself enforces replay prevention.
    const second=new DatabaseSync(file);
    try{
      assert.equal(second.prepare('SELECT COUNT(*) n FROM consumed_nonces').get().n,1);
      const again=reserve([good],file);
      assert.equal(again.status,'HOLD');
      assert.equal(again.reason,'NONCE_REPLAY');
      assert.throws(()=>second.prepare(
        'INSERT INTO consumed_nonces(chain_id,signer,nonce,typed_data_digest,batch_root) VALUES(?,?,?,?,?)'
      ).run(8453,TEST_SIGNER.address.toLowerCase(),
        good.typedData.message.nonce,'0x'+'22'.repeat(32),verified.root),
        /UNIQUE constraint failed|constraint failed/i);
    }finally{second.close();}
    assert.deepEqual(counts(file),{batches:1,nonces:1});

    // A fresh legitimate proof still reserves; failed proof never poisoned it.
    const fresh=await signedProof(2);
    const freshAccepted=reserve([fresh],file);
    assert.equal(freshAccepted.status,'LOCAL_CANDIDATE_RESERVED');
    assert.deepEqual(counts(file),{batches:2,nonces:2});

    // Production entry point does NOT authorize the synthetic signer.
    const prodPath=join(dir,'production-isolated.sqlite');
    const untrusted=reserveBaseBatch([good],{dbPath:prodPath,nowSec:NOW});
    assert.equal(untrusted.status,'HOLD');
    assert.equal(untrusted.reason,'PROOF_INVALID');
    assert.equal(existsSync(prodPath),false);

    console.log('REPLAY007_INTEGRATION '+JSON.stringify({
      chain:8453,cryptographicSignature:'SYNTHETIC_EIP712_RECOVERY_PASS',
      firstReservation:'LOCAL_CANDIDATE_RESERVED',
      exactDigestRecomputed:true,nonceReplay:'HOLD_NONCE_REPLAY',
      tamperedSignature:'HOLD_PROOF_INVALID_NO_DB_WRITE',
      secondConnection:'HOLD_NONCE_REPLAY',
      sqliteUniqueConstraint:'ENFORCED',validFreshNonce:'RESERVED',
      productionSyntheticSigner:'REJECTED',
      finalCounts:{batches:2,nonces:2},fundsMoved:false
    }));
  }finally{rmSync(dir,{recursive:true,force:true});}
});
