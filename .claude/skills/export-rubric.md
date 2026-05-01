# /export-rubric

Export the outcome scoring rubric to a human-readable markdown file.

## Trigger

User says `/export-rubric`

## Behavior

Read the rubric definition from `config/rubric.yaml` and render it as a comprehensive markdown document at `artifacts/outcome-rubric.md`.

The exported rubric includes:
- Overview of the scoring system
- Detailed criteria for each dimension with examples of 0, 1, and 2 scores
- Common anti-patterns to avoid
- The verdict thresholds

## Output

- `artifacts/outcome-rubric.md` — Human-readable rubric document
