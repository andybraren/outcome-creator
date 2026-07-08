---
name: outcome.review
description: Score and review an outcome against the quality rubric across 4 dimensions
---
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
- **2**: Each User Journey phase has an observable success signal with timeframe; early phases have leading indicators, later phases include outcome-level lagging targets where appropriate

#### User Focus (0–2)
- **0**: No clear user need articulated; outcome is technology-driven or internally focused; no JTBD or user journey
- **1**: User need is stated but generic; persona is vague; user journey missing or solution-shaped
- **2**: Problem Statement has explicit JTBD with coherent job executors; User Journey has 2–4 phases with solution-independent capabilities and 2–3 scenarios; grounded in Evidence

#### Business Alignment (0–2)
- **0**: No connection to strategic goals; business value is absent or hand-wavy
- **1**: Strategic goal is referenced but the connection is loose; lagging metrics plausible but not substantiated
- **2**: Direct connection to strategic goals; lagging targets in phase success signals or Evidence; Evidence supports the business case

#### Actionability (0–2)
- **0**: Too broad to act on ("improve everything") or too narrow (just a feature request in disguise)
- **1**: Scope reasonable but phases lack success signals or open questions; out-of-scope missing or vague
- **2**: User Journey phases are user-capability statements with sequencing; Open Questions section identifies discovery questions; Out of Scope has 3+ exclusions with rationale; Related Resources links to implementation sketch

### Step 4: Three-Solutions Test (pre-review check)

Before prose reviews, run the three-solutions test on Problem Statement and User Journey phase capability headlines:

For each statement, ask: *"Could engineering satisfy this with three completely different technical approaches?"*
- **Yes** → Problem-space language. No action needed.
- **No** → Solution language detected. Flag the statement and trigger the reverse-engineering chain:

> - Your solution: *[what they wrote]*
> - Implied friction: *[what customer problem makes this solution obviously necessary]*
> - Who is trying to do the job: *[job executor(s) + context]*
> - What blocks the job today: *[struggle / friction]*
> - How you'd know it's solved without specifying how: *[observable signal]*
> - **Problem framing:** *[rewritten as a problem]*
> - **Solution language preserved:** *[original solution language — move to linked implementation doc]*

When solution language is detected in auto-revise: rewrite the statement as problem-framed and move the original solution language to a linked implementation document (referenced in Related Resources). Don't discard it — the author's solution thinking is valuable context for engineering when it's in the right place.

### Step 4.5: Milestone sizing check

Read `docs/outcome-milestone-planning.md`. If `artifacts/outcome-plans/<OUTCOME-ID>-milestone-plan.yaml` exists, verify the User Journey matches it. If no plan exists, run checks inline:

For each `### Phase` in User Journey & Milestones:

| Check | Flag when |
|-------|-----------|
| **One-sentence** | Capability headline needs unrelated "and" between user scenarios |
| **Job thread** | Problem bullets serve different JTBD threads |
| **Delivery coupling** | Prerequisite gap is in a later phase without `depends_on` note |
| **Problem count** | 4+ unrelated problems in one phase → recommend `/outcome.plan-milestones --apply` or `/outcome.split` |
| **RFE forecast** | 2+ independent problems → note `expected_rfe_count: 1..N` for export handoff |

Write findings to `artifacts/outcome-reviews/OUTCOME-NNN-milestone-sizing.md`.

If milestone issues are blocking actionability, include in auto-revise: recommend or run `/outcome.plan-milestones --apply` (one cycle).

### Step 5: Run Prose Reviews

After scoring, run 4 independent prose reviews (can be parallelized as separate agent forks):

1. **Measurability Reviewer** — Does each phase have a real, measurable success signal with timeframe? Are leading vs lagging metrics placed in the right phases? Flag a legacy Success & Metrics section for migration. Any redundant metric restatements to remove?
2. **User Focus Reviewer** — Is JTBD coherent? Does the User Journey describe the full journey solution-independently? Are scenarios free of duplicated pain/quotes from Evidence?
3. **Business Alignment Reviewer** — Does the business case hold up? Are strategic connections genuine? Is Evidence substantive?
4. **Actionability Reviewer** — Can teams start discovery from the User Journey? Are milestones gap-driven (not theme-only)? Read milestone-sizing findings. Does Open Questions section identify discovery questions? Does Related Resources link to an implementation sketch? Is Out of Scope explicit? Flag legacy sections (including inline Example Implementation) that should be consolidated.

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
