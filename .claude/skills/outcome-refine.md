---
name: outcome.refine
description: Refine an existing outcome document with additional research and structural improvements
---
# /outcome.refine

Refine an existing outcome document with additional research, data, and structural improvements.

## Trigger

User says `/outcome.refine` optionally followed by:
- A path to a specific outcome file in `artifacts/outcome-tasks/` or `local/outcome-tasks/`
- `--headless` to skip interactive prompts

## Behavior

### Step 1: Locate Outcome

1. If a specific file path is given, use it.
2. If in `local/outcome-tasks/`, operate in local mode (skip Jira writes).
3. If no path given, list available outcomes in `artifacts/outcome-tasks/` and `local/outcome-tasks/` and ask which to refine.

### Step 2: Read Current State

Read the outcome document and its frontmatter. Read the original inputs from `artifacts/outcome-originals/` or `local/outcome-originals/` if available. If `<ID>-jtbd-context.md` exists, use it to enrich Evidence (OpScores, verbatim quotes with citations) without duplicating content already in the outcome.

### Step 3: Consolidate to Lean Structure

If the document uses legacy sections, migrate content without losing information:

| Legacy section | Merge into |
|---|---|
| Business Outcome + Product Outcome + Success & Metrics | User Journey phase success signals (lagging in later phases, leading in early) — then delete legacy sections |
| User Outcome | Problem Statement (who) + User Journey (capabilities) — then delete User Outcome |
| End-to-End Customer Arc + Story Map + Release Milestones | User Journey & Milestones (one phase block per delivery slice) |
| Opportunity Assessment | Evidence (one-line opportunity verdict) |
| Downstream Opportunities | Open Questions (questions only) + Related Resources (link to implementation doc with solution details) |
| Example Implementation (inline) | Open Questions (extract questions) + Related Resources (link to implementation doc with solution details) |
| Acceptance Signals | Merge into nearest phase success signals — delete duplicate Measurement Timeframe |

### Step 4: Refine Each Section

#### Problem Statement
- JTBD only: job, context, struggle, who is involved (one sub-bullet per job executor — role and what they own)
- **JTBD coherence test:** Do all named actors share one job thread?
- Move customer quotes and named accounts to Evidence
- Remove solution language — move to a linked implementation doc (add link in Related Resources)

#### User Journey & Milestones

If a **Success & Metrics** section exists, migrate lagging/leading indicators into phase success signals (early phases = leading, final phase(s) = outcome-level lagging), then delete Success & Metrics.


If phases are missing, theme-only, or bundle unrelated problems:

1. Run `/outcome.plan-milestones` (see `docs/outcome-milestone-planning.md`) — atomic inventory, delivery-coupling, sizing checks.
2. Apply with `--apply` or rewrite phases from `artifacts/outcome-plans/<ID>-milestone-plan.yaml`.

Otherwise refine in place:

- Each phase: user capability, when this is true, success signal (with timeframe), problems addressed
- **Three-solutions test** on every user capability headline
- **Milestone sizing:** one-sentence test per phase; flag phases with `expected_rfe_count: 1..N` in plan
- Scenarios: Actors, Context, Flow, Win moment only — remove Today's pain if present
- **Through-line test:** Each scenario demonstrates a capability from its phase

#### Evidence
- Customer quotes, analyst data, platform gaps — single home for all proof points
- **Cite every quote, statistic, and external claim** — include source name and link or document reference; verify quote and URL match exactly
- End with one-line opportunity verdict (importance vs satisfaction)
- Remove duplicate quotes from other sections after consolidating here

#### Open Questions
- Discovery questions per capability area — what engineering and product still need to decide
- Extract questions from any legacy Example Implementation section
- Remove separate Downstream Opportunities list if redundant (capture as questions or links)

#### Related Resources
- Link to implementation sketch, design/prototype, evidence deep-dive, and other collaborative docs
- Move solution language from Problem Statement, phases, or legacy Example Implementation into a linked implementation doc (don't delete — preserve the author's thinking)
- Ensure at least an implementation sketch link is present

#### Out of Scope
- 3+ exclusions with rationale
- **Readiness test:** Could an engineer answer "are we doing X?" from this list alone?

### Step 5: Redundancy Pass

Before finishing, check for and remove:
- Same quote in Problem Statement and Evidence
- Same metric repeated verbatim in multiple phase success signals (keep one home per metric)
- Same capability stated in a phase headline and "When this is true" bullets (tighten, don't repeat)
- Separate Story Map + Milestones + Acceptance Signals sections (must be one User Journey & Milestones)

### Step 6: Update Frontmatter

Update the `updated` timestamp. If components or strategic goals changed, update those too.

### Step 7: Write Refined Document

Overwrite the outcome file with the refined version. Write a summary of changes to stdout.

## Local Mode Detection

If the outcome file is in `local/outcome-tasks/`, the skill operates in local mode:
- Reads from and writes to `local/` instead of `artifacts/`
- Skips any Jira API calls
- Does not update pipeline labels

## Output

- Updated outcome document in the same location
- Console summary of refinements applied
