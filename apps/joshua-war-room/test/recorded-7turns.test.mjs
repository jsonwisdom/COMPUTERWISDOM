import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { verifyReplay } from "../lib/authority.js";

// Original uploaded JSON fixture. File SHA-256 checks the exact bytes.
// walletAuthenticated=true is client-reported metadata, NOT proof of a wallet signature.
const raw = readFileSync(new URL("../evidence/joshua-war-room-replay-7turns-20261116.json", import.meta.url));
const replay = JSON.parse(raw.toString("utf8"));

test("seven-turn uploaded replay exact byte digest", () => {
  assert.equal(createHash("sha256").update(raw).digest("hex"),
    "397ea9f7240523f436c4abf3db2a9e115b833a1a7e658fc3a8f728b8095dada3");
});

test("seven-turn replay independently reproduces game rules", () => {
  const result = verifyReplay(replay);
  assert.equal(result.ok, true, result.reason);
  assert.deepEqual(result.final, {
    turn: 8, defense: 32, trust: 47, intel: 58, points: 110,
    roll: 15, status: "PASS — CIVILIAN SAFETY IMPROVED"
  });
});

test("modified seven-turn score is rejected by the rules", () => {
  const modified = structuredClone(replay);
  modified.state.points = 999;
  assert.equal(verifyReplay(modified).ok, false);
});
