# /outcome.submit

Submit a new outcome to Jira or update an existing one.

## Trigger

User says `/outcome.submit` optionally followed by:
- A path to a specific outcome file
- `--dry-run` to validate without writing to Jira
- `--update PROJSTRAT-XXXX` to update an existing issue

## Behavior

### Step 1: Locate Outcome

1. If a file path is given, use it.
2. If none, list available outcomes in `artifacts/outcome-tasks/` and ask which to submit.
3. Read the outcome document and its frontmatter.

### Step 2: Validate

Before submission, validate:
- All required sections are present (Problem Statement, Success & Metrics, Customer Arc & Delivery Plan, Evidence, Example Implementation & Open Questions, Out of Scope) — or legacy equivalents that `/outcome.refine` can migrate
- Frontmatter has required fields (title, strategic_goals, priority)
- If scored, verdict is at least REVISE (warn if submitting a REWORK)
- Strategic goal references are valid PROJGOALS keys

### Step 3: Construct Jira Payload

Map the outcome document to Jira fields:

```
Project: PROJSTRAT (or configurable via pipeline-settings.yaml)
Issue Type: Outcome
Summary: {title}
Priority: {priority}
Components: {components}
Labels: [outcome-creator-auto-created] + any pipeline labels
Description: {full markdown body}
Links:
  - "is part of" → {strategic_goals} (PROJGOALS issues)
```

### Step 4: Submit or Update

**New outcome** (`--update` not provided):
- Create the issue via Jira REST API
- Update the outcome document's frontmatter with the new Jira key
- Add `outcome-creator-auto-created` label

**Update existing** (`--update PROJSTRAT-XXXX`):
- Update the issue description, priority, components, and labels
- Preserve any manually-added labels or fields
- Add `outcome-creator-auto-updated` label

**Dry run** (`--dry-run`):
- Print the Jira payload that would be submitted
- Validate all fields
- Do not write to Jira

### Step 5: Link to Strategic Goals

For each strategic goal in `strategic_goals`:
- Create an "is part of" link from the outcome to the PROJGOALS issue
- This establishes the outcome → strategic goal traceability

### Step 6: Update Local File

After successful submission:
- Update frontmatter with Jira key and URL
- Update status to `review` (for new) or keep current status (for updates)
- Update the `updated` timestamp

## Environment Variables

```
JIRA_SERVER — Jira instance URL
JIRA_USER — Email address for API auth
JIRA_TOKEN — API token
```

## Output

- Console confirmation with Jira key and URL
- Updated outcome document with Jira metadata in frontmatter
