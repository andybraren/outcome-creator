# Outcome → RFE Handoff

How outcome-creator connects to [rfe-creator](https://github.com/jwforres/rfe-creator) so Next produces **right-sized** child RFEs.

Journey structure should be planned first — see [outcome-milestone-planning.md](outcome-milestone-planning.md) (`/outcome.plan-milestones`). Outcomes use exactly **Next** + **Future**.

## Milestone ↔ RFE cardinality

**Next** is the exportable milestone. It is not assumed to map 1:1 to a single RFE.

| Situation | Typical result |
|-----------|----------------|
| One capability thread, 1–3 related problems, passes three-solutions test | **1 RFE** for Next |
| Multiple independent problems under Next | **Several sibling RFEs** (export with `--per-problem` and/or `/rfe.split`) |
| Phase-candidate still too broad after review | **Several sibling RFEs** from `/rfe.split` on one exported entry |

Sibling RFEs from Next should share labels: `source-outcome:<KEY>`, `milestone-phase:next`, `milestone:Next`. After `/rfe.split`, carry those labels forward on each child so Jira traceability stays clear.

**Future** is a deferred feature list — promote items into Next before exporting them as RFE seeds.

## Pipeline position

```
outcome-creator (GOAL)
  └─ User Journey = Next (near-term) + Future (later features)
       └─ outcome.export-rfe-batch → YAML batch from Next (seeds 1..N candidates)
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

outcome-creator uses the same *ideas* at the outcome layer in `/outcome.split` (sibling outcomes). At the handoff layer, export **seeds** work for rfe-creator; final RFE count for Next is determined by review and split.

## Export modes (not final RFE count)

`/outcome.export-rfe-batch` reads **User Journey & Phases** and exports **Next** (legacy multi-phase docs still parse if present):

### Default: phase-candidate for Next

One batch entry with `export-role:phase-candidate`. This is a **starting prompt** — often one RFE, sometimes several after `/rfe.split`.

- **prompt** — JTBD context + persona/capability language + problem bullets (problem-space only)
- **labels** — `source-outcome`, `milestone-phase:next`, `milestone:Next`, `export-role`, optional `sequencing-note`
- **milestone_success_signal** — copied from Next (traceability; rfe-creator may ignore unknown fields)

### `--per-problem`: problem-slices under Next

One entry per problem bullet with `export-role:problem-slice`. Use when problems are already clearly independent but still belong to Next. You may still need `/rfe.split` on an individual slice.

## Choosing export mode

```
For Next:
  ├─ 1 capability thread + 1–3 related problems, one job thread?
  │     └─ default export (phase-candidate) → expect 1 RFE, split if review fails
  ├─ 2–3 clearly independent problems (different actors/scenarios)?
  │     └─ --per-problem OR phase-candidate + /rfe.split
  └─ 4+ unrelated problems or mixed job threads?
        └─ fix outcome (/outcome.split or tighten Next / move work to Future) before export
```

## Recommended workflow

```bash
# 1. Outcome ready (lean template, Next with success signal)
/outcome.review OUTCOME-155.md

# 2. Export batch for rfe-creator (seeds from Next, not final count)
python3 scripts/export_rfe_batch.py artifacts/outcome-tasks/RHAISTRAT-155-*.md
# optional: --per-problem when Next already has independent problem bullets

# 3. In rfe-creator repo
/rfe.speedrun --input ../outcome-creator/artifacts/rfe-batches/RHAISTRAT-155-rfe-batch.yaml --headless

# 4. For Next: 1..N sibling RFEs
/rfe.review RHAIRFE-XXXX   # check scores.right_sized
/rfe.split RHAIRFE-XXXX    # if right_sized < 2 → siblings under same milestone-phase label
```

## Sizing heuristics

**Next is likely one RFE when:**

- Personas this helps form one capability thread (passes three-solutions test)
- 1–3 problem bullets on the same job thread
- Could be delivered as one strategy feature with one summary sentence

**Expect several sibling RFEs for Next when:**

- Multiple independent problem bullets (different actors, unrelated scenarios)
- Phase-candidate prompt needs "and" between unrelated user needs
- `/rfe.review` scores `right_sized` 0–1 on the candidate

**Fix the outcome (not just split RFEs) when:**

- Next fails JTBD coherence — unrelated jobs bundled
- Kitchen-sink Next with 4+ unrelated problems and no delivery coupling
- Journey still uses a multi-phase arc instead of Next + Future

## Jira linking (future)

rfe-creator children support `parent_key` in frontmatter for split lineage. Outcome → RFE linking today uses labels (`source-outcome:RHAISTRAT-155`, `milestone-phase:next`). A future enhancement: set Jira "is child of" from Outcome issue when submitting RFEs.
