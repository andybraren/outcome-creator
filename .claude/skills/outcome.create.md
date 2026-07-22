---
name: outcome.create
description: Create a new outcome from strategic goals, research, and/or a problem statement
---
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

**Check and sync the registry:**

1. Check if `knowledge/jtbd-registry/index.yaml` exists.
2. If it does NOT exist, **attempt to sync it** by running `make sync-jtbd` (which clones from internal GitLab — requires Red Hat VPN + GitLab SAML). This is a one-time setup; subsequent runs will just `git pull`.
3. If the sync fails (network error, auth error, VPN not connected), log the failure reason in the console summary and continue without JTBD context — do not fail creation. Tell the user: "JTBD registry sync failed ([reason]). Run `make sync-jtbd` manually when on VPN to enable research-backed personas and evidence."
4. If `knowledge/jtbd-registry/index.yaml` exists (either already present or just synced), proceed with the lookup.

**Run the lookup:**

1. Run `/outcome.jtbd-lookup` with the user prompt, batch `research_sources` (`type: jtbd_registry`), or explicit `--jobs` flags.
2. Write `artifacts/outcome-originals/OUTCOME-NNN-jtbd-context.md` per the jtbd-lookup skill.
3. Use Problem Statement seeds, Evidence seeds, and atomic capability seeds when writing the outcome and milestone plan.
4. Add optional frontmatter when jobs were matched: `jtbd_jobs`, `jtbd_registry_id`.

**When the registry is unavailable** (sync failed or user skipped), log it in the console summary and note in the inputs snapshot that "Personas (JTBD)" was derived from Jira context rather than JTBD research personas. The JTBD registry is the preferred source for **Personas (JTBD)** — when present, populate each persona with their job-to-be-done from matched persona files (role names, pain themes, and job statements) rather than inferring from Jira issue descriptions.

If `--headless` is NOT set, ask up to 5 clarifying questions to understand:

1. **Strategic anchor**: Which strategic goal(s) does this outcome relate to? If a PROJGOALS key is provided, fetch it from Jira using the Atlassian MCP or REST API fallback. Strategic goals are used as context when provided — auto-discovery of related strat items from problem text alone is not implemented yet (follow-up).
2. **User need / JTBD**: What context triggers the need? What struggle makes it hard today? What goal are we enabling for customers as a whole? Who are the personas and what is each one's job-to-be-done? (Multiple personas sharing one job thread is fine — flag unrelated jobs for sibling outcomes.) If Step 1a produced a JTBD context artifact, pre-fill from registry data and ask only for gaps the registry does not cover.
3. **Business context**: How does solving this benefit the organization? What business metric would improve?
4. **Evidence**: What research, customer feedback, or data supports this need? Prefer JTBD registry Evidence seeds (OpScores, verbatim quotes with citations) when Step 1a ran. (Automated market/analyst research is a follow-up — see `docs/follow-ups.md`.)
5. **Scope**: Is this a broad thematic outcome or a focused product-level outcome?

If `--headless` IS set, derive answers from the input prompt and any `--strategic-goal` context.

#### Cohesion check (when the input is a feature / idea dump)

If the user (often a PM) pastes a list of features, capabilities, or "things we should build" rather than a single job:

1. **Related?** Do these items generally serve one user need / experience, or are they a grab-bag?
2. **Higher-level bridge?** Is there a coherent end-to-end journey that ties them together — not just a shared theme, label, or backlog owner?
3. **Outliers?** Call out items that don't connect to the rest. Ask: "This one seems like an outlier — how is it related?" or "Can we drop it / put it in a separate outcome?"
4. **Split?** If items target different experience journeys, recommend **two (or more) outcomes** instead of one kitchen-sink outcome. Prefer `/outcome.derive` when the dump is mostly existing Jira issues.

Do **not** silently accept an unrelated bag of features as one outcome. Push back early — clarifying or splitting is cheaper than failing review later.

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

1. **Problem Statement** — Context, Struggle, Goal (org-level enablement), Personas (JTBD) with one sub-bullet per persona and their job-to-be-done. No customer quotes, no named accounts, no solution language.
2. **Phases** — Write from the milestone plan (Step 2.5). **Exactly two subsections: `### Next` and `### Future`** — do not invent additional phase headings. Separate them with a horizontal rule (`---`) for Jira rendering. **All success metrics live under Next** — no separate Success & Metrics section.
   - **Next** (near-term delivery), in this order:
     - **Features to deliver** — linked delivery issues, rank-ordered for Next: `(P1) [KEY](url) — summary`, `(P2) …`, `(P3) …`. Assess which features most unlock Next problems / personas / success signal (prerequisites and delivery coupling first; highest customer-value unlocks next). Prefix only — do **not** write ranking justification in the outcome. Populate from known source issues; use `TBD` only when none exist yet. **Apply product overlays** (see below) before finalizing the list.
     - **Problems to address** (from atomic inventory; value dependencies noted) — problem-framed only; do not bury Jira keys here
     - **Value to personas** (per actor: capability / experience change, solution-independent; three-solutions test)
     - **Success signal** with target timeframe (from plan)
     - 1–2 scenarios: Actors, Context, Flow, Win moment — **no Today's pain** (Problem + Evidence cover that)
   - **Future** (later work): **Features to deliver** only — no problems, personas, success signal, or scenarios
   - Set milestone plan `status: applied` after writing the journey
