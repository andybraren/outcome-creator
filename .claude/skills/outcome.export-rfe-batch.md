---
name: outcome.export-rfe-batch
description: Export an rfe-creator batch YAML from an outcome Next subsection
---
# /outcome.export-rfe-batch

Export a rfe-creator batch YAML from an outcome's **Next** subsection — **seeds** work for rfe-creator; does not assume Next = one RFE.

## Trigger

User says `/outcome.export-rfe-batch` optionally followed by:
- A path to an outcome file in `artifacts/outcome-tasks/` or `local/outcome-tasks/`
- `--per-problem` to emit one problem-slice per bullet (several entries under the same milestone)
- `-o path/to/batch.yaml` to set output path

## Prerequisites

- Outcome uses the **lean template** with **User Journey & Phases** (`### Next` + `### Future`; Next has problems, personas, success signal)
- Outcome should pass `/outcome.review` (coherent JTBD, Next + Future only)

## Milestone ↔ RFE cardinality

**Next** is the exportable milestone. **Future** is skipped (promote items into Next before exporting). After rfe-creator runs, Next may yield:

- **One RFE** — phase-candidate passes `right_sized` on review
- **Several sibling RFEs** — `/rfe.split` (or `--per-problem` export) when Next bundles multiple independent needs

Do not treat the batch entry count as the final RFE count.

## Behavior

### Step 1: Locate outcome

Read the outcome markdown file (frontmatter + body).

### Step 2: Run export script

```bash
python3 scripts/export_rfe_batch.py <outcome-file> [--per-problem] [-o artifacts/rfe-batches/<slug>-rfe-batch.yaml]
```

Default output: `artifacts/rfe-batches/<slug>-rfe-batch.yaml`

| Mode | Export produces | Typical downstream |
|------|-----------------|-------------------|
| Default | One `export-role:phase-candidate` for Next | Often 1 RFE; `/rfe.split` if oversized |
| `--per-problem` | One `export-role:problem-slice` per Next problem bullet | 1..N RFEs; split if any slice still oversized |

### Step 3: Sanity-check entries

For each batch entry, verify:

- **prompt** is problem-space only (no product names, no solution language)
- **labels** include `source-outcome:<KEY>`, `milestone-phase:next`, `milestone:Next`, and `export-role`
- **sequencing-note** label present when Next had value dependencies
- Next with 2–3 **independent** problems → prefer `--per-problem` or plan for `/rfe.split` siblings
- Next with 4+ unrelated problems → fix outcome (`/outcome.split` or tighten Next / move work to Future) before export

### Step 4: Tell user next steps

Hand off to [rfe-creator](https://github.com/jwforres/rfe-creator):

```
/rfe.speedrun --input <batch-file> --headless
/rfe.review <RFE-IDs>          # check right_sized scores per entry
/rfe.split <ID>                # sibling RFEs under same milestone when oversized
```

Preserve `milestone-phase` / `milestone` labels on split children. See `docs/outcome-rfe-handoff.md`.

## Output

- YAML batch file ready for `/rfe.speedrun --input`
- Console: count of **export entries** (not final RFE count)

## When to use `--per-problem`

Use when Next already lists multiple **independent** customer problems that should not be merged into one phase-candidate. Prefer fixing the outcome (move work to Future or sibling outcome via `/outcome.split`) if problems are unrelated **jobs**, not just unrelated features within one job.
