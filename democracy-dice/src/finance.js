// Independent finance provenance. Records provenance only: liveSpend=false, walletSigning=false, always.
import { assertValid } from './validate.js';

export function buildProvenance({ subject, claims, sources, basis }) {
  const ops = new Set(sources.map((s) => s.operator)).size;
  const live = sources.length > 0 && sources.every((s) => s.availability === 'AVAILABLE' && s.retrievedDigest);
  return assertValid('FinanceProvenance', {
    type: 'FinanceProvenance', subject, claims, sources,
    independence: { declared: ops >= 2, distinctOperators: ops, basis: basis ?? 'distinct operators of record' },
    liveSpend: false, walletSigning: false,
    dataLabel: live ? 'LIVE' : 'LIVE_UNAVAILABLE', AUTHORITY_CREATED: false,
  });
}
