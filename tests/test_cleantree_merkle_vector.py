import csv
import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "synthetic-inventory.csv"
EXPECTED_ROOT = "656020bb502588bf3cd0574a6890950ccec3c5ffd2f2e4551594c8d13e32677a"


def utf8_ordinal_key(row: dict[str, str]) -> bytes:
    return f"{row['repository']}\0{row['relative_path']}".encode("utf-8")


def leaf(row: dict[str, str]) -> bytes:
    canonical = "\n".join(
        (
            "CLEANTREE_LEAF_V1",
            row["repository"],
            row["commit_sha"],
            row["relative_path"],
            row["bytes"],
            row["sha256"].lower(),
            row["suggested_classification"],
            row["rule_ids"],
            row["content_scan_state"],
        )
    )
    return hashlib.sha256(canonical.encode("utf-8")).digest()


def merkle_root(nodes: list[bytes]) -> str:
    if not nodes:
        return hashlib.sha256(b"CLEANTREE_EMPTY_V1").hexdigest()
    while len(nodes) > 1:
        if len(nodes) % 2:
            nodes.append(nodes[-1])
        nodes = [
            hashlib.sha256(nodes[index] + nodes[index + 1]).digest()
            for index in range(0, len(nodes), 2)
        ]
    return nodes[0].hex()


class MerkleVectorTests(unittest.TestCase):
    def test_fixture_uses_utf8_ordinal_order_and_expected_root(self):
        with FIXTURE.open(newline="", encoding="utf-8") as handle:
            rows = sorted(csv.DictReader(handle), key=utf8_ordinal_key)
        self.assertEqual(
            [row["relative_path"] for row in rows],
            ["README.md", "credentials.env", "internal/router.py"],
        )
        self.assertEqual(merkle_root([leaf(row) for row in rows]), EXPECTED_ROOT)

    def test_windows_case_insensitive_order_reproduces_rejected_root(self):
        with FIXTURE.open(newline="", encoding="utf-8") as handle:
            rows = sorted(
                csv.DictReader(handle),
                key=lambda row: (
                    row["repository"].lower(),
                    row["relative_path"].lower(),
                ),
            )
        rejected = "b5aff300e2fa84af1009df2ff97e13c395e718e7767bf2878cf281d8e7630d52"
        self.assertEqual(merkle_root([leaf(row) for row in rows]), rejected)
        self.assertNotEqual(rejected, EXPECTED_ROOT)


if __name__ == "__main__":
    unittest.main()
