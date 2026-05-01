# /outcome.signoff

Sign off a rubric-pass outcome as ready for downstream work (RFE creation, strategy planning).

## Trigger

User says `/outcome.signoff PROJSTRAT-XXXX`

## Behavior

### Step 1: Locate Outcome

Find the outcome document in `local/outcome-tasks/` or `artifacts/outcome-tasks/` matching the given Jira key.

### Step 2: Validate Readiness

Verify:
- The outcome has `outcome-creator-rubric-pass` label (or total score ≥ 6 with no zeros)
- All required sections are complete
- At least one strategic goal is linked

If the outcome has `outcome-creator-needs-attention`, warn the reviewer and ask for confirmation.

### Step 3: Collect Sign-off

Record:
- Reviewer identity (from environment or prompt)
- Date of sign-off
- Any reviewer notes or conditions

### Step 4: Update Status

1. Update the outcome document status to `approved`
2. Update Jira:
   - Transition status to "In Progress" or "Active" (configurable)
   - Add `outcome-creator-signed-off` label
   - Remove `outcome-creator-rubric-pass` label
   - Add a comment with the sign-off record

### Step 5: Report

Print:
- Outcome title and Jira key
- Final scores
- Sign-off details
- Next steps: "This outcome is now ready for RFE creation and strategy planning"

## Output

- Updated outcome document with `approved` status
- Updated Jira issue with sign-off labels and comment
- Console confirmation with next steps
