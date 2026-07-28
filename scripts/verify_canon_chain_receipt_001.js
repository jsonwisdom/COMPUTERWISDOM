#!/usr/bin/env node

const { createHash } = require("node:crypto");
const { readFileSync } = require("node:fs");
const { resolve } = require("node:path");

const EXPECTED_ORDER = [
  "COMPUTER_WISDOM_MICROSOFT_BRIEF_V1",
  "REPUTATION_CONTINUITY_SPEC_V1",
  "REPLAY_RECEIPT_SPEC_V1",
  "EXECUTION_CONTINUITY_MODEL_V1",
];

function sha256Utf8(content) {
  return createHash("sha256").update(content, "utf8").digest("hex");
}

function arraysEqual(a, b) {
  return Array.isArray(a) && Array.isArray(b) && a.length === b.length && a.every((value, index) => value === b[index]);
}

function fail(errors, code) {
  errors.push(code);
}

function verify() {
  const repoRoot = process.cwd();
  const receiptPath = resolve(repoRoot, "receipts/continuity/CANON_CHAIN_RECEIPT_001.json");
  const receipt = JSON.parse(readFileSync(receiptPath, "utf8"));

  const errors = [];
  const hashMismatches = [];
  const computedHashes = {};

  if (receipt.spec !== "REPLAY_RECEIPT_SPEC_V1") fail(errors, "SPEC_MISMATCH");
  if (receipt.receipt_id !== "CANON_CHAIN_RECEIPT_001") fail(errors, "RECEIPT_ID_MISMATCH");

  const orderValid = arraysEqual(receipt.canon_order, EXPECTED_ORDER);
  if (!orderValid) fail(errors, "ORDER_INVALID");

  const chainIds = Array.isArray(receipt.canon_chain) ? receipt.canon_chain.map((entry) => entry.id) : [];
  if (!arraysEqual(chainIds, EXPECTED_ORDER)) fail(errors, "CANON_CHAIN_ORDER_INVALID");

  const doesNotCover = receipt.declared_scope && Array.isArray(receipt.declared_scope.does_not_cover)
    ? receipt.declared_scope.does_not_cover
    : [];
  const scopeValid =
    doesNotCover.includes("onchain anchoring") &&
    doesNotCover.includes("Microsoft review or endorsement") &&
    doesNotCover.includes("global legitimacy or institutional acceptance");
  if (!scopeValid) fail(errors, "SCOPE_BOUNDARY_INVALID");

  const anchor = receipt.anchor_status || {};
  const anchorStatusValid =
    anchor.github_committed === true &&
    anchor.onchain_anchored === false &&
    anchor.ens_anchored === false &&
    anchor.eas_anchored === false &&
    anchor.platform_endorsed === false &&
    anchor.global_legitimacy_claimed === false;
  if (!anchorStatusValid) fail(errors, "ANCHOR_STATUS_INVALID");

  for (const entry of Array.isArray(receipt.canon_chain) ? receipt.canon_chain : []) {
    const filePath = resolve(repoRoot, entry.path);
    let content;
    try {
      content = readFileSync(filePath, "utf8");
    } catch {
      fail(errors, `MISSING_ARTIFACT:${entry.id}`);
      continue;
    }

    const computed = sha256Utf8(content);
    computedHashes[entry.id] = computed;

    if (entry.file_content_sha256 === "PENDING_VERIFIER_RECOMPUTATION") {
      hashMismatches.push(`PENDING_HASH:${entry.id}:${computed}`);
    } else if (entry.file_content_sha256 !== computed) {
      hashMismatches.push(`HASH_MISMATCH:${entry.id}:expected=${entry.file_content_sha256}:observed=${computed}`);
    }
  }

  return {
    receipt: "receipts/continuity/CANON_CHAIN_RECEIPT_001.json",
    verification: errors.length === 0 && hashMismatches.length === 0 ? "PASS" : "FAIL",
    checked_files: Object.keys(computedHashes).length,
    computed_hashes: computedHashes,
    hash_mismatches: hashMismatches,
    errors,
    order_valid: orderValid,
    scope_valid: scopeValid,
    anchor_status_valid: anchorStatusValid,
  };
}

try {
  const result = verify();
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  if (result.verification !== "PASS") process.exitCode = 1;
} catch (error) {
  const message = error instanceof Error ? error.message : String(error);
  const fatalResult = {
    receipt: "receipts/continuity/CANON_CHAIN_RECEIPT_001.json",
    verification: "FAIL",
    checked_files: 0,
    computed_hashes: {},
    hash_mismatches: [],
    errors: [`VERIFIER_FATAL:${message}`],
    order_valid: false,
    scope_valid: false,
    anchor_status_valid: false,
  };
  process.stdout.write(`${JSON.stringify(fatalResult, null, 2)}\n`);
  process.exitCode = 1;
}
