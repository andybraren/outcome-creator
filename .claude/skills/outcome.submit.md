---
name: outcome.submit
description: Submit a new outcome to Jira or update an existing one
---
# /outcome.submit

Submit a new outcome to Jira or update an existing one.

## Trigger

User says `/outcome.submit` optionally followed by:
- A path to a specific outcome file
- `--dry-run` to validate without writing to Jira
- `--update PROJSTRAT-XXXX` to update an existing issue
- `--no-verification-story` to skip creating the post-release verification story

## Behavior

### Step 1: Locate Outcome

1. If a file path is given, use it.
2. If none, list available outcomes in `artifacts/outcome-tasks/` and ask which to submit.
3. Read the outcome document and its frontmatter.

### Step 2: Validate

Before submission, validate:
- Required sections: Problem Statement, User Journey & Phases, Evidence, Open Questions, Related Resources
- Success metrics live in phase success signals only (no separate Success & Metrics section)
- Frontmatter has required fields (title, strategic_goals, priority)
- **Title length:** Prefer ≤5 words (Jira Summary). If longer, warn and offer to shorten before submit unless the user opted into a longer title
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

Links are created for keys already in frontmatter — the pipeline does not auto-discover or suggest strategic goal issues from outcome content (follow-up).

### Step 6: Create Success Verification Story

After successful creation of a **new** outcome (not updates), check `config/pipeline-settings.yaml` → `success_verification.enabled`. If enabled (the default):

1. Create a child Story under the newly-created outcome issue:
   - **Issue type:** from `success_verification.issue_type` (default: Story)
   - **Summary:** from `success_verification.title` (default: "Post-release: verify outcome success achievement")
   - **Description:** from `success_verification.description` — a reminder to check whether the **Next** success signal is being met after release
   - **Parent:** the outcome issue just created (via `parent` field in Jira — hierarchy link)
   - **Labels:** `[outcome-creator-auto-created]`
2. Log the created story key to the console

This story serves as a team reminder: shipping Next features is not done until we verify the Next success signal was actually achieved. The story should remain open until the team has checked in against that criteria post-release. Do not put this reminder text in the outcome template body.

Skip this step if:
- `--update` was provided (existing outcome)
- `success_verification.enabled` is `false`
- `--no-verification-story` flag was passed

### Step 7: Update Local File

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
- Console confirmation of verification story key (if created)
- Updated outcome document with Jira metadata in frontmatter
