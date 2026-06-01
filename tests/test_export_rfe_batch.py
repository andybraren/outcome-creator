"""Tests for export_rfe_batch phase parsing."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from export_rfe_batch import (
    extract_job_context,
    parse_phases,
    phases_to_batch_entries,
    OutcomePhase,
)

SAMPLE_PROBLEM = """
## Problem Statement

- **Job (JTBD)**: Run AI agents in production with enterprise confidence
- **Struggle**: There is no equivalent of MLOps for agents.

## Evidence
"""

SAMPLE_ARC = """
## User Journey & Milestones

### Phase 1: Trust

**User capability:** Security teams can establish identity and access boundaries.

**Success signal:** ≥1 account in production (target: 6 months)

**Problems this phase addresses:**
- Agents act with ambiguous identities *(identity before access control)*
- End-user context is lost during tool execution

#### Scenario: Example
- **Actors:** Architect

### Phase 2: Operate

**User capability:** Platform teams can deploy agents regardless of framework.

**Problems this phase addresses:**
- Lifecycle is tied to the specific framework
- *Depends on Phase 1 — governance required*

## Evidence
"""


def test_extract_job_context():
    ctx = extract_job_context(SAMPLE_PROBLEM)
    assert "enterprises need to run ai agents" in ctx.lower()
    assert "mlops" in ctx.lower()


def test_parse_phases():
    phases = parse_phases(SAMPLE_ARC)
    assert len(phases) == 2
    assert phases[0].name == "Trust"
    assert len(phases[0].problems) == 2
    assert any("identity before access control" in n for n in phases[0].sequencing_notes)
    assert phases[1].name == "Operate"
    assert len(phases[1].problems) == 1
    assert any("Phase 1" in n for n in phases[1].sequencing_notes)


def test_phases_to_batch_per_phase():
    phases = parse_phases(SAMPLE_ARC)
    entries = phases_to_batch_entries(
        phases, outcome_id="OUT-1", priority="Critical", per_problem=False
    )
    assert len(entries) == 2
    assert entries[0]["labels"][0] == "source-outcome:OUT-1"
    assert "milestone-phase:1" in entries[0]["labels"]
    assert "export-role:phase-candidate" in entries[0]["labels"]
    assert "milestone_success_signal" in entries[0]


def test_phases_to_batch_per_problem():
    phases = parse_phases(SAMPLE_ARC)
    entries = phases_to_batch_entries(
        phases, outcome_id="OUT-1", priority="Major", per_problem=True
    )
    assert len(entries) == 3
    assert "export-role:problem-slice" in entries[0]["labels"]
    assert "milestone-phase:1" in entries[0]["labels"]
