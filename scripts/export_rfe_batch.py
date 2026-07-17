#!/usr/bin/env python3
"""Export rfe-creator batch YAML from an outcome document's User Journey.

Exports the **Next** subsection (near-term delivery). Future is a deferred
feature list and is skipped unless legacy multi-phase docs are present.

A milestone may become one or several sibling RFEs after rfe-creator
review/split — export only seeds the batch; it does not fix final count.

Default: one phase-candidate prompt for Next (often becomes 1 RFE; may become
several siblings via /rfe.split). Use --per-problem when independent problems should
start as separate entries under the same milestone.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from frontmatter import read_frontmatter

# Preferred: ### Next / ### Future. Legacy: ### Phase N: Name
NEXT_FUTURE_HEADER = re.compile(
    r"^### (Next|Future)\s*$", re.MULTILINE | re.IGNORECASE
)
LEGACY_PHASE_HEADER = re.compile(r"^### Phase (\d+):\s*(.+)\s*$", re.MULTILINE)
FIELD_CAPABILITY = re.compile(
    r"^\*\*(?:User|Customer) capability:\*\*\s*(.+)\s*$", re.MULTILINE
)
FIELD_SUCCESS = re.compile(r"^\*\*Success signal:\*\*\s*(.+)\s*$", re.MULTILINE)
FIELD_PERSONAS = re.compile(
    r"^\*\*Personas this helps:\*\*\s*$", re.MULTILINE | re.IGNORECASE
)
FIELD_WHEN_TRUE = re.compile(
    r"^\*\*When this is true:\*\*\s*$", re.MULTILINE | re.IGNORECASE
)
DEPENDENCY_MARKERS = ("depends on", "dependency")


@dataclass
class OutcomePhase:
    number: int | str
    name: str
    capability: str = ""
    success_signal: str = ""
    problems: list[str] = field(default_factory=list)
    sequencing_notes: list[str] = field(default_factory=list)
    exportable: bool = True  # Future is not exported by default


def _strip_dependency_note(text: str) -> tuple[str, str | None]:
    """Split trailing *(note)* from a problem line; return (problem, sequencing_note)."""
    text = text.strip().lstrip("- ").strip()
    note_match = re.search(r"\*\((.+?)\)\*\s*$", text)
    if note_match:
        note = note_match.group(1).strip()
        problem = text[: note_match.start()].strip()
        return problem, note
    return text, None


def _is_sequencing_only_line(problem: str) -> bool:
    lower = problem.lower().strip("* ")
    return any(m in lower for m in DEPENDENCY_MARKERS) and len(problem) < 120


def _journey_body(body: str) -> str | None:
    arc_match = re.search(
        r"^## (?:User Journey & Phases|User Journey & Milestones|Customer Arc & Delivery Plan|User Journey)\s*$",
        body,
        re.MULTILINE | re.IGNORECASE,
    )
    if not arc_match:
        return None

    arc_body = body[arc_match.end() :]
    next_section = re.search(r"^## [^#]", arc_body, re.MULTILINE)
    if next_section:
        arc_body = arc_body[: next_section.start()]
    return arc_body


def _parse_block_fields(block: str, phase: OutcomePhase) -> None:
    cap = FIELD_CAPABILITY.search(block)
    if cap:
        phase.capability = cap.group(1).strip()

    # Prefer Personas this helps; fall back to legacy When this is true
    personas_match = FIELD_PERSONAS.search(block) or FIELD_WHEN_TRUE.search(block)
    if personas_match and not phase.capability:
        rest = block[personas_match.end() :]
        stop = re.search(
            r"^\*\*(?:Features to deliver|Success signal|Problems)",
            rest,
            re.MULTILINE,
        )
        if stop:
            rest = rest[: stop.start()]
        bullets: list[str] = []
        for line in rest.splitlines():
            line = line.strip()
            if line.startswith("- "):
                bullets.append(line[2:].strip())
        if bullets:
            phase.capability = "; ".join(bullets)

    sig = FIELD_SUCCESS.search(block)
    if sig:
        phase.success_signal = sig.group(1).strip()

    problems_match = re.search(
        r"^\*\*Problems (?:to address|this (?:phase )?addresses):\*\*\s*$",
        block,
        re.MULTILINE | re.IGNORECASE,
    )
    if problems_match:
        rest = block[problems_match.end() :]
        scenario = re.search(r"^####\s+", rest, re.MULTILINE)
        if scenario:
            rest = rest[: scenario.start()]
        # Stop at next bold field so features/personas are not eaten as problems
        next_field = re.search(r"^\*\*[^*]+:\*\*\s*$", rest, re.MULTILINE)
        if next_field:
            rest = rest[: next_field.start()]
        for line in rest.splitlines():
            line = line.strip()
            if not line.startswith("- "):
                continue
            problem, note = _strip_dependency_note(line)
            if _is_sequencing_only_line(problem):
                if note:
                    phase.sequencing_notes.append(note)
                else:
                    phase.sequencing_notes.append(problem)
                continue
            if problem:
                phase.problems.append(problem)
            if note:
                phase.sequencing_notes.append(note)


def parse_phases(body: str) -> list[OutcomePhase]:
    """Parse Next/Future (preferred) or legacy ### Phase N sections."""
    arc_body = _journey_body(body)
    if arc_body is None:
        return []

    nf_headers = list(NEXT_FUTURE_HEADER.finditer(arc_body))
    if nf_headers:
        phases: list[OutcomePhase] = []
        for i, match in enumerate(nf_headers):
            start = match.end()
            end = nf_headers[i + 1].start() if i + 1 < len(nf_headers) else len(arc_body)
            block = arc_body[start:end]
            name = match.group(1).strip().title()  # Next / Future
            phase = OutcomePhase(
                number=name.lower(),
                name=name,
                exportable=(name.lower() == "next"),
            )
            _parse_block_fields(block, phase)
            phases.append(phase)
        return phases

    # Legacy multi-phase support
    headers = list(LEGACY_PHASE_HEADER.finditer(arc_body))
    if not headers:
        return []

    phases = []
    for i, match in enumerate(headers):
        start = match.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(arc_body)
        block = arc_body[start:end]
        phase = OutcomePhase(
            number=int(match.group(1)),
            name=match.group(2).strip(),
            exportable=True,
        )
        _parse_block_fields(block, phase)
        phases.append(phase)

    return phases


