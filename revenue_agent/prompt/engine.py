from typing import List


def _normalize_items(items: List[str]) -> List[str]:
    """Deduplicate, strip, remove empties, sort canonically."""
    return sorted({i.strip() for i in items if i.strip()})


def build_canonical_prompt(
    question: str,
    known_facts: List[str],
    unknowns: List[str],
    constraints: List[str],
) -> str:
    """Deterministic prompt construction. Same inputs -> identical bytes."""
    sections = [
        "[ROOT]",
        f"[QUESTION]\n{question.strip()}",
        "[KNOWN FACTS]\n" + "\n".join(f"- {f}" for f in _normalize_items(known_facts)),
        "[UNKNOWNS]\n" + "\n".join(f"- {u}" for u in _normalize_items(unknowns)),
        "[CONSTRAINTS]\n" + "\n".join(f"- {c}" for c in _normalize_items(constraints)),
        "[INSTRUCTIONS]\nProvide your answer below. Then provide evidence/reasoning summary. Finally state confidence as float 0-1.",
        "[MODEL ANSWER]",
    ]
    return "\n\n".join(sections)
