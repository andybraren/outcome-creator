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
2. **User need**: What user problem or unmet need does this address? Who specifically is affected?
3. **Business context**: How does solving this benefit the organization? What business metric would improve?
4. **Evidence**: What research, customer feedback, or data supports this need?
5. **Scope**: Is this a broad thematic outcome or a focused product-level outcome?

If `--headless` IS set, derive answers from the input prompt and any `--strategic-goal` context.

### Step 2: Bootstrap Rubric

Check if `artifacts/outcome-rubric.md` exists. If not, run the `export-rubric` skill to generate it. Use the rubric to guide outcome creation — ensure each section addresses what the rubric scores.

### Step 3: Create Outcome Document

Write the outcome to `artifacts/outcome-tasks/OUTCOME-NNN-<slug>.md` using the template from `templates/outcome-template.md`.

The document MUST include all sections:

1. **Problem Statement** — The user/market need, grounded in evidence
2. **Business Outcome** — How the business benefits (lagging indicator)
   - Metric or directional indicator
   - Connection to strategic goals
   - Expected business impact
3. **User Outcome** — What users can do/feel differently
   - User outcome statements using importance/satisfaction framing
   - Who benefits (persona or segment)
   - What changes in their day-to-day
4. **Product Outcome** — Measurable behavior change in the product (leading indicator)
   - Specific product metrics or behavioral changes
   - How this connects to the user outcome
5. **Evidence & Research** — Data supporting this outcome
6. **Opportunity Assessment** — How underserved is this today
7. **Downstream Opportunities** — Potential solution directions (not commitments)
8. **Acceptance Signals** — How we'll know the outcome is being achieved

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
- Write outcome statements that are solution-agnostic
- Ground every claim in evidence or clearly mark assumptions
- Make user outcomes specific to a persona or user segment
- Ensure business outcomes connect to at least one strategic goal
- Include both quantitative and qualitative acceptance signals

**Don't:**
- Describe features or solutions (that's for RFEs and strategies)
- Use vague language like "improve the experience" without specifics
- Set unrealistic or unmeasurable acceptance criteria
- Combine multiple unrelated outcomes into one document
- Skip the evidence section — even thin evidence is better than none
