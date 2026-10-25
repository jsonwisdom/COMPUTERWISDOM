// Read-only FEC / OpenSecrets / third-source adapters with honest availability reporting.
// Network is OFF unless DD_ENABLE_HTTP=1 AND the adapter's key env var is set. No financial activity.
import { assertValid } from './validate.js';

export const ADAPTERS = {
  FEC: { keyEnv: 'DD_FEC_API_KEY', url: (k) => `https://api.open.fec.gov/v1/candidates/?per_page=1&api_key=${encodeURIComponent(k)}`, operator: 'U.S. Federal Election Commission' },
  OPENSECRETS: { keyEnv: 'DD_OPENSECRETS_API_KEY', url: (k) => `https://www.opensecrets.org/api/?method=getLegislators&id=NJ&output=json&apikey=${encodeURIComponent(k)}`, operator: 'OpenSecrets / Center for Responsive Politics' },
  THIRD_SOURCE: { keyEnv: 'DD_THIRD_SOURCE_URL', url: (u) => u, operator: 'operator-configured third source' },
};

function report(adapter, availability, detail, now) {
  return assertValid('SourceAvailability', { type: 'SourceAvailability', adapter, availability,
    dataLabel: availability === 'AVAILABLE' ? 'LIVE' : 'LIVE_UNAVAILABLE',
    checkedAt: now().toISOString(), liveFinancialActivity: false, detail, AUTHORITY_CREATED: false });
}

export async function checkAvailability(adapter, { env = process.env, fetchImpl = globalThis.fetch, now = () => new Date() } = {}) {
  const a = ADAPTERS[adapter];
  if (!a) throw new Error(`unknown adapter ${adapter}`);
  if (env.DD_ENABLE_HTTP !== '1') return report(adapter, 'NOT_CONFIGURED', 'HTTP disabled (DD_ENABLE_HTTP!=1)', now);
  const key = env[a.keyEnv];
  if (!key) return report(adapter, adapter === 'THIRD_SOURCE' ? 'NOT_CONFIGURED' : 'AUTH_REQUIRED', `${a.keyEnv} not set`, now);
  try {
    const res = await fetchImpl(a.url(key), { method: 'GET', redirect: 'error' });
    if (res.status === 429) return report(adapter, 'RATE_LIMITED', 'HTTP 429', now);
    if (res.status === 401 || res.status === 403) return report(adapter, 'AUTH_REQUIRED', `HTTP ${res.status}`, now);
    if (!res.ok) return report(adapter, 'ERROR', `HTTP ${res.status}`, now);
    // HTTP_200 != CONTENT_VERIFIED: availability only, content not verified here.
    return report(adapter, 'AVAILABLE', `HTTP ${res.status}; content NOT verified`, now);
  } catch (e) {
    return report(adapter, 'ERROR', `fetch failed: ${e.name}`, now);
  }
}
