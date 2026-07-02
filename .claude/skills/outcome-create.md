# /outcome.create

Create a new outcome from strategic goals, research, and/or a problem statement.

## Trigger

User says `/outcome.create` optionally followed by:
- A problem statement or strategic theme description
- `--strategic-goal PROJGOALS-XXX` to anchor to a specific strategic goal
- `--headless` to skip clarifying questions (for batch/CI use)
- `--input batch.yaml` to create multiple outcomes from a YAML file

## Behavior

### Step 1: Gather Context

#### Step 1a: JTBD registry lookup (when available)

If `knowledge/jtbd-registry/index.yaml` exists (see `config/jtbd-registry.yaml`):

1. Run `/outcome.jtbd-lookup` with the user prompt, batch `research_sources` (`type: jtbd_registry`), or explicit `--jobs` flags.
2. Write `artifacts/outcome-originals/OUTCOME-NNN-jtbd-context.md` per the jtbd-lookup skill.
3. Use Problem Statement seeds, Evidence seeds, and atomic capability seeds when writing the outcome and milestone plan.
4. Add optional frontmatter when jobs were matched: `jtbd_jobs`, `jtbd_registry_id`.

If the registry is not synced (`make sync-jtbd`), skip this step — do not fail creation.

If `--headless` is NOT set, ask up to 5 clarifying questions to understand:

1. **Strategic anchor**: Which strategic goal(s) does this outcome relate to? If a PROJGOALS key is provided, fetch it from Jira using the Atlassian MCP or REST API fallback. Strategic goals are used as context when provided — auto-discovery of related strat items from problem text alone is not implemented yet (follow-up).
2. **User need / JTBD**: What job is the user trying to get done? Who are the job executors? What context triggers the job? What struggle makes it hard today? (Multiple actors sharing one job is fine — flag unrelated jobs for sibling outcomes.) If Step 1a produced a JTBD context artifact, pre-fill from registry data and ask only for gaps the registry does not cover.
3. **Business context**: How does solving this benefit the organization? What business metric would improve?
4. **Evidence**: What research, customer feedback, or data supports this need? Prefer JTBD registry Evidence seeds (OpScores, verbatim quotes with citations) when Step 1a ran. (Automated market/analyst research is a follow-up — see `docs/follow-ups.md`.)
5. **Scope**: Is this a broad thematic outcome or a focused product-level outcome?

If `--headless` IS set, derive answers from the input prompt and any `--strategic-goal` context.

### Step 2: Bootstrap Rubric

Check if `artifacts/outcome-rubric.md` exists. If not, run the `export-rubric` skill to generate it. Use the rubric to guide outcome creation — ensure each section addresses what the rubric scores.

### Step 2.5: Plan milestones (before User Journey)

Follow `/outcome.plan-milestones` (see `docs/outcome-milestone-planning.md`):

1. Build an **atomic capability inventory** from JTBD context seeds (`job_steps`), struggle, and evidence — bottom-up, not theme names.
2. Group only **delivery-coupled** gaps into milestones; unrelated gaps → separate milestones.
3. Run **milestone sizing checks** (three-solutions, one-sentence, job thread, RFE forecast).
4. Write `artifacts/outcome-plans/OUTCOME-NNN-milestone-plan.yaml`.

If unrelated job threads appear in the inventory, stop and recommend `/outcome.split` instead of one outcome.

### Step 3: Create Outcome Document

Write the outcome to `artifacts/outcome-tasks/OUTCOME-NNN-<slug>.md` using the template from `templates/outcome-template.md`.

The document MUST include these sections only (lean structure — avoid redundant restatements):

1. **Problem Statement** — JTBD only: job, context, struggle, who is involved (sub-bullets per job executor). No customer quotes, no named accounts, no solution language.
2. **User Journey & Milestones** — Write phases from the milestone plan (Step 2.5). **All success metrics live here** — no separate Success & Metrics section. Typically **2–4 phases** (fewer when delivery-coupled; cap at ~4). For each phase:
   - User capability headline (from plan; three-solutions test)
   - When this is true (actor capabilities, solution-independent)
   - Success signal with target timeframe (from plan)
   - Problems this phase addresses (from atomic inventory; value dependencies noted)
   - 2–3 scenarios nested under relevant phases: Actors, Context, Flow, Win moment — **no Today's pain** (Problem + Evidence cover that)
   - Set milestone plan `status: applied` after writing phases
3. **Evidence** — Customer quotes, analyst/market data, platform gaps, one-line opportunity verdict. No separate Opportunity Assessment section.
4. **Open Questions** — What engineering and product still need to decide. Discovery questions per capability area. No solution sketches in the body — link to external docs instead.
5. **Out of Scope** — 3+ related exclusions with brief rationale
6. **Related Resources** — Required links to external docs: implementation sketch, design/prototype, evidence deep-dive. Keep the outcome body lean; solution language, architecture details, and collaborative artifacts live in linked resources.

Do NOT create: Success & Metrics, User Outcome, Product Outcome, Business Outcome (as separate sections), End-to-End Customer Arc, Story Map, Release Milestones, Opportunity Assessment, Downstream Opportunities, Example Implementation (inline), Related Documents (use Related Resources), or Acceptance Signals.

### Step 4: Write Frontmatter

Add YAML frontmatter with:
```yaml
---
id: OUTCOME-NNN
title: "Descriptive title"
status: draft
strategic_goals: [PROJGOALS-XXX]
components: []
priority: Critical | Major | Minor
score: null
jtbd_jobs: []              # optional — registry job IDs when Step 1a matched
jtbd_registry_id: null     # optional — e.g. jtbd-rhai-2026
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

### Step 5: Save Input Snapshot

Save the original inputs (strategic goal data, research excerpts, user prompt) to `artifacts/outcome-originals/OUTCOME-NNN-inputs.md` for traceability. If Step 1a ran, the JTBD context artifact is separate: `OUTCOME-NNN-jtbd-context.md`.

## Output

- `artifacts/outcome-tasks/OUTCOME-NNN-<slug>.md` — The outcome document
- `artifacts/outcome-originals/OUTCOME-NNN-inputs.md` — Input snapshot
- `artifacts/outcome-originals/OUTCOME-NNN-jtbd-context.md` — JTBD registry context (when registry present)
- `artifacts/outcome-plans/OUTCOME-NNN-milestone-plan.yaml` — Milestone plan (gap inventory + grouping)
- Console summary of what was created (include milestone count and RFE forecast per phase)

## Quality Guidelines

**Important:** ALWAYS cite sources for quotes, statistics, data points, or claims from other documents. Include a link or reference to the original source. Verify the quote and URL match the source exactly.

**Do:**
- Plan milestones bottom-up before writing User Journey (`docs/outcome-milestone-planning.md`)
- Write problem-framed statements that pass the three-solutions test in Problem Statement and User Journey phases
- Put all customer quotes and named accounts in Evidence (once), each with source citation
- Put solution language in linked implementation docs (Related Documents), not in the outcome body
- Preserve the author's solution thinking when converting from Jira — move it to a linked doc, don't delete it

**Don't:**
- Repeat the same metric verbatim across multiple phase success signals (say it once in the right phase)
- Repeat customer quotes in Problem Statement and scenarios
- Add "Today's pain" to scenarios when Problem Statement and Evidence already describe the struggle
- Create legacy sections (User Outcome, separate milestones, Acceptance Signals) — use the lean template
