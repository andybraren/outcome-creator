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

Read the outcome document and its frontmatter. Read the original inputs from `artifacts/outcome-originals/` or `local/outcome-originals/` if available.

### Step 3: Refine Each Section

For each section, apply the following refinement logic:

#### Problem Statement
- Sharpen the problem definition with specific user pain points
- Add concrete scenarios or quotes if available
- Ensure the problem is framed around the user need, not a missing feature

#### Business Outcome
- Verify connection to strategic goals — fetch the PROJGOALS issue if needed
- Add or refine metrics (revenue impact, cost reduction, adoption targets)
- Distinguish between leading and lagging indicators
- Ensure the business outcome is a real outcome, not an output disguised as one

#### User Outcome
- Apply the user outcome statement format: "Minimize/Maximize [direction] the [metric] of [task/activity]"
- Add importance and satisfaction framing where research data is available
- Ensure the user outcome describes a change in capability or experience, not a feature
- Validate that the stated persona or segment is specific enough to be actionable
- Check: "Is it possible to have a happy customer who never uses a specific feature we'd build?" — if yes, the outcome is well-framed

#### Product Outcome
- Ensure product outcomes are leading indicators of business outcomes
- Add specific, measurable product metrics (not traction metrics for single features)
- Verify product outcomes span features — they should describe value, not adoption of one tool
- Pair sentiment metrics (satisfaction) with behavioral metrics (engagement, completion)

#### Evidence & Research
- Integrate any new research or customer data
- Structure evidence by type: customer quotes, survey data, telemetry, analyst reports
- Flag gaps in evidence that need further research

#### Opportunity Assessment
- Calculate or refine the opportunity score if importance/satisfaction data exists
- Categorize: Underserved, Overserved, Appropriately-served, Table Stakes
- Note if this is a new assessment or a revision of a previous one

#### Downstream Opportunities
- List potential solution directions without committing to any
- Cross-reference existing RFEs that might serve this outcome
- Note open questions that teams should explore during discovery

#### Acceptance Signals
- Ensure signals are observable and time-bound where possible
- Include both quantitative signals (metrics, conversion rates) and qualitative signals (user feedback themes, support ticket patterns)
- Verify that acceptance signals connect back to the product outcome metrics

### Step 4: Update Frontmatter

Update the `updated` timestamp. If components or strategic goals changed, update those too.

### Step 5: Write Refined Document

Overwrite the outcome file with the refined version. Write a summary of changes to stdout.

## Local Mode Detection

If the outcome file is in `local/outcome-tasks/`, the skill operates in local mode:
- Reads from and writes to `local/` instead of `artifacts/`
- Skips any Jira API calls
- Does not update pipeline labels

## Output

- Updated outcome document in the same location
- Console summary of refinements applied
