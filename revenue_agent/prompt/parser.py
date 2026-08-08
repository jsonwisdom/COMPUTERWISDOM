from typing import Any, Dict


REQUIRED_SECTIONS = ("answer", "summary", "confidence")

SECTION_HEADERS = {
    "[MODEL ANSWER]": "answer",
    "[EVIDENCE / REASONING SUMMARY]": "summary",
    "[CONFIDENCE": "confidence",
}


class ParseError(ValueError):
    """Raised when model output violates the spine contract."""


def _inline_content(line: str, header: str, section: str) -> str:
    """Return content following a recognized section header."""
    if section != "confidence":
        return line[len(header) :].strip()

    closing_bracket = line.find("]", len(header))
    if closing_bracket == -1:
        return ""
    return line[closing_bracket + 1 :].strip()


def parse_model_response(raw_output: str, model_id: str) -> Dict[str, Any]:
    """Extract and validate deterministic fields from a model response."""
    if not isinstance(raw_output, str) or not raw_output.strip():
        raise ParseError(f"Model {model_id}: empty or non-string output")

    sections: Dict[str, list] = {}
    current_section = None

    for line in raw_output.split("\n"):
        stripped = line.strip()

        matched = next(
            (
                (header, key)
                for header, key in SECTION_HEADERS.items()
                if stripped.startswith(header)
            ),
            None,
        )
        if matched:
            header, current_section = matched
            inline = _inline_content(stripped, header, current_section)
            if inline:
                sections.setdefault(current_section, []).append(inline)
            continue

        if current_section and stripped:
            sections.setdefault(current_section, []).append(stripped)

    missing = [
        section
        for section in REQUIRED_SECTIONS
        if section not in sections or not sections[section]
    ]
    if missing:
        raise ParseError(
            f"Model {model_id}: missing or empty required sections: {missing}"
        )

    conf_raw = " ".join(sections["confidence"]).strip()
    try:
        confidence = float(conf_raw)
    except (TypeError, ValueError):
        raise ParseError(
            f"Model {model_id}: invalid confidence format '{conf_raw}'"
        )
    if not 0.0 <= confidence <= 1.0:
        raise ParseError(
            f"Model {model_id}: confidence {confidence} out of range [0.0, 1.0]"
        )

    return {
        "answer": "\n".join(sections["answer"]).strip(),
        "summary": "\n".join(sections["summary"]).strip(),
        "confidence": confidence,
        "model_id": model_id,
    }
