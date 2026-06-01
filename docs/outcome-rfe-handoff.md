# Outcome → RFE Handoff

How outcome-creator connects to [rfe-creator](https://github.com/jwforres/rfe-creator) so milestones produce **right-sized** child RFEs.

Milestone structure should be planned first — see [outcome-milestone-planning.md](outcome-milestone-planning.md) (`/outcome.plan-milestones`).

## Milestone ↔ RFE cardinality

A **milestone** (User Journey phase) is not assumed to map 1:1 to a single RFE.

| Situation | Typical result |
|-----------|----------------|
| One capability, 1–3 related problems, passes three-solutions test | **1 RFE** for the milestone |
| Multiple independent problems under one milestone | **Several sibling RFEs** (export with `--per-problem` and/or `/rfe.split`) |
| Phase-candidate still too broad after review | **Several sibling RFEs** from `/rfe.split` on one exported entry |

Sibling RFEs from the same milestone should share labels: `source-outcome:<KEY>`, `milestone-phase:<N>`, `milestone:<name>`. After `/rfe.split`, carry those labels forward on each child so Jira traceability stays clear.

## Pipeline position

```
outcome-creator (GOAL)
  └─ User Journey phases = delivery milestones
       └─ outcome.export-rfe-batch → YAML batch (seeds 1..N candidates per milestone)
            └─ rfe-creator /rfe.speedrun (WHAT)
                 └─ /rfe.review → scores right_sized (0–2)
                      └─ /rfe.split → sibling RFEs when a candidate is still oversized
```

## Two different "split" problems

| Problem | Tool | When |
|---------|------|------|
| **Outcome too big** | `/outcome.split` (outcome-creator) | Unrelated jobs bundled (kitchen sink); JTBD coherence fails; should be sibling outcomes |
| **RFE too big** | `/rfe.split` ([rfe-creator](https://github.com/jwforres/rfe-creator)) | After export: review scores `right_sized` 0/2; one candidate maps to 3+ strategy features |

Do not use `/rfe.split` to fix a badly scoped **outcome** — fix the outcome first, then re-export the batch.

## What rfe-creator split does (borrowed pattern)

From `rfe.split` in rfe-creator:

1. **Atomic capability inventory** — list gaps as independent customer values
2. **Group only what is delivery-coupled** — must ship together or experience breaks
3. **Generate children** — each child is a standalone business need with coverage check
4. **Review children** — assess-rfe rubric including **Right-sized** (0–2)
5. **Self-correct once** — re-split children still scoring &lt; 2 on right_sized

outcome-creator uses the same *ideas* at the outcome layer in `/outcome.split` (sibling outcomes). At the handoff layer, export **seeds** work for rfe-creator; final RFE count per milestone is determined by review and split.

## Export modes (not final RFE count)

`/outcome.export-rfe-batch` reads **User Journey & Milestones**:

### Default: phase-candidate per milestone

One batch entry per phase with `export-role:phase-candidate`. This is a **starting prompt** for the milestone — often one RFE, sometimes several after `/rfe.split`.

- **prompt** — JTBD context + capability + problem bullets (problem-space only)
- **labels** — `source-outcome`, `milestone-phase`, `milestone`, `export-role`, optional `sequencing-note`
- **milestone_success_signal** — copied from the phase (traceability; rfe-creator may ignore unknown fields)

### `--per-problem`: problem-slices under a milestone

One entry per problem bullet with `export-role:problem-slice`. Use when problems are already clearly independent but still belong to the same milestone. You may still need `/rfe.split` on an individual slice.

## Choosing export mode

```
For each milestone phase:
  ├─ 1 capability + 1–3 related problems, one job thread?
  │     └─ default export (phase-candidate) → expect 1 RFE, split if review fails
  ├─ 2–3 clearly independent problems (different actors/scenarios)?
  │     └─ --per-problem OR phase-candidate + /rfe.split
  └─ 4+ unrelated problems or mixed job threads?
        └─ fix outcome (/outcome.split or narrow phase) before export
```

## Recommended workflow

```bash
# 1. Outcome ready (lean template, phases with success signals)
/outcome.review OUTCOME-155.md

# 2. Export batch for rfe-creator (seeds, not final count)
python3 scripts/export_rfe_batch.py artifacts/outcome-tasks/RHAISTRAT-155-*.md
# optional: --per-problem when milestones already have independent problem bullets

# 3. In rfe-creator repo
/rfe.speedrun --input ../outcome-creator/artifacts/rfe-batches/RHAISTRAT-155-rfe-batch.yaml --headless

# 4. Per milestone: 1..N sibling RFEs
/rfe.review RHAIRFE-XXXX   # check scores.right_sized
/rfe.split RHAIRFE-XXXX    # if right_sized < 2 → siblings under same milestone-phase label
```

## Sizing heuristics

**A milestone is likely one RFE when:**

- One user capability headline (passes three-solutions test)
- 1–3 problem bullets on the same job thread
- Could be delivered as one strategy feature with one summary sentence

**Expect several sibling RFEs for one milestone when:**

- Multiple independent problem bullets (different actors, unrelated scenarios)
- Phase-candidate prompt needs "and" between unrelated user needs
- `/rfe.review` scores `right_sized` 0–1 on the candidate

**Fix the outcome (not just split RFEs) when:**

- The whole phase fails JTBD coherence — unrelated jobs bundled in one milestone
- Kitchen-sink milestone with 4+ unrelated problems and no delivery coupling

## Jira linking (future)

rfe-creator children support `parent_key` in frontmatter for split lineage. Outcome → RFE linking today uses labels (`source-outcome:RHAISTRAT-155`, `milestone-phase:1`). A future enhancement: set Jira "is child of" from Outcome issue when submitting RFEs.
