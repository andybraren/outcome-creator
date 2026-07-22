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
| Business Outcome + Product Outcome + Success & Metrics | Next **Success signal** (leading and/or lagging as appropriate) — then delete legacy sections |
| User Outcome | Problem Statement (who) + Next **Personas this helps** — then delete User Outcome |
| End-to-End Customer Arc + Story Map + Release Milestones | User Journey & Phases (`### Next` + `### Future` only) |
| Multi-phase arcs (Phase 1/2/3/4, thematic Trust/Operate/…) | Collapse near-term into **Next**; park later features under **Future** |
| Opportunity Assessment | Evidence (one-line opportunity verdict) |
| Downstream Opportunities | Open Questions (questions only) + Related Resources (link to implementation doc with solution details) |
| Example Implementation (inline) | Open Questions (extract questions) + Related Resources (link to implementation doc with solution details) |
| Acceptance Signals | Merge into Next success signal — delete duplicate Measurement Timeframe |
| User capability / When this is true | Merge into **Personas this helps** (drop duplicate capability headline) |
| Out of Scope | Drop the section. Park deferred work under **Future**; note sibling/split follow-ups in Related Resources or Open Questions if still useful |

### Step 4: Refine Each Section

#### Problem Statement
- Order: Context → Struggle → Goal → Personas (JTBD)
- **Goal:** org-level enablement for customers as a whole (migrated from legacy Job (JTBD) when present)
- **Personas (JTBD):** one sub-bullet per persona with their job-to-be-done (merge legacy Who is involved + per-actor JTBD)
- **JTBD coherence test:** Do all named personas share one job thread?
- Move customer quotes and named accounts to Evidence
- Remove solution language — move to a linked implementation doc (add link in Related Resources)

#### User Journey & Phases

If a **Success & Metrics** section exists, migrate indicators into Next **Success signal**, then delete Success & Metrics.

If the journey has more than Next + Future, is missing subsections, is theme-only, or bundles unrelated problems into Next:

1. Run `/outcome.plan-milestones` (see `docs/outcome-milestone-planning.md`) — atomic inventory, Next vs Future assignment, sizing checks.
2. Apply with `--apply` or rewrite from `artifacts/outcome-plans/<ID>-milestone-plan.yaml`.

Otherwise refine in place:

- **Enforce structure:** only `### Next` and `### Future` — collapse extra phases into these two
- **Next** order: Features to deliver → Problems to address → Value to personas → Success signal → Scenario(s)
- **Future:** Features to deliver only (strip problems, personas, success signals, scenarios if present)
- Separate Next and Future with a horizontal rule (`---`) for Jira rendering
- **Features to deliver:** If Jira keys are buried in problem bullets, Evidence, or Related Resources, move delivery-scoped keys into the appropriate bucket's list as `[KEY](url) — summary`. Keep problem bullets problem-framed. Every in-scope **delivery** issue appears in exactly one of Next or Future. **Apply product overlays** (`docs/product-overlays.md`): for RHAI, keep **RHAIRFE only** in Features to deliver; omit RHAISTRAT from that list (prefer RFE when both exist for the same work; do not relocate STRATs to Related Resources solely because they were excluded).
- **Next feature ranking:** Rank-order Next features as `(P1)`, `(P2)`, `(P3)`, … based on what most unlocks Next problems / personas / success signal (prerequisites and delivery coupling first). Prefix only — do **not** write ranking justification. Future features do not need P-ranks.
- **Three-solutions test** on Value to personas language
- **Milestone sizing:** one-sentence test on Next; flag `expected_rfe_count: 1..N` in plan when needed
- Scenarios only under Next: Actors, Context, Flow, Win moment — remove Today's pain if present
- **Through-line test:** Each scenario demonstrates a Next persona capability

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

### Step 5: Redundancy Pass

Before finishing, check for and remove:
- Same quote in Problem Statement and Evidence
- Duplicate User capability + Value to personas (keep Value to personas only)
- Problems, personas, success signals, or scenarios under Future
- Extra phase headings beyond Next and Future
- Separate Story Map + Milestones + Acceptance Signals sections (must be one Phases section)
- Product-overlay violations (e.g. RHAI outcome listing RHAISTRAT under Features to deliver)
- Legacy **Out of Scope** section (drop; park deferred work under Future)

### Step 6: Update Frontmatter

Update the `updated` timestamp. If components or strategic goals changed, update those too.

**Title check:** If `title` is longer than ~5 words (or reads like a full experience / metrics sentence), shorten it to a colloquial ≤5-word shorthand suitable as a Jira Summary — same Title rules as `/outcome.create`. Keep the fuller wording in Goal / Phases; do not drop meaning from the body when shortening the title.

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
