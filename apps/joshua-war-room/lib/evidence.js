import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { isDeepStrictEqual } from "node:util";
import { verifyReplay } from "./authority.js";

// Pin the exact uploaded bytes, not just a claimed score or client label.
export const FIXTURE_SHA256 = "397ea9f7240523f436c4abf3db2a9e115b833a1a7e658fc3a8f728b8095dada3";
export const FIXTURE_SOURCE = "archived-seven-turn";
export const LOCAL_SOURCE = "browser-local";
const fixtureUrl = new URL("../evidence/joshua-war-room-replay-7turns-20261116.json", import.meta.url);
export const sha256 = value => createHash("sha256").update(value).digest("hex");
export function readPinnedFixture() {
  const bytes = readFileSync(fixtureUrl);
  if (sha256(bytes) !== FIXTURE_SHA256) throw Error("Pinned fixture byte integrity failure");
  return bytes;
}
export function validateReplaySelection(replay, source, sourceDigest) {
  if (![FIXTURE_SOURCE, LOCAL_SOURCE].includes(source) || !/^[0-9a-f]{64}$/.test(sourceDigest || ""))
    return {ok:false,reason:"An explicit source and SHA-256 are required"};
  const rules = verifyReplay(replay);
  if (!rules.ok) return {ok:false,reason:rules.reason};
  try {
    const digest = source === FIXTURE_SOURCE
      ? FIXTURE_SHA256
      : sha256(JSON.stringify(replay));
    if (source === FIXTURE_SOURCE && !isDeepStrictEqual(replay, JSON.parse(readPinnedFixture().toString("utf8"))))
      return {ok:false,reason:"Selected replay differs from the pinned archive"};
    if (digest !== sourceDigest) return {ok:false,reason:"Selected source digest mismatch"};
    return {ok:true,source,sourceDigest:digest,rules};
  } catch {
    return {ok:false,reason:"Pinned fixture unavailable or integrity check failed"};
  }
}
