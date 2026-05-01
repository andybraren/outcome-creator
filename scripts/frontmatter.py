"""YAML frontmatter read/write/schema utilities for outcome documents."""

import re
from datetime import date
from pathlib import Path
from typing import Any

import yaml

FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

REQUIRED_FIELDS = {"id", "title", "status", "strategic_goals", "priority", "created", "updated"}

VALID_STATUSES = {"draft", "review", "approved", "active", "closed"}
VALID_PRIORITIES = {"Critical", "Major", "Minor"}
VALID_VERDICTS = {"PASS", "REVISE", "REWORK"}


def read_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    """Read YAML frontmatter and body from a markdown file.

    Returns (frontmatter_dict, body_text).
    """
    content = path.read_text(encoding="utf-8")
    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        return {}, content

    fm_raw = match.group(1)
    body = content[match.end():]
    fm = yaml.safe_load(fm_raw) or {}
    return fm, body


def write_frontmatter(path: Path, frontmatter: dict[str, Any], body: str) -> None:
    """Write YAML frontmatter and body to a markdown file."""
    fm_str = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False, allow_unicode=True)
    content = f"---\n{fm_str}---\n{body}"
    path.write_text(content, encoding="utf-8")


def update_frontmatter(path: Path, updates: dict[str, Any]) -> dict[str, Any]:
    """Read, update specific fields, and write back. Returns the updated frontmatter."""
    fm, body = read_frontmatter(path)
    fm.update(updates)
    fm["updated"] = str(date.today())
    write_frontmatter(path, fm, body)
    return fm


def validate_frontmatter(fm: dict[str, Any]) -> list[str]:
    """Validate frontmatter against the schema. Returns a list of error messages."""
    errors = []

    missing = REQUIRED_FIELDS - set(fm.keys())
    if missing:
        errors.append(f"Missing required fields: {', '.join(sorted(missing))}")

    if fm.get("status") and fm["status"] not in VALID_STATUSES:
        errors.append(f"Invalid status '{fm['status']}'. Must be one of: {', '.join(sorted(VALID_STATUSES))}")

    if fm.get("priority") and fm["priority"] not in VALID_PRIORITIES:
        errors.append(f"Invalid priority '{fm['priority']}'. Must be one of: {', '.join(sorted(VALID_PRIORITIES))}")

    if fm.get("score") and isinstance(fm["score"], dict):
        score = fm["score"]
        for dim in ("measurability", "user_focus", "business_alignment", "actionability"):
            val = score.get(dim)
            if val is not None and not (0 <= val <= 2):
                errors.append(f"Score '{dim}' must be 0-2, got {val}")

        if score.get("verdict") and score["verdict"] not in VALID_VERDICTS:
            errors.append(f"Invalid verdict '{score['verdict']}'. Must be one of: {', '.join(sorted(VALID_VERDICTS))}")

    goals = fm.get("strategic_goals", [])
    if goals:
        for g in goals:
            if not isinstance(g, str) or not re.match(r"^[A-Z]+-\d+$", g):
                errors.append(f"Invalid strategic goal key '{g}'. Expected format: PROJECT-123")

    return errors


def compute_verdict(scores: dict[str, int]) -> tuple[int, str]:
    """Compute total score and verdict from dimension scores."""
    dims = ["measurability", "user_focus", "business_alignment", "actionability"]
    total = sum(scores.get(d, 0) for d in dims)
    has_zero = any(scores.get(d, 0) == 0 for d in dims)

    if total >= 8:
        verdict = "PASS"
    elif total >= 6 and not has_zero:
        verdict = "REVISE"
    else:
        verdict = "REWORK"

    return total, verdict


def apply_scores(path: Path, scores: dict[str, int]) -> dict[str, Any]:
    """Apply dimension scores to an outcome document's frontmatter."""
    total, verdict = compute_verdict(scores)
    score_block = {
        **scores,
        "total": total,
        "verdict": verdict,
    }
    return update_frontmatter(path, {"score": score_block})
