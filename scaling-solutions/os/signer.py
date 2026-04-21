#!/usr/bin/env python3
import os
from pathlib import Path
from typing import Dict

from nacl.encoding import HexEncoder
from nacl.exceptions import BadSignatureError
from nacl.signing import SigningKey, VerifyKey

ROOT = Path(__file__).resolve().parents[1]
KEY_DIR = ROOT / ".keys"
PRIVATE_KEY_PATH = KEY_DIR / "ed25519_seed.hex"
PUBLIC_KEY_PATH = KEY_DIR / "ed25519_pub.hex"
SIGNER_MODE = os.getenv("SIGNER_MODE", "local")


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


def _ed25519_sign(receipt_hash: str) -> Dict[str, str]:
    keypair = ensure_local_keypair()
    signing_key = SigningKey(keypair["private_key"], encoder=HexEncoder)
    signature = signing_key.sign(receipt_hash.encode("utf-8")).signature.hex()
    return {
        "signing_scheme": "ed25519",
        "signer": "os.jaywisdom.eth",
        "public_key": keypair["public_key"],
        "signature": signature,
    }


def _kms_sign(receipt_hash: str) -> Dict[str, str]:
    from google.cloud import kms_v1

    key_version_name = os.environ["KMS_KEY_VERSION"]
    public_key_hex = os.environ["KMS_PUBLIC_KEY_HEX"]

    client = kms_v1.KeyManagementServiceClient()
    digest = bytes.fromhex(receipt_hash)
    response = client.asymmetric_sign(
        request={
            "name": key_version_name,
            "digest": {"sha256": digest}
        }
    )
    return {
        "signing_scheme": "ecdsa_kms",
        "signer": "os.jaywisdom.eth",
        "public_key": public_key_hex,
        "signature": response.signature.hex(),
        "kms_key_version": key_version_name,
    }


def sign_receipt_hash(receipt_hash: str) -> Dict[str, str]:
    if SIGNER_MODE == "kms":
        return _kms_sign(receipt_hash)
    return _ed25519_sign(receipt_hash)


def verify_receipt_hash(receipt_hash: str, signature_bundle: Dict[str, str]) -> bool:
    try:
        scheme = signature_bundle.get("signing_scheme")
        if scheme == "ed25519":
            verify_key = VerifyKey(signature_bundle["public_key"], encoder=HexEncoder)
            verify_key.verify(receipt_hash.encode("utf-8"), bytes.fromhex(signature_bundle["signature"]))
            return True

        if scheme == "ecdsa_kms":
            from cryptography.exceptions import InvalidSignature
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.asymmetric import ec
            from cryptography.hazmat.primitives.serialization import load_der_public_key

            public_key = load_der_public_key(bytes.fromhex(signature_bundle["public_key"]))
            public_key.verify(
                bytes.fromhex(signature_bundle["signature"]),
                bytes.fromhex(receipt_hash),
                ec.ECDSA(hashes.SHA256())
            )
            return True

        return False
    except (BadSignatureError, KeyError, ValueError, Exception):
        return False
