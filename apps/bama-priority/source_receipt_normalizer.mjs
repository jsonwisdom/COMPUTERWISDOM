const SOURCE_CLASSES = new Set(["UA_OFFICIAL", "NEWS", "OPINION"]);
const SHA256 = /^[a-f0-9]{64}$/;

export function normalizeSourceReceipt(input) {
  if (!input || typeof input !== "object" || Array.isArray(input)) {
    throw new TypeError("receipt must be an object");
  }

  const signal = String(input.signal ?? "").trim();
  if (!signal) throw new Error("signal is required");

  const observedAt = String(input.observed_at ?? "").trim();
  if (!observedAt || Number.isNaN(Date.parse(observedAt))) {
    throw new Error("observed_at must be an ISO-8601 date-time");
  }

  const sourceUrl = String(input.source_url ?? "").trim();
  let parsed;
  try {
    parsed = new URL(sourceUrl);
  } catch {
    throw new Error("source_url must be a valid URL");
  }
  if (parsed.protocol !== "https:") {
    throw new Error("source_url must use https");
  }

  const sourceClass = String(input.source_class ?? "").trim();
  if (!SOURCE_CLASSES.has(sourceClass)) {
    throw new Error("source_class must be UA_OFFICIAL, NEWS, or OPINION");
  }

  const contentSha256 = input.content_sha256 ?? null;
  if (contentSha256 !== null && !SHA256.test(contentSha256)) {
    throw new Error("content_sha256 must be null or 64 lowercase hex characters");
  }

  if (input.claim_state !== undefined && input.claim_state !== "HOLD") {
    throw new Error("claim_state is fail-closed at HOLD");
  }
  if (input.authority_created !== undefined && input.authority_created !== false) {
    throw new Error("authority_created must remain false");
  }

  return Object.freeze({
    signal,
    observed_at: new Date(observedAt).toISOString(),
    source_url: sourceUrl,
    source_class: sourceClass,
    content_sha256: contentSha256,
    claim_state: "HOLD",
    authority_created: false
  });
}
