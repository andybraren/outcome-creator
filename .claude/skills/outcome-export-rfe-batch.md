# /outcome.export-rfe-batch

Export a rfe-creator batch YAML from an outcome's User Journey phases — **seeds** work for rfe-creator; does not assume one milestone = one RFE.

## Trigger

User says `/outcome.export-rfe-batch` optionally followed by:
- A path to an outcome file in `artifacts/outcome-tasks/` or `local/outcome-tasks/`
- `--per-problem` to emit one problem-slice per bullet (several entries under the same milestone)
- `-o path/to/batch.yaml` to set output path

## Prerequisites

- Outcome uses the **lean template** with **User Journey & Phases** (phases with user capability, problems, success signals)
- Outcome should pass `/outcome.review` (coherent JTBD, problem-framed phases)

## Milestone ↔ RFE cardinality

Each User Journey **phase is a milestone**. After rfe-creator runs, that milestone may yield:

- **One RFE** — phase-candidate passes `right_sized` on review
- **Several sibling RFEs** — `/rfe.split` (or `--per-problem` export) when the milestone bundles multiple independent needs

Do not treat the batch entry count as the final RFE count per milestone.

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
| Default | One `export-role:phase-candidate` per milestone | Often 1 RFE; `/rfe.split` if oversized |
| `--per-problem` | One `export-role:problem-slice` per problem bullet | 1..N RFEs per milestone; split if any slice still oversized |

### Step 3: Sanity-check entries

For each batch entry, verify:

- **prompt** is problem-space only (no product names, no solution language)
- **labels** include `source-outcome:<KEY>`, `milestone-phase:<N>`, `milestone:<name>`, and `export-role`
- **sequencing-note** label present when the phase had value dependencies
- Milestone with 2–3 **independent** problems → prefer `--per-problem` or plan for `/rfe.split` siblings
- Milestone with 4+ unrelated problems → fix outcome (`/outcome.split` or narrow phase) before export

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
- Console: count of **export entries** (not final RFE count per milestone)

## When to use `--per-problem`

Use when a milestone already lists multiple **independent** customer problems that should not be merged into one phase-candidate. Prefer fixing the outcome (split phase or sibling outcome via `/outcome.split`) if problems are unrelated **jobs**, not just unrelated features within one job.
