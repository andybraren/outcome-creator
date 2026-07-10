#!/usr/bin/env python3
"""Export rfe-creator batch YAML from an outcome document's delivery phases.

A milestone (User Journey phase) may become one or several sibling RFEs after
rfe-creator review/split — export only seeds the batch; it does not fix final count.

Default: one phase-candidate prompt per milestone (often becomes 1 RFE; may become
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

PHASE_HEADER = re.compile(r"^### Phase (\d+):\s*(.+)\s*$", re.MULTILINE)
FIELD_CAPABILITY = re.compile(
    r"^\*\*(?:User|Customer) capability:\*\*\s*(.+)\s*$", re.MULTILINE
)
FIELD_SUCCESS = re.compile(r"^\*\*Success signal:\*\*\s*(.+)\s*$", re.MULTILINE)
DEPENDENCY_MARKERS = ("depends on", "dependency")


@dataclass
class OutcomePhase:
    number: int
    name: str
    capability: str = ""
    success_signal: str = ""
    problems: list[str] = field(default_factory=list)
    sequencing_notes: list[str] = field(default_factory=list)


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


def parse_phases(body: str) -> list[OutcomePhase]:
    """Parse ### Phase N: sections from User Journey & Phases."""
    arc_match = re.search(
        r"^## (?:User Journey & Phases|User Journey & Milestones|Customer Arc & Delivery Plan)\s*$",
        body,
        re.MULTILINE | re.IGNORECASE,
    )
    if not arc_match:
        return []

    arc_body = body[arc_match.end() :]
    # Stop at next top-level ## section
    next_section = re.search(r"^## [^#]", arc_body, re.MULTILINE)
    if next_section:
        arc_body = arc_body[: next_section.start()]

    headers = list(PHASE_HEADER.finditer(arc_body))
    if not headers:
        return []

    phases: list[OutcomePhase] = []
    for i, match in enumerate(headers):
        start = match.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(arc_body)
        block = arc_body[start:end]
        phase = OutcomePhase(
            number=int(match.group(1)),
            name=match.group(2).strip(),
        )

        cap = FIELD_CAPABILITY.search(block)
        if cap:
            phase.capability = cap.group(1).strip()

        sig = FIELD_SUCCESS.search(block)
        if sig:
            phase.success_signal = sig.group(1).strip()

        problems_match = re.search(
            r"^\*\*Problems this phase addresses:\*\*\s*$",
            block,
            re.MULTILINE,
        )
        if problems_match:
            rest = block[problems_match.end() :]
            scenario = re.search(r"^####\s+", rest, re.MULTILINE)
            if scenario:
                rest = rest[: scenario.start()]
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
        sequencing = "; ".join(_clean_sequencing_note(n) for n in phase.sequencing_notes) if phase.sequencing_notes else ""

        if per_problem:
            for problem in phase.problems:
                slice_idx += 1
                labels = [
                    f"source-outcome:{outcome_id}",
                    f"milestone-phase:{phase.number}",
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
            f"milestone-phase:{phase.number}",
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

    # Bold label may be **Label**: or **Label**: (colon inside or outside bold)
    job = re.search(
        r"\*\*Job \(JTBD\)(:\*\*|\*\*:)\s*(.+?)\s*$", section, re.MULTILINE
    )
    struggle = re.search(
        r"\*\*Struggle(:\*\*|\*\*:)\s*(.+?)\s*$", section, re.MULTILINE
    )
    if job and struggle:
        return (
            f"Enterprises need to {job.group(2).strip().lower().rstrip('.')}, "
            f"but {struggle.group(2).strip().lower().rstrip('.')}"
        )
    if job:
        return job.group(2).strip()
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
            "Each milestone may yield 1..N sibling RFEs. After speedrun, /rfe.review each entry; "
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
            "One problem-slice per bullet under each milestone (default: one phase-candidate "
            "per milestone — may still become several RFEs via /rfe.split)"
        ),
    )
    args = parser.parse_args()

    out = write_batch_file(args.outcome_file, args.output, per_problem=args.per_problem)
    _, entries = export_batch(args.outcome_file, per_problem=args.per_problem)
    print(f"Wrote {len(entries)} RFE entries to {out}")


if __name__ == "__main__":
    main()
