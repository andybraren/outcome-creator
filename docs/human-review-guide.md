# Human Review Guide

This guide walks through the human review workflow for outcomes that have been through the CI pipeline.

## When to Review

After the CI pipeline runs `outcome-create` → `outcome-refine` → `outcome-review`, each outcome gets a verdict:

| Verdict | Label | What It Means |
|---------|-------|---------------|
| **PASS** (8/8) | `outcome-creator-rubric-pass` | Pipeline thinks it's ready. A human should validate and sign off. |
| **REVISE** (6–7/8) | `outcome-creator-needs-attention` | Targeted issues need fixing. Pull, fix, push back. |
| **REWORK** (<6/8) | `outcome-creator-needs-attention` | Fundamental problems. May need to be rewritten from scratch. |

## Workflow: Rubric Pass Outcomes

These outcomes scored well in CI. Your job is to validate that the scores are justified and sign off.

```bash
# 1. Pull the outcome into your local workspace
/outcome.pull PROJSTRAT-1344

# 2. Read the outcome and review files
#    - local/outcome-tasks/PROJSTRAT-1344-*.md (the outcome)
#    - local/outcome-reviews/PROJSTRAT-1344-*.md (reviewer findings)

# 3. Check each dimension:
#    - Measurability: Are these real metrics you could actually track?
#    - User Focus: Would a real user recognize this as their problem?
#    - Business Alignment: Does the strategic connection hold up?
#    - Actionability: Could your team start discovery tomorrow?

# 4. If satisfied, sign off
/outcome.signoff PROJSTRAT-1344

# 5. If not satisfied, refine and push back
/outcome.refine
/outcome.review
/outcome.push PROJSTRAT-1344
```

## Workflow: Needs Attention Outcomes

These outcomes have specific issues flagged by reviewers. Read the review files to understand what's wrong.

```bash
# 1. Pull the outcome
/outcome.pull PROJSTRAT-1344

# 2. Read the review files to understand issues
#    Each dimension has its own review file with:
#    - Score and justification
#    - Specific issues found
#    - Recommendations for improvement

# 3. Fix the issues
#    Edit local/outcome-tasks/PROJSTRAT-1344-*.md directly,
#    or use /outcome.refine to have Claude help

# 4. Re-score locally
/outcome.review

# 5. If now passing, push back for CI re-scoring
/outcome.push PROJSTRAT-1344

# 6. Wait for CI to confirm, then sign off
/outcome.signoff PROJSTRAT-1344
```

## What to Look For

### Measurability
- Can you actually measure these metrics with tools you have?
- Do baselines exist, or would you need to establish them first?
- Are the acceptance signals things you'd genuinely check in 3–6 months?

### User Focus
- Is the persona specific enough? "AI engineers" is borderline — "AI engineers debugging agent failures in production" is better.
- Would you bring this outcome statement to a user interview and have them nod in recognition?
- Is this outcome solution-agnostic? Could you imagine 3 different features that might serve it?

### Business Alignment
- Does the strategic goal connection feel genuine, or was it bolted on?
- Would a product leader look at this and say "yes, this is what we need to focus on"?
- Is the business metric one that leadership actually tracks?

### Actionability
- If you handed this to a product trio, could they start discovery this sprint?
- Are the downstream opportunities realistic starting points?
- Are the open questions the *right* questions — things that would actually change your approach if answered differently?

## Common Issues and Fixes

| Issue | Fix |
|-------|-----|
| Outcome reads like a feature request | Rewrite to focus on the user need, not the solution. Ask "why does the user want this?" and write that instead. |
| Metrics are vague ("improve performance") | Add specific metrics: "Reduce p95 latency from 2s to 500ms" or at minimum "Reduce time-to-first-result by at least 50%" |
| No evidence section | Add at least 2–3 pieces of evidence. Customer quotes, survey data, telemetry. Even "Based on 5 customer interviews, 4 cited this as their top pain point" is useful. |
| Too broad | Split into 2–3 focused outcomes. Each outcome should be ownable by one team. |
| Too narrow | Zoom out. If only one feature could serve this "outcome," it's really a feature request. |
| Business outcome is disconnected | Trace the chain: business outcome ← user outcome ← product outcome. If the chain breaks, fix the weakest link. |

## Sign-off Criteria

Before signing off, confirm:

- [ ] All four dimensions score at least 1 (no zeros)
- [ ] At least one strategic goal is genuinely connected
- [ ] The user outcome describes a real need you've heard from users
- [ ] The product outcome is something you could instrument and measure
- [ ] The downstream opportunities give teams a real starting point
- [ ] You'd be comfortable presenting this outcome to leadership