def _clean_sequencing_note(note: str) -> str:
    return note.strip().lstrip("- ").strip("* ").strip()


def build_phase_prompt(phase: OutcomePhase, job_context: str = "") -> str:
    """Build a problem-space RFE prompt seeding one milestone (may split into siblings)."""
    sentences: list[str] = []
    if job_context:
        sentences.append(job_context.rstrip(".") + ".")
    if phase.capability:
        sentences.append(f"Milestone ({phase.name}): {phase.capability.rstrip('.')}.")
    for problem in phase.problems:
        sentences.append(problem.rstrip(".") + ".")
    return " ".join(sentences)


def build_slice_prompt(problem: str, phase: OutcomePhase, job_context: str = "") -> str:
    """Build a prompt for a single problem slice within a phase."""
    parts: list[str] = []
    if job_context:
        parts.append(job_context.strip())
    if phase.capability:
        parts.append(f"Within the broader milestone ({phase.name}): {phase.capability}")
    parts.append(problem)
    return " ".join(parts)


def _priority_from_frontmatter(fm: dict[str, Any]) -> str:
    p = fm.get("priority", "Major")
    if p in ("Critical", "Major", "Minor"):
        return p
    return "Major"


def _milestone_phase_label(phase: OutcomePhase) -> str:
    return f"milestone-phase:{phase.number}"


def phases_to_batch_entries(
    phases: list[OutcomePhase],
    *,
    outcome_id: str,
    priority: str,
    per_problem: bool = False,
    job_context: str = "",
) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    slice_idx = 0

    for phase in phases:
        if not phase.exportable:
            continue

        sequencing = (
            "; ".join(_clean_sequencing_note(n) for n in phase.sequencing_notes)
            if phase.sequencing_notes
            else ""
        )

        if per_problem:
            for problem in phase.problems:
                slice_idx += 1
                labels = [
                    f"source-outcome:{outcome_id}",
                    _milestone_phase_label(phase),
                    f"milestone:{phase.name}",
                    f"export-role:problem-slice",
                    f"slice:{slice_idx}",
                ]
                if sequencing:
                    labels.append(f"sequencing-note:{sequencing}")
                entries.append(
                    {
                        "prompt": build_slice_prompt(problem, phase, job_context),
                        "priority": priority,
                        "labels": labels,
                    }
                )
            continue

        if not phase.problems and not phase.capability:
            continue

        slice_idx += 1
        labels = [
            f"source-outcome:{outcome_id}",
            _milestone_phase_label(phase),
            f"milestone:{phase.name}",
            "export-role:phase-candidate",
            f"slice:{slice_idx}",
        ]
        if sequencing:
            labels.append(f"sequencing-note:{sequencing}")

        entry: dict[str, Any] = {
            "prompt": build_phase_prompt(phase, job_context),
            "priority": priority,
            "labels": labels,
        }
        if phase.success_signal:
            entry["milestone_success_signal"] = phase.success_signal
        entries.append(entry)

    return entries


