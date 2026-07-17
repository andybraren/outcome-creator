---
name: outcome.split
description: Split an oversized outcome into sibling outcomes or narrow phases
---
# /outcome.split

Split an oversized outcome into sibling outcomes or narrow phases — analogous to `/rfe.split` in [rfe-creator](https://github.com/jwforres/rfe-creator), but at the **outcome** layer.

## Trigger

User says `/outcome.split` optionally followed by:
- A path to an outcome file
- `--headless` to skip interactive confirmation

## When to split (not the same as /rfe.split)

| Signal | Action |
|--------|--------|
| JTBD coherence fails — unrelated jobs in one outcome | Split into **sibling outcomes** (new outcome docs) |
| Kitchen sink anti-pattern — 5+ teams, no shared job thread | Split by job thread |
| Next has 4+ unrelated problem bullets | **`/outcome.plan-milestones --apply`** to tighten Next / move work to Future, or export with `--per-problem` |
| Next passes three-solutions test, 1–3 related problems | **Do not split** — use `/outcome.export-rfe-batch` |

## Behavior

### Step 1: Load outcome

Read Problem Statement, User Journey (Next + Future), Evidence, Out of Scope.

### Step 2: Atomic job inventory (from rfe.split pattern)

For each struggle or problem bullet, ask:

1. Could this ship as its own outcome without breaking a coherent user journey?
2. Does it share a job thread with the others, or is it a different job?
3. Are capabilities **delivery-coupled** (must ship together)? If yes, keep in one outcome (typically under Next).

List atomic items with one-sentence job statements. Mark delivery-coupled groups.

### Step 3: Propose split strategies

Propose 2–3 ways to group into sibling outcomes:

- How many outcomes
- What each outcome's JTBD would be
- Which phases move to which outcome
- What moves to Out of Scope / "deferred sibling" on each

**Recommend** the option with the fewest outcomes where each still passes JTBD coherence and is not a kitchen sink.

### Step 4: Generate sibling outcomes (if splitting)

For each sibling:

1. Copy lean template structure from `templates/outcome-template.md`
2. Rewrite Problem Statement (JTBD) for that job thread only
3. Keep only relevant User Journey phases
4. Add cross-reference in Out of Scope: "See sibling outcome: …"
5. Write to `artifacts/outcome-tasks/OUTCOME-NNN-<slug>.md` with new frontmatter

Archive or mark the parent outcome `status: split` in frontmatter and note `split_children: [OUTCOME-002, ...]` if useful.

### Step 5: Write split status

Write `artifacts/outcome-reviews/<ID>-split-status.yaml`:

```yaml
status: completed
action: split | no-split
reason: "<short explanation>"
children: [OUTCOME-002, OUTCOME-003]
```

If `no-split`, explain (e.g. delivery-coupled phases, single coherent job).

### Step 6: Next steps

- Run `/outcome.review` on each sibling
- Run `/outcome.export-rfe-batch` per sibling when ready for rfe-creator

## Relationship to rfe-creator

- **outcome.split** → fixes scope at the goal layer (sibling outcomes)
- **outcome.export-rfe-batch** → seeds rfe-creator batch entries per milestone (1..N RFEs per milestone after review/split)
- **rfe.split** → sibling RFEs when a candidate is still too large

Do not skip outcome.split and rely only on rfe.split — you will get many RFEs without a coherent parent outcome.
