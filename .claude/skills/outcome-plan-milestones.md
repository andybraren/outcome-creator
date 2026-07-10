# /outcome.plan-milestones

Plan or refactor **User Journey** milestones using bottom-up capability inventory and delivery-coupling rules (adapted from [rfe-creator `/rfe.split`](https://github.com/jwforres/rfe-creator)).

## Trigger

User says `/outcome.plan-milestones` optionally followed by:

- A path to an outcome file in `artifacts/outcome-tasks/` or `local/outcome-tasks/`
- `--apply` to rewrite the User Journey & Phases section from the approved plan
- `--headless` to skip interactive confirmation of the recommended grouping

## When to use

- **Before** writing phases in `/outcome.create` (create invokes this automatically)
- **After** pulling a kitchen-sink Jira outcome — phases feel thematic but not gap-driven
- **When** review flags milestone sizing (broad phase, unrelated problems, missing sequencing)
- **Not** for splitting unrelated JTBDs across outcomes — use `/outcome.split`

## Prerequisites

- Outcome has at least a **Problem Statement** (JTBD, struggle, who is involved)
- Evidence section helps but is optional for a first pass

## Behavior

### Step 1: Load outcome

Read the outcome markdown (frontmatter + body). Note `id` from frontmatter.

### Step 2: Atomic capability inventory

Read `docs/outcome-milestone-planning.md` for full rules. Execute:

**Sources (in order):**

0. JTBD context artifact (`artifacts/outcome-originals/<ID>-jtbd-context.md`) — `job_steps` → atomic capability seeds; use when Step 1a ran during create
1. Problem Statement — struggle bullets, who is involved
2. Evidence — platform gaps, customer findings
3. Existing User Journey — problem bullets per phase (if refactoring)

When loading from JTBD `job_steps`, set `source` to `Job <id> — <step name>` and keep summaries in problem-space (three-solutions test).

**Per gap, record:**

- `id`: `cap-1`, `cap-2`, …
- `summary`: one-sentence user capability (problem-space)
- `source`: where it came from
- `job_thread`: `primary` or `unrelated` (if unrelated to JTBD → flag for `/outcome.split`, stop planning)
- `delivery_coupled_with`: list of cap ids that must ship with this gap

**Questions (from rfe.split pattern):**

1. Could this ship independently and deliver customer value?
2. Does it require another gap to function at all?
3. Different job thread than adjacent gaps?
4. Would shipping one without the other break the experience? → delivery-coupled

**Do not** start from existing phase theme names. Decompose first, then group.

### Step 3: Propose 2–3 milestone grouping strategies

For each strategy:

- How many milestones
- Which `atomic_capability_ids` per milestone
- One-sentence `capability_headline` per milestone
- `depends_on` and `sequencing_notes`
- `success_signal_sketch` per milestone

Mark one strategy `recommended: true` — prefer the **fewest milestones** where each still passes sizing checks.

Document at least one `rejected_groupings` entry (e.g. theme-only "Trust/Operate/Observe" without gap analysis).

### Step 4: Milestone sizing checks

For each milestone in the recommended strategy, run:

| Check | Action if fail |
|-------|----------------|
| **Three-solutions test** on `capability_headline` | Rewrite; solution language → linked implementation doc |
| **One-sentence test** | Needs "and" between unrelated scenarios → split milestone or set `expected_rfe_count: "1..N"` |
| **Job thread** | Unrelated problems → separate milestones or `/outcome.split` |
| **Delivery coupling** | Prerequisite in wrong milestone → merge or fix `depends_on` |
| **RFE forecast** | 1–3 related problems → `"1"`; 2+ independent → `"1..N"` or `"2+"` |

### Step 5: Write plan artifact

Write `artifacts/outcome-plans/<OUTCOME-ID>-milestone-plan.yaml` using `templates/milestone-plan-template.yaml`.

Set `status: draft` unless `--apply` will run in this session.

### Step 6: Present recommendation

Unless `--headless`, summarize for the user:

- Atomic capability count
- Recommended milestone count and names
- Sequencing (phase order + dependencies)
- Any milestone with `expected_rfe_count` > 1
- Flags for `/outcome.split` if unrelated job threads found

Ask for confirmation before `--apply` unless `--headless`.

### Step 7: Apply (if `--apply`)

Rewrite **only** `## User Journey & Phases` in the outcome file:

- `### Phase N: <name>` per planned milestone
- Separate consecutive phases with a horizontal rule (`---`) for Jira rendering
- **User capability:** from `capability_headline`
- **When this is true:** actor bullets derived from capabilities (solution-independent)
- **Success signal:** from `success_signal_sketch`
- **Problems this phase addresses:** from `problems_addressed`; inline `*(sequencing note)*` from `sequencing_notes`
- **Features to deliver:** from `features_to_deliver` / `source_issues` on atomic capabilities — linked `[KEY](url) — summary` bullets; one home per issue across phases
- Preserve existing scenarios where they still map to a phase; add/move scenarios if needed (2–3 total across arc)
- Do not duplicate content into phase success signals or Evidence (metrics belong in phase success signals only)

Set plan `status: applied` and `updated` timestamp. Update outcome `updated` in frontmatter.

### Step 8: Next steps

Tell the user:

```
/outcome.review <file>     # includes milestone sizing check
/outcome.refine <file>     # if other sections need work
/outcome.export-rfe-batch  # when ready for rfe-creator
```

## Output

- `artifacts/outcome-plans/<ID>-milestone-plan.yaml`
- If `--apply`: updated User Journey section
- Console: milestone count, RFE forecast summary, any split warnings

## Integration

- `/outcome.create` — runs this process before writing User Journey (Step 2.5)
- `/outcome.refine` — runs when User Journey is missing, weak, or theme-only
- `/outcome.review` — Step 4.5 validates plan exists or runs sizing checks inline
