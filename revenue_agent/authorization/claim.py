from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path

_TASK_ID_RE = re.compile(r"^TASK-[A-F0-9]{32}$")
_DIGEST_RE = re.compile(r"^[a-f0-9]{64}$")


@dataclass(frozen=True)
class ClaimResult:
    status: str
    reason: str = ""


class FileBasedClaimStore:
    """Durable single-use claim gate for one host filesystem."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.root.mkdir(mode=0o700, parents=True, exist_ok=True)

    def claim(self, task_id: str, auth_receipt_digest: str) -> ClaimResult:
        if not isinstance(task_id, str) or not _TASK_ID_RE.fullmatch(task_id):
            return ClaimResult("REJECTED", "INVALID_TASK_ID")
        if not isinstance(auth_receipt_digest, str) or not _DIGEST_RE.fullmatch(
            auth_receipt_digest
        ):
            return ClaimResult("REJECTED", "INVALID_AUTH_RECEIPT_DIGEST")

        path = self.root / f"{task_id}.claim"
        flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        fd = None
        created = False
        try:
            fd = os.open(path, flags, 0o600)
            created = True
            data = auth_receipt_digest.encode("ascii")
            written = 0
            while written < len(data):
                count = os.write(fd, data[written:])
                if count <= 0:
                    raise OSError("short claim write")
                written += count
            os.fsync(fd)
            os.close(fd)
            fd = None
            directory_fd = os.open(self.root, os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
            return ClaimResult("CLAIMED")
        except FileExistsError:
            return ClaimResult("ALREADY_CLAIMED")
        except OSError:
            if fd is not None:
                os.close(fd)
            if created:
                try:
                    path.unlink()
                except FileNotFoundError:
                    pass
            return ClaimResult("REJECTED", "CLAIM_STORE_IO_ERROR")
