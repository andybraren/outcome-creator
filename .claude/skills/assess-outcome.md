---
name: assess-outcome
description: Score a single outcome or directory of outcomes against the quality rubric
---
# /assess-outcome

Score a single outcome or directory of outcomes against the quality rubric.

## Trigger

User says `/assess-outcome` optionally followed by:
- A path to a specific outcome file
- A path to a directory containing outcome files
- `--format json` to output scores as JSON (for CI integration)

## Behavior

### Step 1: Locate Outcomes

1. If a specific file is given, score that file.
2. If a directory is given, score all `.md` files in it.
3. If neither, score all files in `artifacts/outcome-tasks/`.

### Step 2: Score Each Outcome

For each outcome, invoke the `outcome-scorer` agent to evaluate across 4 dimensions:

| Dimension | Weight | Scoring Criteria |
|-----------|--------|------------------|
| Measurability | 0–2 | Clear metrics, directional indicators, observable acceptance signals |
| User Focus | 0–2 | Specific persona, real user need, meaningful capability change |
| Business Alignment | 0–2 | Strategic goal connection, substantiated business value |
| Actionability | 0–2 | Well-scoped, clear downstream opportunities, identified open questions |

### Step 3: Generate Summary

For each outcome, output:
- Title and ID
- Per-dimension scores
- Total score
- Verdict: PASS (8), REVISE (6–7), REWORK (<6)
- Top issues (if any)

### Step 4: Aggregate (directory mode)

If scoring multiple outcomes:
- Average scores per dimension
- Count of PASS / REVISE / REWORK
- Identify systematic weaknesses across the set

## Output Formats

**Console (default):**
```
OUTCOME-001: "Deploy Agents Confidently" — 7/8 (REVISE)
  Measurability: 2/2  User Focus: 1/2  Business: 2/2  Actionability: 2/2
  Issue: User outcome is generic — needs specific persona

OUTCOME-002: "Reduce Agent Debugging Time" — 8/8 (PASS)
  Measurability: 2/2  User Focus: 2/2  Business: 2/2  Actionability: 2/2
```

**JSON (`--format json`):**
```json
[
  {
    "id": "OUTCOME-001",
    "title": "Deploy Agents Confidently",
    "scores": { "measurability": 2, "user_focus": 1, "business_alignment": 2, "actionability": 2 },
    "total": 7,
    "verdict": "REVISE",
    "issues": ["User outcome is generic — needs specific persona"]
  }
]
```
