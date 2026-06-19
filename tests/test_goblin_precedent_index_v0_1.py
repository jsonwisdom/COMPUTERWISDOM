#!/usr/bin/env python3
"""Test suite for GOBLIN_PRECEDENT_INDEX_V0_1.md."""

import re
from pathlib import Path

import pytest

INDEX_PATH = Path("docs/GOBLIN_PRECEDENT_INDEX_V0_1.md")


def test_index_exists():
    assert INDEX_PATH.exists(), "Index file missing"


def test_all_goblins_present():
    content = INDEX_PATH.read_text()
    for i in range(1, 11):
        gc_id = f"GC-{i:03d}"
        assert gc_id in content, f"{gc_id} not found in index"


def test_authority_false():
    content = INDEX_PATH.read_text()
    assert content.count("Authority: false") >= 2 or content.count("authority: false") >= 2


def test_trinity_present():
    content = INDEX_PATH.read_text()
    assert "PROTECT | WITNESS | APPEND_ONLY" in content, "Trinity missing"


def test_circuit_breaker_trigger():
    content = INDEX_PATH.read_text()
    gc010_section = re.search(
        r"### FR-010 — GC-010: Assumption Cascade Goblin(.*?)(?=\n---\n\n## Symptom Lookup Table|\Z)",
        content,
        re.DOTALL,
    )
    assert gc010_section, "GC-010 section not found"
    section_text = gc010_section.group(1)
    assert "three or more" in section_text.lower() or "3+" in section_text
    assert "STOP_AND_REBASE" in section_text or "STOP" in section_text


def test_all_receipts_linked():
    content = INDEX_PATH.read_text()
    for i in range(1, 11):
        fr_id = f"FR-{i:03d}"
        assert fr_id in content, f"{fr_id} not referenced in index"


def test_all_checklists_linked():
    content = INDEX_PATH.read_text()
    for i in range(1, 11):
        cl_id = f"CL-{i:03d}"
        assert cl_id in content, f"{cl_id} not referenced in index"


def test_schema_file_exists():
    schema_path = Path("schemas/goblin_precedent_index.v0_1.schema.json")
    assert schema_path.exists(), "Schema file missing"


def test_registry_table_present():
    content = INDEX_PATH.read_text()
    assert "## Goblin Registry" in content
    assert "| GC-ID | Goblin Name | Receipt | Checklist | Priority | Status |" in content


if __name__ == "__main__":
    pytest.main([__file__])
