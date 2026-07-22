---
name: outcome.plan-milestones
description: Plan or refactor User Journey into Next and Future using bottom-up capability inventory
---
# /outcome.plan-milestones

Plan or refactor **User Journey** into exactly **Next** (near-term) and **Future** (later) using bottom-up capability inventory and delivery-coupling rules (adapted from [rfe-creator `/rfe.split`](https://github.com/jwforres/rfe-creator)).

## Trigger

User says `/outcome.plan-milestones` optionally followed by:

- A path to an outcome file in `artifacts/outcome-tasks/` or `local/outcome-tasks/`
- `--apply` to rewrite the User Journey & Phases section from the approved plan
- `--headless` to skip interactive confirmation of the recommended grouping

## When to use

- **Before** writing the journey in `/outcome.create` (create invokes this automatically)
- **After** pulling a kitchen-sink Jira outcome — journey feels thematic but not gap-driven
- **When** review flags Next sizing (too broad, unrelated problems, missing success signal)
- **Not** for splitting unrelated JTBDs across outcomes — use `/outcome.split`

## Prerequisites

- Outcome has at least a **Problem Statement** (context, struggle, goal, personas)
- Evidence section helps but is optional for a first pass

## Behavior

### Step 1: Load outcome

Read the outcome markdown (frontmatter + body). Note `id` from frontmatter.

### Step 2: Atomic capability inventory

Read `docs/outcome-milestone-planning.md` for full rules. Execute:

**Sources (in order):**

0. JTBD context artifact (`artifacts/outcome-originals/<ID>-jtbd-context.md`) — `job_steps` → atomic capability seeds; use when Step 1a ran during create
1. Problem Statement — struggle, goal, Personas (JTBD)
2. Evidence — platform gaps, customer findings
3. Existing User Journey — problem bullets under Next / legacy phases (if refactoring)

When loading from JTBD `job_steps`, set `source` to `Job <id> — <step name>` and keep summaries in problem-space (three-solutions test).

**Per gap, record:**

- `id`: `cap-1`, `cap-2`, …
- `summary`: one-sentence user capability (problem-space)
- `source`: where it came from
- `job_thread`: `primary` or `unrelated` (if unrelated to JTBD → flag for `/outcome.split`, stop planning)
- `delivery_coupled_with`: list of cap ids that must ship with this gap
- `bucket`: `next` or `future` (after grouping)

**Questions (from rfe.split pattern):**

1. Could this ship independently and deliver customer value?
2. Does it require another gap to function at all?
3. Different job thread than adjacent gaps?
4. Would shipping one without the other break the experience? → delivery-coupled
5. Is this near-term (Next) or later (Future)?

**Do not** invent Phase 3 / thematic arcs. Decompose first, then assign each gap to **Next** or **Future** only.

### Step 3: Propose Next vs Future groupings

Propose 1–2 strategies if ambiguous; each strategy must still produce exactly two buckets:

- **Next** — the near-term delivery-coupled slice that delivers customer value soonest
- **Future** — remaining in-scope work that can wait

For Next:

- `problems_addressed` from atomic inventory
- `personas_helped` (actor + experience change; solution-independent)
- `depends_on` / `sequencing_notes` when needed
- `success_signal_sketch` — observable customer value + rough timeframe
- `features_to_deliver` / known source issues

For Future:

- `features_to_deliver` only (no personas, success signal, or scenarios in the outcome body)

Mark one strategy `recommended: true` — prefer the **tightest Next** that still passes sizing checks; park the rest in Future.

Document at least one `rejected_groupings` entry (e.g. multi-phase "Trust/Operate/Observe" arc, or stuffing everything into Next).

### Step 4: Milestone sizing checks

Run on **Next** (Future is a feature backlog — sizing checks apply when promoting Future items into Next later):

| Check | Action if fail |
|-------|----------------|
| **Three-solutions test** on persona/capability language | Rewrite; solution language → linked implementation doc |
| **One-sentence test** | Needs "and" between unrelated scenarios → split outcome or set `expected_rfe_count: "1..N"` / park some gaps in Future |
| **Job thread** | Unrelated problems → `/outcome.split` or move outliers to Future |
| **Delivery coupling** | Prerequisite missing from Next → merge into Next or note sequencing |
| **RFE forecast** | 1–3 related problems → `"1"`; 2+ independent → `"1..N"` or `"2+"` |

### Step 5: Write plan artifact

Write `artifacts/outcome-plans/<OUTCOME-ID>-milestone-plan.yaml` using `templates/milestone-plan-template.yaml`.

Set `status: draft` unless `--apply` will run in this session.

### Step 6: Present recommendation

Unless `--headless`, summarize for the user:

- Atomic capability count
- What lands in Next vs Future
- Next RFE forecast (`expected_rfe_count`)
- Flags for `/outcome.split` if unrelated job threads found

Ask for confirmation before `--apply` unless `--headless`.

### Step 7: Apply (if `--apply`)

Rewrite **only** `## User Journey & Phases` in the outcome file:

- Exactly `### Next` and `### Future` — no other `###` phase headings
- Separate with a horizontal rule (`---`) for Jira rendering
- **Next** order: Features to deliver → Problems to address → Value to personas → Success signal → Scenario(s)
- **Future**: Features to deliver only
- **Features to deliver:** from `features_to_deliver` / `source_issues` — linked bullets; one home per delivery issue across Next/Future. **Apply product overlays** (`docs/product-overlays.md`): for RHAI, include **RHAIRFE only**; omit RHAISTRAT from Features to deliver.
- **Next ranking:** Prefix Next features `(P1)`, `(P2)`, `(P3)`, … by importance to unlock Next (prerequisites / delivery-coupled first, then highest customer-value unlocks). Prefix only — no ranking justification in the outcome. Future features unranked.
- Preserve scenarios that still map to Next; drop scenarios that belonged only to deferred work
- Do not put metrics in Future or Evidence (success signal lives under Next only)

Set plan `status: applied` and `updated` timestamp. Update outcome `updated` in frontmatter.

### Step 8: Next steps

Tell the user:

```
/outcome.review <file>     # includes Next sizing check
/outcome.refine <file>     # if other sections need work
/outcome.export-rfe-batch  # when ready for rfe-creator (exports Next)
```

## Output

- `artifacts/outcome-plans/<ID>-milestone-plan.yaml`
- If `--apply`: updated User Journey section
- Console: Next vs Future summary, RFE forecast, any split warnings

## Integration

- `/outcome.create` — runs this process before writing User Journey (Step 2.5)
- `/outcome.refine` — runs when User Journey is missing, weak, multi-phase, or theme-only
- `/outcome.review` — Step 4.5 validates plan exists or runs sizing checks inline
