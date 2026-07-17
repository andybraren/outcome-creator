---
name: outcome.derive
description: Derive a new experience-oriented outcome from existing Jira issues
---
# /outcome.derive

Derive a new experience-oriented outcome from existing Jira issues (RFEs, features, epics, bugs, or any issue type).

## Trigger

User says `/outcome.derive` optionally followed by:
- One or more Jira keys: `RHAIRFE-1234 RHAIRFE-1235 RHAIRFE-1240`
- A JQL query: `--jql "project = RHAIRFE AND labels = maas AND status != Closed"`
- A Jira filter or board URL
- `--strategic-goal PROJGOALS-XXX` to anchor the derived outcome
- `--headless` to skip clarifying questions (for batch/CI use)
- `--dry-run` to create the outcome locally without submitting to Jira

The agent may also invoke this skill autonomously when the user describes a set of existing Jira features, RFEs, or epics and asks to "create an outcome from them," "derive an outcome," "write an outcome based on these features," or similar.

## When to use

- User has a cluster of related Jira issues (RFEs, features, epics) that represent parts of a larger user need, and wants to synthesize them into a proper experience-oriented outcome
- Features exist in Jira but no parent outcome ties them to a user job or strategic goal
- A product manager or strategist wants to "roll up" tactical items into a coherent outcome
- The user describes having "a bunch of features in Jira" and wants an outcome derived from them

**Not for:**
- Creating an outcome from scratch (use `/outcome.create`)
- Pulling an existing outcome from Jira (use `/outcome.pull`)
- Improving an outcome that already exists (use `/outcome.refine`)

## Behavior

### Step 1: Gather Source Issues

#### From explicit keys

If the user provides Jira keys directly (`RHAIRFE-1234 RHAIRFE-1235`), fetch each issue using the Atlassian MCP (`getJiraIssue`) or REST API fallback. Request fields: `summary, description, status, issuetype, priority, labels, components, assignee, reporter, created, updated, resolution, project, issuelinks, comment`.

#### From JQL

If the user provides `--jql`, run the query via the Atlassian MCP (`searchJiraIssuesUsingJql`). Paginate if results exceed `maxResults`. Cap at 50 issues — if more match, warn the user and ask them to narrow the query or confirm they want all results.

#### From user description

If the user describes features without Jira keys (e.g., "we have a bunch of MaaS multi-tenancy features"), ask for:
1. The Jira project(s) to search
2. Keywords, labels, components, or epics to filter by
3. Build a JQL query from their description and confirm before executing

### Step 2: Analyze & Cluster Source Issues

Read all fetched issues. For each issue, extract:

- **Summary** and **description** (the feature/RFE content)
- **Components** and **labels** (for grouping signals)
- **Issue links** (parent epics, related issues, blocks/is-blocked-by)
- **Priority** and **status**
- **Comments** (for additional context — customer names, use cases, rationale)

#### Cohesion check (do this before synthesizing)

PMs often brain-dump a bag of features or point at "these existing tickets" without checking whether they belong in one outcome. **Do not skip this check.** Before clustering or writing a JTBD, ask:

1. **Related?** Are these features generally about the same user need / experience, or a grab-bag of unrelated asks?
2. **Natural fit?** Does it make sense for them to ship under one outcome, or are they only grouped because they share a label, component, or backlog owner?
3. **Higher-level bridge?** Is there a coherent end-to-end experience (one job thread / journey) that ties them together — not just a theme name like "multi-tenancy" or "governance"?
4. **Progression?** Do they form a natural progression of the same journey (discover → configure → operate), or parallel unrelated journeys?

If the answer to (1)–(3) is weak, **push back** before deriving. Prefer clarifying or splitting over forcing a kitchen-sink outcome.

#### Cluster by job thread

Group the issues by the user job they serve. Ask per issue:

1. What user need does this feature address?
2. Who is trying to do the job (the actor)?
3. What struggle or friction does it solve?

Issues that serve the **same JTBD** cluster together → one outcome. Issues that serve **different JTBDs** (different experience journeys) → recommend separate `/outcome.derive` invocations or flag for `/outcome.split` after creation. Do not paper over that with a vague umbrella JTBD.

If clusters are ambiguous and `--headless` is NOT set, present the proposed clustering and ask the user to confirm or adjust.

#### Flag outliers and push back

When most issues cohere but one or two do not:

- **Interactive mode:** Call them out explicitly. Ask the user to clarify how the outlier connects to the shared journey, or confirm it can be dropped / deferred to a separate outcome. Example prompts:
  - "This one looks like an outlier — it doesn't clearly serve the same job as the others. How is it related?"
  - "Can we remove it from this outcome and handle it separately?"
  - "These two clusters look like different experience journeys. Should we derive two outcomes instead of one?"
