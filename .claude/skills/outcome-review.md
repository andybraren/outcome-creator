# /outcome.review

Score and review an outcome against the quality rubric across 4 dimensions.

## Trigger

User says `/outcome.review` optionally followed by:
- A path to a specific outcome file
- A Jira key (e.g., `PROJSTRAT-1344`) to fetch and review an existing outcome
- `--headless` to skip interactive prompts
- `--auto-revise` to automatically fix issues found (default: on)

## Behavior

### Step 1: Locate Outcome

1. If a Jira key is provided, fetch the issue using the Atlassian MCP or REST API fallback. Save to `artifacts/outcome-tasks/` with proper frontmatter.
2. If a file path is given, use it.
3. If in `local/`, operate in local mode.
4. If none, list available outcomes and ask which to review.

### Step 2: Load Rubric

Read the scoring rubric from `config/rubric.yaml`. If `artifacts/outcome-rubric.md` doesn't exist, export it via the `export-rubric` skill.

### Step 3: Score with Outcome Scorer

Invoke the `outcome-scorer` agent (defined in `.claude/agents/outcome-scorer.md`) to score the outcome. The scorer is a restricted agent with only Read/Write/Glob/Grep permissions.

The scorer evaluates 4 dimensions, each scored 0–2:

#### Measurability (0–2)
- **0**: No metrics, no directional indicators, purely aspirational
- **1**: Directional indicators present but no specific metrics; or metrics exist but aren't clearly tied to the outcome
- **2**: Clear, specific metrics for business and product outcomes; acceptance signals are observable and time-bound

#### User Focus (0–2)
- **0**: No clear user need articulated; outcome is technology-driven or internally focused
- **1**: User need is stated but generic; persona is vague; user outcome reads like a feature description
- **2**: Specific user persona identified; user outcome describes a meaningful change in capability or experience; grounded in research or evidence

#### Business Alignment (0–2)
- **0**: No connection to strategic goals; business value is absent or hand-wavy
- **1**: Strategic goal is referenced but the connection is loose; business outcome is plausible but not substantiated
- **2**: Direct connection to strategic goals with clear rationale; business outcome has specific metrics; evidence supports the business case

#### Actionability (0–2)
- **0**: Too broad to act on ("improve everything") or too narrow (just a feature request in disguise)
- **1**: Scope is reasonable but downstream opportunities are unclear; teams would struggle to derive product work from this
- **2**: Well-scoped; downstream opportunities are concrete; teams can immediately begin discovery; open questions are identified

### Step 4: Three-Solutions Test (pre-review check)

Before prose reviews, run the three-solutions test on Problem Statement, Milestones, and Arc capabilities:

For each statement, ask: *"Could engineering satisfy this with three completely different technical approaches?"*
- **Yes** → Problem-space language. No action needed.
- **No** → Solution language detected. Flag the statement and trigger the reverse-engineering chain:

> - Your solution: *[what they wrote]*
> - Implied friction: *[what customer problem makes this solution obviously necessary]*
> - Who is trying to do the job: *[job executor(s) + context]*
> - What blocks the job today: *[struggle / friction]*
> - How you'd know it's solved without specifying how: *[observable signal]*
> - **Problem framing:** *[rewritten as a problem]*
> - **Example Implementation:** *[original solution language preserved here]*

When solution language is detected in auto-revise: rewrite the statement as problem-framed and move the original solution language to the Example Implementation section. Don't discard it — the author's solution thinking is valuable context for engineering when it's in the right place.

### Step 5: Run Prose Reviews

After scoring, run 4 independent prose reviews (can be parallelized as separate agent forks):

1. **Measurability Reviewer** — Are the metrics real? Can they actually be measured? Are baselines available? Are milestone-level success signals present?
2. **User Focus Reviewer** — Is this a real user need or an internal assumption? Would users recognize this as their problem? Does the E2E customer arc describe the full journey solution-independently?
3. **Business Alignment Reviewer** — Does the business case hold up? Are the strategic connections genuine or forced?
4. **Actionability Reviewer** — Could a product team take this and start discovery tomorrow? Are release milestones customer-capability statements? Is out-of-scope explicit?

Each reviewer writes findings to `artifacts/outcome-reviews/OUTCOME-NNN-<dimension>.md`.

### Step 6: Determine Verdict

Combine scores into a total (0–8):
- **8/8**: PASS — Ready for downstream work
- **6–7/8**: REVISE — Targeted improvements needed
- **<6/8**: REWORK — Fundamental issues

### Step 7: Auto-Revise (if enabled)

If `--auto-revise` is on and verdict is REVISE:
1. Read all reviewer findings
2. Apply targeted fixes to the outcome document
3. Re-score (up to 2 revision cycles)
4. If still REVISE after 2 cycles, stop and report

### Step 8: Update Frontmatter

Update the outcome document's frontmatter with scores:
```yaml
score:
  measurability: 2
  user_focus: 1
  business_alignment: 2
  actionability: 2
  total: 7
  verdict: REVISE
```

### Step 9: Apply Labels (CI mode only)

If NOT in local mode and outcome has a Jira key:
- Score ≥ 6 (no zeros): Add `outcome-creator-rubric-pass` label
- Score < 6 or any zero: Add `outcome-creator-needs-attention` label

## Output

- Updated outcome document with scores in frontmatter
- Review files in `artifacts/outcome-reviews/` or `local/outcome-reviews/`
- Console summary with scores, verdict, and key findings