3. **Evidence** — Customer quotes, analyst/market data, platform gaps, one-line opportunity verdict. No separate Opportunity Assessment section.
4. **Open Questions** — What engineering and product still need to decide. Discovery questions per capability area. No solution sketches in the body — link to external docs instead.
5. **Related Resources** — Required links to external docs: implementation sketch, design/prototype, evidence deep-dive. Keep the outcome body lean; solution language, architecture details, and collaborative artifacts live in linked resources.

Do NOT create: Out of Scope, Success & Metrics, User Outcome, Product Outcome, Business Outcome (as separate sections), End-to-End Customer Arc, Story Map, Release Milestones, Opportunity Assessment, Downstream Opportunities, Example Implementation (inline), Related Documents (use Related Resources), or Acceptance Signals.

### Step 4: Write Frontmatter

Add YAML frontmatter with:
```yaml
---
id: OUTCOME-NNN
title: "Short Colloquial Title"   # ≤5 words by default — see Title rules below
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

#### Title rules (Jira Summary)

`title` becomes the Jira issue Summary. Keep it **≤5 words by default** — a colloquial shorthand people can say in planning conversations and still be understood.

- **Do:** Capture the gist in a short noun or verb phrase — e.g. `Deploy Agents Confidently`, `Diagnose Agent Failures`, `Govern Model Access`
- **Don't:** Pack the full experience statement, metrics, persona lists, or "so that…" clauses into the title
- Put the measurable / experience-oriented detail in **Goal** and **Phases**, not in `title`
- Exceed 5 words only when the user explicitly asks for a longer title

### Step 5: Save Input Snapshot

Save the original inputs (strategic goal data, research excerpts, user prompt) to `artifacts/outcome-originals/OUTCOME-NNN-inputs.md` for traceability. If Step 1a ran, the JTBD context artifact is separate: `OUTCOME-NNN-jtbd-context.md`.

## Output

- `artifacts/outcome-tasks/OUTCOME-NNN-<slug>.md` — The outcome document
- `artifacts/outcome-originals/OUTCOME-NNN-inputs.md` — Input snapshot
- `artifacts/outcome-originals/OUTCOME-NNN-jtbd-context.md` — JTBD registry context (when registry present)
- `artifacts/outcome-plans/OUTCOME-NNN-milestone-plan.yaml` — Milestone plan (gap inventory + grouping)
- Console summary of what was created (include Next RFE forecast and Future feature count)

## Quality Guidelines

**Important:** ALWAYS cite sources for quotes, statistics, data points, or claims from other documents. Include a link or reference to the original source. Verify the quote and URL match the source exactly.

**Do:**
- Keep `title` ≤5 words by default — colloquial shorthand for planning talk (see Title rules)
- Plan milestones bottom-up before writing User Journey (`docs/outcome-milestone-planning.md`)
- Run the cohesion check when the input is a feature/idea dump — confirm one shared journey before writing
- Write problem-framed statements that pass the three-solutions test in Problem Statement and Next personas
- Put all customer quotes and named accounts in Evidence (once), each with source citation
- Put solution language in linked implementation docs (Related Documents), not in the outcome body
- Preserve the author's solution thinking when converting from Jira — move it to a linked doc, don't delete it
- Flag outliers and recommend sibling outcomes when items target different experience journeys

**Don't:**
- Use a long sentence or full user-outcome statement as the Jira title — that detail belongs in Goal / Phases
- Accept a kitchen-sink feature list as one outcome without checking cohesion
- Add Phase 3 / Phase 4 / thematic phase headings — only Next and Future
- Put problems, personas, success signals, or scenarios under Future
- Repeat customer quotes in Problem Statement and scenarios
- Add "Today's pain" to scenarios when Problem Statement and Evidence already describe the struggle
- Create legacy sections (User Outcome, separate milestones, Acceptance Signals) — use the lean template
- Leave Jira issue keys as plain text — always hyperlink them (see Jira references rule below)

### Product overlays

Before writing **Features to deliver**, load matching overlays from `config/product-overlays/` (see `docs/product-overlays.md`). Match on source-issue projects / key prefixes.

- **Default (no overlay):** Stories / Features / RFEs that deliver the work may appear in the list.
- **RHAI (`rhai.yaml`):** List **RHAIRFE only** — never RHAISTRAT. Prefer the RFE when a STRAT↔RFE pair exists for the same work. Omit RHAISTRAT from Features to deliver (do not relocate excluded STRATs to Related Resources solely for that reason).

### Jira Issue References

All Jira issue key references (e.g. `RHAISTRAT-1070`, `RHAIRFE-2494`) MUST be rendered as markdown hyperlinks in the outcome document:

- **Format:** `[RHAISTRAT-1070](https://redhat.atlassian.net/browse/RHAISTRAT-1070)`
- **Why:** When the outcome is pushed to Jira (via `/outcome.push` or manual upload), plain-text issue keys may or may not auto-link depending on Jira's rendering context. Explicit hyperlinks guarantee clickable cross-references in all contexts (Jira description, Confluence, exported markdown).
- **Scope:** Apply to all sections — Goal, Evidence, Related Resources, and anywhere else an issue key appears.
- **Base URL:** Use `https://redhat.atlassian.net/browse/` as the base. If a different Jira instance is configured, derive the base URL from the `cloudId` or site URL used in Atlassian MCP calls.
- **Features to deliver:** Still hyperlink every key — but which projects belong in that section is governed by product overlays (above).