- Do **not** silently fold an unrelated feature into the outcome just because the user listed it.
- Put confirmed exclusions in **Out of Scope** (and in the inputs snapshot) with a one-line rationale.

#### Signal unrelated jobs / split into sibling outcomes

If the source issues span 2+ unrelated job threads (or two distinct experience journeys with no shared bridge):
- **Interactive mode:** Present the clusters and ask which cluster to derive first. Recommend separate outcomes for the rest — do not force one outcome across different journeys.
- **Headless mode:** Derive from the largest coherent cluster. Write a warning listing the unrelated issues with a recommendation to run `/outcome.derive` again for each remaining cluster.

### Step 3: Synthesize JTBD from Features

This is the core transformation — turning solution-shaped feature requests into a problem-framed outcome.

#### Reverse-engineer the job

From the clustered features, work backwards:

1. **Implied capabilities:** What can the user do if all these features ship? (List each feature's implied user capability)
2. **Common job:** What single job-to-be-done ties these capabilities together? Write it in JTBD format: "When [context], [actor] wants to [job], so that [desired outcome]."
3. **Context:** When or where does this job arise?
4. **Struggle:** What makes the job hard today? (Extract from issue descriptions, comments, and linked customer feedback)
5. **Personas (JTBD):** Which actors (personas, roles) appear across the source issues, and what job is each trying to get done?

#### Three-solutions test

Apply the three-solutions test to the synthesized job statement: "Could engineering satisfy this with three completely different technical approaches?" If not, abstract further until the job is solution-independent.

#### Preserve solution language

Collect all solution-specific language from the source issues (architecture decisions, technical approaches, API designs, specific tool mentions). This gets moved to a linked implementation document — not discarded.

### Step 4: JTBD Registry Lookup (when available)

If `knowledge/jtbd-registry/index.yaml` exists:

1. Run `/outcome.jtbd-lookup` with the synthesized JTBD and actor descriptions
2. Enrich the Problem Statement with registry job matches (OpScores, verbatim quotes)
3. Write `artifacts/outcome-originals/OUTCOME-NNN-jtbd-context.md`
4. Use `job_steps` as seeds for the atomic capability inventory (Step 5)

If the registry is not synced, skip — do not fail derivation.

### Step 5: Plan Milestones

Follow `/outcome.plan-milestones` (see `docs/outcome-milestone-planning.md`):

1. **Atomic capability inventory** — seed from the source issue capabilities (Step 3), enriched by JTBD `job_steps` (Step 4 when available). Each source issue maps to one or more atomic capabilities.
2. **Group by delivery coupling** — issues that must ship together → same milestone. Independent capabilities → separate milestones.
3. **Milestone sizing checks** — three-solutions, one-sentence, job thread, RFE forecast.
4. Write `artifacts/outcome-plans/OUTCOME-NNN-milestone-plan.yaml`.

Include a `source_issues` mapping in the plan:

```yaml
atomic_capabilities:
  - id: cap-1
    summary: "..."
    source: "RHAIRFE-1234 — [summary]"
    source_issues: [RHAIRFE-1234]
    job_thread: primary
    delivery_coupled_with: [cap-2]
```

If unrelated job threads appear, stop and recommend `/outcome.split`.

### Step 6: Create Outcome Document

Write the outcome to `artifacts/outcome-tasks/OUTCOME-NNN-<slug>.md` using the template from `templates/outcome-template.md`.

Follow the **same section rules as `/outcome.create`** — the document MUST include only:

1. **Problem Statement** — Context, Struggle, Goal, Personas (JTBD) from Step 3. No solution language, no feature names from source issues.
2. **User Journey & Phases** — Exactly `### Next` and `### Future` from the milestone plan (Step 5). Source issue **customer gaps** for near-term work become Next "Problems to address" (problem-framed, no feature names) plus "Personas this helps". Source issues go under **Features to deliver** in Next or Future. Next features are rank-ordered as `(P1) [KEY](url) — summary`, `(P2) …` by what most unlocks Next (no ranking justification in the body). Future is features-only and unranked. Solution/architecture detail still lives in linked implementation docs.
3. **Evidence** — Customer quotes and data extracted from source issue descriptions and comments (with citations back to Jira keys). Analyst/market data if available. Platform gap assessment based on what the features reveal about current state.
4. **Open Questions** — Discovery questions surfaced during synthesis. Questions from source issue comments. Architectural decisions that need resolution.
5. **Out of Scope** — Features from the source issues that were excluded (different JTBD, too narrow, out of cluster). At least 3 exclusions with rationale.
6. **Related Resources** — Link to each source issue. Link to implementation sketch (compiled from source issue solution language). Link to design/prototype if any source issues reference one.

### Step 7: Write Frontmatter

```yaml
---
id: OUTCOME-NNN
title: "Descriptive title"
status: draft
strategic_goals: [PROJGOALS-XXX]
components: []                    # union of components from source issues
priority: Critical | Major | Minor  # highest priority from source issues, or user-specified
score: null
derived_from: [RHAIRFE-1234, RHAIRFE-1235, RHAIRFE-1240]
jtbd_jobs: []                     # optional — registry job IDs when Step 4 matched
jtbd_registry_id: null            # optional
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

The `derived_from` field is unique to derived outcomes — it traces back to the source issues.

### Step 8: Save Artifacts

1. **Input snapshot** — Save the raw source issue data to `artifacts/outcome-originals/OUTCOME-NNN-inputs.md`. Include:
   - List of source issue keys with summaries
   - The clustering analysis (which issues → which job thread)
   - Solution language extracted from source issues (preserved for implementation docs)
   - Any source issues excluded and why

2. **Implementation sketch** — Compile the solution language, architecture details, and technical approaches from all source issues into `artifacts/outcome-originals/OUTCOME-NNN-implementation-sketch.md`. Link from the outcome's Related Resources section.

3. **JTBD context** (when registry present) — `artifacts/outcome-originals/OUTCOME-NNN-jtbd-context.md`

4. **Milestone plan** — `artifacts/outcome-plans/OUTCOME-NNN-milestone-plan.yaml`

### Step 9: Bootstrap Rubric

Check if `artifacts/outcome-rubric.md` exists. If not, run the `export-rubric` skill.

### Step 10: Confirm and Next Steps

Unless `--headless`, present a summary:

- Source issues used (count and keys)
- Source issues excluded (if any, with reasons) — including outliers the user confirmed to drop
- Cohesion check result (one shared journey vs. split recommended)
- Synthesized JTBD (one sentence)
- Milestone count and names
- Any warnings (unrelated job threads, missing evidence, source issues with no description)

Suggest next steps:

```
/outcome.review <file>            # score against rubric
/outcome.refine <file>            # enrich with additional research
/outcome.submit <file>            # push to Jira
/outcome.speedrun <file>          # review + refine + submit in one step
/outcome.export-rfe-batch <file>  # hand off to rfe-creator
```

## Headless Mode

When `--headless` is set:
- Skip clustering confirmation — use the largest coherent cluster
- Skip clarifying questions — derive JTBD from source issue content
- Write warnings about excluded issues to the input snapshot
- Continue through the full pipeline

## Local Mode

If invoked with files in `local/outcome-tasks/`, write outputs to `local/` instead of `artifacts/`. Skip any Jira API calls for submission (fetching source issues from Jira still happens).

## Quality Guidelines

**Do:**
- Run the cohesion check before synthesizing — relatedness, higher-level journey bridge, natural progression
- Push back on outliers: ask how they connect, or confirm remove / separate outcome
- Reverse-engineer the user job from feature requests — the outcome must be experience-oriented, not a feature list
- Prefer two coherent outcomes over one kitchen-sink when source issues target different experience journeys
- Preserve all solution language from source issues — move it to linked implementation docs, never discard
- Cite source Jira keys when extracting evidence (customer quotes, rationale)
- Use `derived_from` frontmatter to maintain traceability
- Run the three-solutions test on every capability headline and the synthesized JTBD

**Don't:**
- Silently fold unrelated features into one outcome because the user listed them together
- Copy-paste feature summaries as outcome phases — phases are user capabilities, not feature names
- Lose context from source issue comments — customer names, use cases, and rationale are valuable evidence
- Create a "feature umbrella" outcome that just lists features without a coherent job thread
- Skip the cohesion / clustering step — unrelated features in one outcome will fail review

## Output

- `artifacts/outcome-tasks/OUTCOME-NNN-<slug>.md` — The derived outcome document
- `artifacts/outcome-originals/OUTCOME-NNN-inputs.md` — Source issue snapshot with clustering analysis
- `artifacts/outcome-originals/OUTCOME-NNN-implementation-sketch.md` — Solution language compiled from source issues
- `artifacts/outcome-originals/OUTCOME-NNN-jtbd-context.md` — JTBD registry context (when registry present)
- `artifacts/outcome-plans/OUTCOME-NNN-milestone-plan.yaml` — Milestone plan with source issue mapping
- Console summary: source issue count, JTBD synthesis, milestone count, next steps

## Integration

- `/outcome.create` — for outcomes from scratch (no existing Jira features)
- `/outcome.derive` — for outcomes synthesized from existing Jira features (this skill)
- `/outcome.refine` — enrich a derived outcome with additional research
- `/outcome.review` — score the derived outcome against the rubric
- `/outcome.split` — if the source issues span unrelated JTBDs, split after derivation
- `/outcome.export-rfe-batch` — hand off phases back to rfe-creator (some source issues may re-appear as RFE seeds)
