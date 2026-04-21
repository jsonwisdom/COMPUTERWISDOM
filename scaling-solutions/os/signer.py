#!/usr/bin/env python3
from pathlib import Path
from typing import Dict

from nacl.encoding import HexEncoder
from nacl.exceptions import BadSignatureError
from nacl.signing import SigningKey, VerifyKey

ROOT = Path(__file__).resolve().parents[1]
KEY_DIR = ROOT / ".keys"
PRIVATE_KEY_PATH = KEY_DIR / "ed25519_seed.hex"
PUBLIC_KEY_PATH = KEY_DIR / "ed25519_pub.hex"


def ensure_local_keypair() -> Dict[str, str]:
    KEY_DIR.mkdir(parents=True, exist_ok=True)
    if PRIVATE_KEY_PATH.exists() and PUBLIC_KEY_PATH.exists():
        return {
            "private_key": PRIVATE_KEY_PATH.read_text(encoding="utf-8").strip(),
            "public_key": PUBLIC_KEY_PATH.read_text(encoding="utf-8").strip(),
        }

    signing_key = SigningKey.generate()
    private_key = signing_key.encode(encoder=HexEncoder).decode("utf-8")
    public_key = signing_key.verify_key.encode(encoder=HexEncoder).decode("utf-8")
    PRIVATE_KEY_PATH.write_text(private_key + "\n", encoding="utf-8")
    PUBLIC_KEY_PATH.write_text(public_key + "\n", encoding="utf-8")
    return {"private_key": private_key, "public_key": public_key}


def sign_receipt_hash(receipt_hash: str) -> Dict[str, str]:
    keypair = ensure_local_keypair()
    signing_key = SigningKey(keypair["private_key"], encoder=HexEncoder)
    signature = signing_key.sign(receipt_hash.encode("utf-8")).signature.hex()
    return {
        "signing_scheme": "ed25519",
        "signer": "os.jaywisdom.eth",
        "public_key": keypair["public_key"],
        "signature": signature,
    }


def verify_receipt_hash(receipt_hash: str, signature_bundle: Dict[str, str]) -> bool:
    try:
        if signature_bundle.get("signing_scheme") != "ed25519":
            return False
        verify_key = VerifyKey(signature_bundle["public_key"], encoder=HexEncoder)
        verify_key.verify(receipt_hash.encode("utf-8"), bytes.fromhex(signature_bundle["signature"]))
        return True
    except (BadSignatureError, KeyError, ValueError):
        return False
