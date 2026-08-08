import { validateReceipt } from './schema.js';
import { RendererError } from './errors.js';

const AUTHORITY_FIELD_PATTERN = /^authority(_|$)/i;
const DIGEST_PATTERN = /^[a-f0-9]{64}$/;

function collectAuthorityKeys(value, path = '$', found = []) {
  if (!value || typeof value !== 'object') return found;

  if (Array.isArray(value)) {
    value.forEach((item, index) => collectAuthorityKeys(item, `${path}[${index}]`, found));
    return found;
  }

  for (const [key, child] of Object.entries(value)) {
    const childPath = `${path}.${key}`;
    if (AUTHORITY_FIELD_PATTERN.test(key)) found.push(childPath);
    collectAuthorityKeys(child, childPath, found);
  }

  return found;
}

function deepFreeze(value) {
  if (!value || typeof value !== 'object' || Object.isFrozen(value)) return value;
  Object.freeze(value);
  for (const child of Object.values(value)) deepFreeze(child);
  return value;
}

export function project(receipt) {
  const authorityKeys = collectAuthorityKeys(receipt);
  if (authorityKeys.length > 0) {
    throw new RendererError(
      `Receipt contains prohibited authority field(s): ${authorityKeys.join(', ')}`,
      'AUTHORITY_FIELD_PRESENT',
    );
  }

  if (typeof receipt?.receipt_digest !== 'string' || !DIGEST_PATTERN.test(receipt.receipt_digest)) {
    throw new RendererError('Invalid receipt_digest format', 'DIGEST_MALFORMED');
  }

  validateReceipt(receipt);

  const safeReceipt = structuredClone(receipt);
  const projection = {
    work_order_id: safeReceipt.work_order_id,
    baseline_anchor: safeReceipt.baseline_anchor,
    semantic_validation: safeReceipt.semantic_validation,
    observed_outputs: safeReceipt.observed_outputs,
    evidence_refs: safeReceipt.evidence_refs,
    anomalies: safeReceipt.anomalies,
    receipt_digest: safeReceipt.receipt_digest,
  };

  return deepFreeze(projection);
}