def extract_job_context(body: str) -> str:
    """One-line JTBD from Problem Statement for richer RFE prompts."""
    ps = re.search(r"^## Problem Statement\s*$", body, re.MULTILINE)
    section = body[ps.end() :] if ps else body
    next_h = re.search(r"^## ", section, re.MULTILINE)
    if next_h:
        section = section[: next_h.start()]

    # Prefer Goal; fall back to legacy Job (JTBD)
    # Bold label may be **Label**: or **Label**: (colon inside or outside bold)
    goal = re.search(
        r"\*\*(?:Goal|Job \(JTBD\))(:\*\*|\*\*:)\s*(.+?)\s*$",
        section,
        re.MULTILINE,
    )
    struggle = re.search(
        r"\*\*Struggle(:\*\*|\*\*:)\s*(.+?)\s*$", section, re.MULTILINE
    )
    if goal and struggle:
        return (
            f"Enterprises need to {goal.group(2).strip().lower().rstrip('.')}, "
            f"but {struggle.group(2).strip().lower().rstrip('.')}"
        )
    if goal:
        return goal.group(2).strip()
    return ""


def export_batch(
    outcome_path: Path,
    *,
    per_problem: bool = False,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    fm, body = read_frontmatter(outcome_path)
    outcome_id = str(fm.get("id", outcome_path.stem))
    priority = _priority_from_frontmatter(fm)
    job_context = extract_job_context(body)
    phases = parse_phases(body)
    entries = phases_to_batch_entries(
        phases,
        outcome_id=outcome_id,
        priority=priority,
        per_problem=per_problem,
        job_context=job_context,
    )
    header = {
        "generated_by": "outcome-creator",
        "source_outcome": outcome_id,
        "usage": "Run in rfe-creator: /rfe.speedrun --input <this-file> --headless",
        "rfe_sizing": (
            "Next may yield 1..N sibling RFEs. After speedrun, /rfe.review each entry; "
            "if right_sized < 2, /rfe.split and keep milestone-phase labels on children. "
            "See docs/outcome-rfe-handoff.md."
        ),
    }
    return header, entries


def write_batch_file(
    outcome_path: Path,
    output_path: Path | None = None,
    *,
    per_problem: bool = False,
) -> Path:
    fm, _ = read_frontmatter(outcome_path)
    outcome_id = str(fm.get("id", outcome_path.stem))
    if output_path is None:
        slug = outcome_path.stem
        output_path = outcome_path.parent.parent / "rfe-batches" / f"{slug}-rfe-batch.yaml"

    header, entries = export_batch(outcome_path, per_problem=per_problem)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# Generated by outcome-creator — {outcome_id}",
        f"# {header['usage']}",
        f"# {header['rfe_sizing']}",
        "",
    ]
    lines.append(yaml.dump(entries, default_flow_style=False, sort_keys=False, allow_unicode=True))
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Export rfe-creator batch YAML from an outcome")
    parser.add_argument("outcome_file", type=Path, help="Path to outcome markdown file")
    parser.add_argument("-o", "--output", type=Path, help="Output YAML path")
    parser.add_argument(
        "--per-problem",
        action="store_true",
        help=(
            "One problem-slice per bullet under Next (default: one phase-candidate "
            "for Next — may still become several RFEs via /rfe.split)"
        ),
    )
    args = parser.parse_args()

    out = write_batch_file(args.outcome_file, args.output, per_problem=args.per_problem)
    _, entries = export_batch(args.outcome_file, per_problem=args.per_problem)
    print(f"Wrote {len(entries)} RFE entries to {out}")


if __name__ == "__main__":
    main()
