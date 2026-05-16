#!/usr/bin/env ts-node

import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

type CanonEntry = {
  id: string;
  path: string;
  commit: string;
  file_content_sha256: string;
};

type Receipt = {
  spec: string;
  receipt_id: string;
  receipt_type: string;
  status: string;
  repository_binding: {
    repo: string;
    repo_url: string;
    canonical_branch: string;
    latest_known_commit_before_receipt: string;
  };
  canon_order: string[];
  canon_chain: CanonEntry[];
  declared_scope: {
    covers: string[];
    does_not_cover: string[];
    future_receipts_may_supersede: boolean;
  };
  verifier_assumptions: {
    must_recompute: string[];
    must_trust: string[];
    must_ignore: string[];
    equivalence_rule: string;
  };
  anchor_status: {
    github_committed: boolean;
    onchain_anchored: boolean;
    ens_anchored: boolean;
    eas_anchored: boolean;
    platform_endorsed: boolean;
    global_legitimacy_claimed: boolean;
    rule: string;
  };
};

type VerificationResult = {
  receipt: string;
  verification: "PASS" | "FAIL";
  checked_files: number;
  computed_hashes: Record<string, string>;
  hash_mismatches: string[];
  errors: string[];
  order_valid: boolean;
  scope_valid: boolean;
  anchor_status_valid: boolean;
};

const EXPECTED_ORDER = [
  "COMPUTER_WISDOM_MICROSOFT_BRIEF_V1",
  "REPUTATION_CONTINUITY_SPEC_V1",
  "REPLAY_RECEIPT_SPEC_V1",
  "EXECUTION_CONTINUITY_MODEL_V1",
];

function sha256Utf8(content: string): string {
  return createHash("sha256").update(content, "utf8").digest("hex");
}

function fail(errors: string[], code: string): void {
  errors.push(code);
}

function loadReceipt(path: string): Receipt {
  const raw = readFileSync(path, "utf8");
  return JSON.parse(raw) as Receipt;
}

function arraysEqual(a: string[], b: string[]): boolean {
  return a.length === b.length && a.every((value, index) => value === b[index]);
}

function verify(): VerificationResult {
  const repoRoot = process.cwd();
  const receiptPath = resolve(repoRoot, "receipts/continuity/CANON_CHAIN_RECEIPT_001.json");
  const receipt = loadReceipt(receiptPath);

  const errors: string[] = [];
  const hashMismatches: string[] = [];
  const computedHashes: Record<string, string> = {};

  if (receipt.spec !== "REPLAY_RECEIPT_SPEC_V1") {
    fail(errors, "SPEC_MISMATCH");
  }

  if (receipt.receipt_id !== "CANON_CHAIN_RECEIPT_001") {
    fail(errors, "RECEIPT_ID_MISMATCH");
  }

  const orderValid = arraysEqual(receipt.canon_order, EXPECTED_ORDER);
  if (!orderValid) {
    fail(errors, "ORDER_INVALID");
  }

  const chainIds = receipt.canon_chain.map((entry) => entry.id);
  if (!arraysEqual(chainIds, EXPECTED_ORDER)) {
    fail(errors, "CANON_CHAIN_ORDER_INVALID");
  }

  const scopeValid =
    receipt.declared_scope.does_not_cover.includes("onchain anchoring") &&
    receipt.declared_scope.does_not_cover.includes("Microsoft review or endorsement") &&
    receipt.declared_scope.does_not_cover.includes("global legitimacy or institutional acceptance");

  if (!scopeValid) {
    fail(errors, "SCOPE_BOUNDARY_INVALID");
  }

  const anchorStatusValid =
    receipt.anchor_status.github_committed === true &&
    receipt.anchor_status.onchain_anchored === false &&
    receipt.anchor_status.ens_anchored === false &&
    receipt.anchor_status.eas_anchored === false &&
    receipt.anchor_status.platform_endorsed === false &&
    receipt.anchor_status.global_legitimacy_claimed === false;

  if (!anchorStatusValid) {
    fail(errors, "ANCHOR_STATUS_INVALID");
  }

  for (const entry of receipt.canon_chain) {
    const filePath = resolve(repoRoot, entry.path);
    let content: string;

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
      continue;
    }

    if (entry.file_content_sha256 !== computed) {
      hashMismatches.push(`HASH_MISMATCH:${entry.id}:expected=${entry.file_content_sha256}:observed=${computed}`);
    }
  }

  const verification = errors.length === 0 && hashMismatches.length === 0 ? "PASS" : "FAIL";

  return {
    receipt: "receipts/continuity/CANON_CHAIN_RECEIPT_001.json",
    verification,
    checked_files: Object.keys(computedHashes).length,
    computed_hashes: computedHashes,
    hash_mismatches: hashMismatches,
    errors,
    order_valid: orderValid,
    scope_valid: scopeValid,
    anchor_status_valid: anchorStatusValid,
  };
}

console.log(JSON.stringify(verify(), null, 2));
