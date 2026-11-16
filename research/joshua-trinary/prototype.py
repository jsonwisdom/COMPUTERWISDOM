"""CW-JOSHUA-TRINARY-001 — civilian fictional game, not an operational model."""
from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Literal

Status = Literal["PASS", "FAIL", "UNKNOWN"]
Action = Literal["notify", "inquire", "silence"]

@dataclass
class Player:
    name: str
    credibility: float = .5
    transparency: float = .5
    timeliness: float = .5
    def score(self) -> float:
        return .40*self.credibility + .35*self.transparency + .25*self.timeliness

def canonical_bytes(value: object) -> bytes:
    """Local Python encoding only; NOT advertised as cross-language canonical JSON."""
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")

def digest(record: object) -> str:
    return sha256(canonical_bytes(record)).hexdigest()

def verify_notification(record: dict | None, independent_expected_hash: str | None) -> Status:
    if record is None or independent_expected_hash is None:
        return "UNKNOWN"
    return "PASS" if digest(record) == independent_expected_hash else "FAIL"

def escalation_flag(perceived_hostility: float, credibility: float, action: Action) -> bool:
    if not 0 <= perceived_hostility <= 1: raise ValueError("hostility outside fictional range")
    return perceived_hostility > credibility and action != "notify"

def step(players: dict[str, Player], actions: dict[str, Action],
         hostility: dict[str, float], records: dict[str, dict | None],
         independent_hashes: dict[str, str | None]) -> dict:
    """Produces only proposed simulation outcomes; NEVER grants human approval."""
    results = {}
    for name, player in players.items():
        act = actions[name]
        if act not in ("notify","inquire","silence"): raise ValueError("invalid action")
        status: Status = "UNKNOWN"
        if act == "notify":
            status = verify_notification(records.get(name), independent_hashes.get(name))
            if status == "PASS":
                player.credibility = min(1., player.credibility + .08)
                player.timeliness = min(1., player.timeliness + .05)
            elif status == "FAIL":
                player.credibility = max(0., player.credibility - .12)
        elif act == "silence":
            player.credibility = max(0., player.credibility - .06)
        # Inquire alone does not prove transparency.
        flag = escalation_flag(hostility[name],player.credibility,act)
        results[name] = {"action":act,"evidence_status":status,
                         "score":player.score(),"flag_pending_human_review":flag}
    return results

def manifest(records: list[dict]) -> dict:
    entries = [{"entry_id":e.get("entry_id"),"content_hash":digest(e),"record":e}
               for e in records]
    return {"project_id":"CW-JOSHUA-TRINARY-001",
            "hash_algorithm":"SHA-256",
            "entries":entries,"manifest_hash":digest(entries),
            "human_signature":None,"circuit_status":"UNKNOWN"}

if __name__ == "__main__":
    players={name:Player(name) for name in "ABC"}
    print(json.dumps(step(players,{"A":"notify","B":"inquire","C":"notify"},
         {"A":.4,"B":.6,"C":.5},
         {"A":{"type":"hotline_test","msg":"test"},"B":None,"C":None},
         {"A":None,"B":None,"C":None}),indent=2))
