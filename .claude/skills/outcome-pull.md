# /outcome.pull

Pull a post-CI outcome from Jira into the local/ workspace for human review.

## Trigger

User says `/outcome.pull PROJSTRAT-XXXX`

## Behavior

### Step 1: Fetch from Jira

Fetch the outcome issue from Jira using the Atlassian MCP or REST API fallback (`scripts/pull_outcome.py`).

### Step 2: Convert to Outcome Document

Parse the Jira issue and convert it to the standard outcome document format:
- Extract title, description, priority, components, labels, status
- Parse the description body into sections (Problem Statement, Business Outcome, User Outcome, Product Outcome, etc.)
- Build frontmatter from Jira fields

### Step 3: Write to Local Workspace

Write the outcome document to `local/outcome-tasks/PROJSTRAT-XXXX-<slug>.md`.

If review artifacts exist in `artifacts/outcome-reviews/`, copy them to `local/outcome-reviews/`.

If original input snapshots exist in `artifacts/outcome-originals/`, copy them to `local/outcome-originals/`.

### Step 4: Report

Print:
- File location
- Current score (if available)
- Current verdict
- Suggested next step (`/outcome.refine` or `/outcome.signoff`)

## Output

- `local/outcome-tasks/PROJSTRAT-XXXX-<slug>.md` — The outcome document
- `local/outcome-reviews/` — Any existing review files (copied)
- `local/outcome-originals/` — Input snapshots (copied)
