from __future__ import annotations

from dataclasses import dataclass, asdict
import random


AUTHORITY_GATES = {
    1: "CONSTITUTION",
    2: "STATUTE",
    3: "APPROPRIATION",
    4: "EXECUTIVE_INSTRUMENT",
    5: "AGENCY_IMPLEMENTATION",
    6: "FOREIGN_AFFAIRS_OR_MILITARY_AUTHORITY",
    7: "JUDICIAL_REVIEW",
    8: "CONGRESSIONAL_OR_INSPECTOR_OVERSIGHT",
}


@dataclass(frozen=True)
class PresidentialDiceRun:
    seed: int
    d6: int
    d20: int
    d8: int
    x: float
    h: float
    a: int
    k: int
    score: float
    authority_gate: str

    def receipt(self) -> dict:
        return asdict(self)


def friction_from_d6(roll: int) -> int:
    if not 1 <= roll <= 6:
        raise ValueError("d6 roll must be in 1..6")
    return (roll + 1) // 2


def calculate_outcome(a: int, x: float, h: float, k: int) -> float:
    return a * (x - h) ** 2 + k


def run_presidential_dice(*, seed: int, x: float, h: float) -> PresidentialDiceRun:
    rng = random.Random(seed)
    d6 = rng.randint(1, 6)
    d20 = rng.randint(1, 20)
    d8 = rng.randint(1, 8)
    a = friction_from_d6(d6)
    score = calculate_outcome(a=a, x=x, h=h, k=d20)
    return PresidentialDiceRun(
        seed=seed,
        d6=d6,
        d20=d20,
        d8=d8,
        x=x,
        h=h,
        a=a,
        k=d20,
        score=score,
        authority_gate=AUTHORITY_GATES[d8],
    )


if __name__ == "__main__":
    run = run_presidential_dice(seed=20260819, x=7, h=5)
    print(run.receipt())
