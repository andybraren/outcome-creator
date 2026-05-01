"""Tests for frontmatter utilities."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from frontmatter import compute_verdict, read_frontmatter, validate_frontmatter, write_frontmatter


class TestComputeVerdict:
    def test_perfect_score(self):
        scores = {"measurability": 2, "user_focus": 2, "business_alignment": 2, "actionability": 2}
        total, verdict = compute_verdict(scores)
        assert total == 8
        assert verdict == "PASS"

    def test_revise_score(self):
        scores = {"measurability": 2, "user_focus": 1, "business_alignment": 2, "actionability": 2}
        total, verdict = compute_verdict(scores)
        assert total == 7
        assert verdict == "REVISE"

    def test_revise_minimum(self):
        scores = {"measurability": 1, "user_focus": 1, "business_alignment": 2, "actionability": 2}
        total, verdict = compute_verdict(scores)
        assert total == 6
        assert verdict == "REVISE"

    def test_rework_low_score(self):
        scores = {"measurability": 1, "user_focus": 1, "business_alignment": 1, "actionability": 1}
        total, verdict = compute_verdict(scores)
        assert total == 4
        assert verdict == "REWORK"

    def test_rework_with_zero(self):
        scores = {"measurability": 2, "user_focus": 0, "business_alignment": 2, "actionability": 2}
        total, verdict = compute_verdict(scores)
        assert total == 6
        assert verdict == "REWORK"

    def test_all_zeros(self):
        scores = {"measurability": 0, "user_focus": 0, "business_alignment": 0, "actionability": 0}
        total, verdict = compute_verdict(scores)
        assert total == 0
        assert verdict == "REWORK"


class TestValidateFrontmatter:
    def test_valid_frontmatter(self):
        fm = {
            "id": "OUTCOME-001",
            "title": "Test Outcome",
            "status": "draft",
            "strategic_goals": ["PROJGOALS-314"],
            "priority": "Major",
            "created": "2026-01-15",
            "updated": "2026-01-15",
        }
        errors = validate_frontmatter(fm)
        assert errors == []

    def test_missing_fields(self):
        fm = {"id": "OUTCOME-001", "title": "Test"}
        errors = validate_frontmatter(fm)
        assert any("Missing required fields" in e for e in errors)

    def test_invalid_status(self):
        fm = {
            "id": "OUTCOME-001",
            "title": "Test",
            "status": "invalid",
            "strategic_goals": [],
            "priority": "Major",
            "created": "2026-01-15",
            "updated": "2026-01-15",
        }
        errors = validate_frontmatter(fm)
        assert any("Invalid status" in e for e in errors)

    def test_invalid_priority(self):
        fm = {
            "id": "OUTCOME-001",
            "title": "Test",
            "status": "draft",
            "strategic_goals": [],
            "priority": "Low",
            "created": "2026-01-15",
            "updated": "2026-01-15",
        }
        errors = validate_frontmatter(fm)
        assert any("Invalid priority" in e for e in errors)

    def test_invalid_score(self):
        fm = {
            "id": "OUTCOME-001",
            "title": "Test",
            "status": "draft",
            "strategic_goals": [],
            "priority": "Major",
            "created": "2026-01-15",
            "updated": "2026-01-15",
            "score": {"measurability": 5, "user_focus": 2, "business_alignment": 2, "actionability": 2},
        }
        errors = validate_frontmatter(fm)
        assert any("measurability" in e for e in errors)

    def test_invalid_strategic_goal_format(self):
        fm = {
            "id": "OUTCOME-001",
            "title": "Test",
            "status": "draft",
            "strategic_goals": ["not-a-key"],
            "priority": "Major",
            "created": "2026-01-15",
            "updated": "2026-01-15",
        }
        errors = validate_frontmatter(fm)
        assert any("Invalid strategic goal" in e for e in errors)


class TestReadWriteFrontmatter:
    def test_roundtrip(self, tmp_path):
        path = tmp_path / "test.md"
        fm = {"id": "TEST-001", "title": "Test Outcome", "status": "draft"}
        body = "\n# Test Outcome\n\nSome content here.\n"

        write_frontmatter(path, fm, body)
        read_fm, read_body = read_frontmatter(path)

        assert read_fm["id"] == "TEST-001"
        assert read_fm["title"] == "Test Outcome"
        assert "Some content here." in read_body

    def test_no_frontmatter(self, tmp_path):
        path = tmp_path / "plain.md"
        path.write_text("# Just a markdown file\n\nNo frontmatter here.\n")

        fm, body = read_frontmatter(path)
        assert fm == {}
        assert "Just a markdown file" in body
