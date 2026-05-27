# /outcome.create

Create a new outcome from strategic goals, research, and/or a problem statement.

## Trigger

User says `/outcome.create` optionally followed by:
- A problem statement or strategic theme description
- `--strategic-goal PROJGOALS-XXX` to anchor to a specific strategic goal
- `--headless` to skip clarifying questions (for batch/CI use)
- `--input batch.yaml` to create multiple outcomes from a YAML file

## Behavior

### Step 1: Gather Context

If `--headless` is NOT set, ask up to 5 clarifying questions to understand:

1. **Strategic anchor**: Which strategic goal(s) does this outcome relate to? If a PROJGOALS key is provided, fetch it from Jira using the Atlassian MCP or REST API fallback.
2. **User need / JTBD**: What job is the user trying to get done? Who are the job executors? What context triggers the job? What struggle makes it hard today? (Multiple actors sharing one job is fine — flag unrelated jobs for sibling outcomes.)
3. **Business context**: How does solving this benefit the organization? What business metric would improve?
4. **Evidence**: What research, customer feedback, or data supports this need?
5. **Scope**: Is this a broad thematic outcome or a focused product-level outcome?

If `--headless` IS set, derive answers from the input prompt and any `--strategic-goal` context.

### Step 2: Bootstrap Rubric

Check if `artifacts/outcome-rubric.md` exists. If not, run the `export-rubric` skill to generate it. Use the rubric to guide outcome creation — ensure each section addresses what the rubric scores.

### Step 3: Create Outcome Document

Write the outcome to `artifacts/outcome-tasks/OUTCOME-NNN-<slug>.md` using the template from `templates/outcome-template.md`.

The document MUST include these sections only (lean structure — avoid redundant restatements):

1. **Problem Statement** — JTBD only: job, context, struggle, who is involved. No customer quotes, no named accounts, no solution language.
2. **Success & Metrics** — Lagging (business) and leading (product) indicators in one place. Do not duplicate per-phase success signals here.
3. **Customer Arc & Delivery Plan** — Combined arc and milestones. For each phase (3+ for long-lived outcomes):
   - Customer capability headline (three-solutions test)
   - When this is true (actor capabilities, solution-independent)
   - Success signal with target timeframe
   - Problems this phase addresses (value dependencies noted)
   - 2–3 scenarios nested under relevant phases: Actors, Context, Flow, Win moment — **no Today's pain** (Problem + Evidence cover that)
4. **Evidence** — Customer quotes, analyst/market data, platform gaps, one-line opportunity verdict. No separate Opportunity Assessment section.
5. **Example Implementation & Open Questions** — Author's solution sketch (illustrative) plus open questions per capability area. No separate Downstream Opportunities section.
6. **Out of Scope** — 3+ related exclusions with brief rationale

Do NOT create: User Outcome, Product Outcome, Business Outcome (as separate sections), End-to-End Customer Arc, Story Map, Release Milestones, Opportunity Assessment, Downstream Opportunities, or Acceptance Signals.

### Step 4: Write Frontmatter

Add YAML frontmatter with:
```yaml
---
id: OUTCOME-NNN
title: "Descriptive title"
status: draft
strategic_goals: [PROJGOALS-XXX]
components: []
priority: Critical | Major | Minor
score: null
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

### Step 5: Save Input Snapshot

Save the original inputs (strategic goal data, research excerpts, user prompt) to `artifacts/outcome-originals/OUTCOME-NNN-inputs.md` for traceability.

## Output

- `artifacts/outcome-tasks/OUTCOME-NNN-<slug>.md` — The outcome document
- `artifacts/outcome-originals/OUTCOME-NNN-inputs.md` — Input snapshot
- Console summary of what was created

## Quality Guidelines

**Do:**
- Write problem-framed statements that pass the three-solutions test in Problem Statement and Customer Arc phases
- Put all customer quotes and named accounts in Evidence (once)
- Put solution language only in Example Implementation & Open Questions
- Preserve the author's solution thinking when converting from Jira — move it, don't delete it

**Don't:**
- Repeat the same metric in Success & Metrics and phase success signals (outcome-level vs phase-level only)
- Repeat customer quotes in Problem Statement and scenarios
- Add "Today's pain" to scenarios when Problem Statement and Evidence already describe the struggle
- Create legacy sections (User Outcome, separate milestones, Acceptance Signals) — use the lean template
