#!/usr/bin/env python3
import base64
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
KEY_DIR = ROOT / ".keys"
PRIVATE_KEY_PATH = KEY_DIR / "local_signing_key.txt"
PUBLIC_KEY_PATH = KEY_DIR / "local_signing_key.pub.txt"


def canon(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _derive_public_from_private(private_key: str) -> str:
    return hashlib.sha256(("pub:" + private_key).encode("utf-8")).hexdigest()


def ensure_local_keypair() -> Dict[str, str]:
    KEY_DIR.mkdir(parents=True, exist_ok=True)
    if PRIVATE_KEY_PATH.exists() and PUBLIC_KEY_PATH.exists():
        return {
            "private_key": PRIVATE_KEY_PATH.read_text(encoding="utf-8").strip(),
            "public_key": PUBLIC_KEY_PATH.read_text(encoding="utf-8").strip(),
        }

    seed = base64.b64encode(os.urandom(32)).decode("utf-8")
    public_key = _derive_public_from_private(seed)
    PRIVATE_KEY_PATH.write_text(seed + "\n", encoding="utf-8")
    PUBLIC_KEY_PATH.write_text(public_key + "\n", encoding="utf-8")
    return {"private_key": seed, "public_key": public_key}


def sign_receipt_hash(receipt_hash: str) -> Dict[str, str]:
    # Placeholder local signer. This is NOT Ed25519.
    # It provides deterministic non-production signing until KMS or a real Ed25519 library is wired.
    keypair = ensure_local_keypair()
    private_key = keypair["private_key"]
    public_key = keypair["public_key"]
    signature = hashlib.sha256((private_key + ":" + receipt_hash).encode("utf-8")).hexdigest()
    return {
        "signing_scheme": "local_sha256_placeholder",
        "signer": "os.jaywisdom.eth",
        "public_key": public_key,
        "signature": signature,
    }


def verify_receipt_hash(receipt_hash: str, signature_bundle: Dict[str, str]) -> bool:
    if signature_bundle.get("signing_scheme") != "local_sha256_placeholder":
        return False
    if not PRIVATE_KEY_PATH.exists():
        return False
    private_key = PRIVATE_KEY_PATH.read_text(encoding="utf-8").strip()
    expected = hashlib.sha256((private_key + ":" + receipt_hash).encode("utf-8")).hexdigest()
    return expected == signature_bundle.get("signature")
