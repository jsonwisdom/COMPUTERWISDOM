// Human approval workflow: authenticated (HMAC-SHA256), atomic single-use receipts.
// HUMAN_APPROVAL_RECORDED and CRYPTOGRAPHIC_IDENTITY_VERIFIED are independent states.
// HMAC proves the receipt was issued by this store; it does NOT prove the human's identity.
import { createHmac, randomBytes, timingSafeEqual } from 'node:crypto';
import { digest } from './jcs.js';
import { assertValid } from './validate.js';

export class ApprovalStore {
  #key; #receipts = new Map(); #consumed = new Set(); #now;
  constructor({ key = randomBytes(32), now = () => new Date() } = {}) {
    if (!Buffer.isBuffer(key) || key.length < 32) throw new Error('key must be >=32 bytes');
    this.#key = key; this.#now = now;
  }
  #mac(r) {
    const { mac, consumed, CRYPTOGRAPHIC_IDENTITY_VERIFIED, identityEvidence, ...signed } = r;
    return 'hmac-sha256:' + createHmac('sha256', this.#key).update(digest(signed)).digest('hex');
  }
  record({ subject, approver }) {
    if (!approver) throw new Error('approver required');
    const r = { type: 'ApprovalReceipt', approvalId: randomBytes(16).toString('hex'), subjectDigest: digest(subject),
      approver, issuedAt: this.#now().toISOString(), nonce: randomBytes(16).toString('hex'),
      HUMAN_APPROVAL_RECORDED: true, CRYPTOGRAPHIC_IDENTITY_VERIFIED: false, identityEvidence: null,
      consumed: false, status: 'HOLD', AUTHORITY_CREATED: false, FINAL_AUTHORITY: 'JASON' };
    r.mac = this.#mac(r);
    assertValid('ApprovalReceipt', r);
    this.#receipts.set(r.approvalId, r);
    return structuredClone(r);
  }
  /** Atomic single-use consume. JS runs this synchronously: check-and-set cannot interleave. */
  consume(receipt, subject) {
    const stored = this.#receipts.get(receipt?.approvalId);
    if (!stored) return { ok: false, reason: 'UNKNOWN_APPROVAL' };
    const a = Buffer.from(this.#mac(receipt)), b = Buffer.from(String(receipt.mac));
    if (a.length !== b.length || !timingSafeEqual(a, b)) return { ok: false, reason: 'BAD_MAC' };
    if (digest(subject) !== stored.subjectDigest) return { ok: false, reason: 'SUBJECT_MISMATCH' };
    if (this.#consumed.has(stored.approvalId)) return { ok: false, reason: 'ALREADY_CONSUMED' };
    this.#consumed.add(stored.approvalId);
    stored.consumed = true;
    return { ok: true, receipt: structuredClone(stored), AUTHORITY_CREATED: false };
  }
}
