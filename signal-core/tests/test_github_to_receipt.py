from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cli.receipts import verify_receipt
from examples.github_to_receipt import generate_receipt


def test_github_example_generates_verifiable_receipt(tmp_path):
    out = tmp_path / 'sealed_receipt.json'
    receipt = generate_receipt('jsonwisdom/COMPUTERWISDOM', 386, str(out))
    assert receipt['confidence']['authority'] == 'NONE'
    assert out.exists()
    assert verify_receipt(str(out)) == 0
