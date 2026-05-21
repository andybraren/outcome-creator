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
- Ensure the problem is stated as an explicit JTBD: *When [context], [job executor(s)] need to [job], but [struggle].*
- Name each job executor and their role in the same job — multiple actors on one job is valid
- **JTBD coherence test:** Do all named actors share one job thread? If unrelated jobs are bundled, recommend splitting into sibling outcomes
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

#### End-to-End Customer Arc
- Ensure the story map has 3+ phases with capability statements per relevant actor
- All capability statements must be solution-independent — no product names, feature names, or UI paths
- Ensure 2–3 scenarios, each explicitly tied to a phase (*(Phase: …)*)
- Each scenario must have: actors, context, today's pain, 5–10 step flow, win moment
- **Through-line test:** For each scenario, can you point to the matching phase in the story map and say what capability is now true? If not, fix the map or the scenario
- **Solution-independence test:** Does the arc describe what the customer experiences without referencing the product, features, or technology?

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

#### Release Milestones
- Ensure milestones are customer capability statements — what the customer can do, not what gets built
- **Three-solutions test:** Could engineering achieve each milestone three different ways and still satisfy the statement? If no, rewrite as customer capability
- Verify milestones have a logical sequence based on customer value and dependencies
- Note value dependencies between milestones (e.g., "you need identity before access control is meaningful")
- Each milestone must have a success signal — observable evidence that customer value was delivered
- Story map phases should align with milestones (map = experience, milestones = delivery slices)

#### Downstream Opportunities
- List potential solution directions without committing to any
- Cross-reference existing RFEs that might serve this outcome
- Note open questions that teams should explore during discovery

#### Out of Scope
- Ensure 3+ related but excluded items are named with brief rationale
- Rationale should explain *why* each item is excluded (sibling outcome, future phase, different team, out of control, etc.)
- Vague exclusions ("performance optimization is out of scope") need to name what's specifically excluded
- **Readiness test:** Could an engineer answer the first 10 "are we doing X?" questions using the out-of-scope statement alone?

#### Acceptance Signals
- Ensure signals are observable and time-bound where possible
- Include both quantitative signals (metrics, conversion rates) and qualitative signals (user feedback themes, support ticket patterns)
- Verify that acceptance signals connect back to the product outcome metrics
- **Milestone-level signals required:** Each release milestone needs its own success signal (in the Milestones section). Outcome-level signals alone score partial on measurability.
- Signals in Release Milestones and Acceptance Signals must be consistent — milestone signals are checkpoints, outcome-level signals are the finish line

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
