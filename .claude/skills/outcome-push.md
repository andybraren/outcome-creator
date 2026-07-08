---
name: outcome.push
description: Resubmit a locally-revised outcome back to CI for re-processing
---
# /outcome.push

Resubmit a locally-revised outcome back to CI for re-processing.

## Trigger

User says `/outcome.push PROJSTRAT-XXXX`

## Behavior

### Step 1: Locate Local Outcome

Find the outcome document in `local/outcome-tasks/` matching the given Jira key.

### Step 2: Validate

Verify:
- The file exists in `local/outcome-tasks/`
- The outcome has been modified since it was pulled (compare timestamps)
- Required sections are present

### Step 3: Update Jira

1. Update the Jira issue description with the revised outcome content
2. Remove the `outcome-creator-needs-attention` label (if present)
3. Add `outcome-creator-resubmitted` label
4. The CI pipeline will pick it up on the next run and re-score

### Step 4: Copy Back to Artifacts

Copy the local files back to `artifacts/` so the CI pipeline has access:
- `local/outcome-tasks/PROJSTRAT-XXXX-*.md` → `artifacts/outcome-tasks/`
- `local/outcome-reviews/PROJSTRAT-XXXX-*` → `artifacts/outcome-reviews/`

### Step 5: Report

Print:
- Updated Jira URL
- Summary of changes
- Note that CI will re-score on next run

## Output

- Updated Jira issue
- Files copied from `local/` to `artifacts/`
- Console confirmation
