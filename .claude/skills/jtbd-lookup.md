# /outcome.jtbd-lookup

Resolve Red Hat OpenShift AI JTBD research from the local knowledge registry and produce structured context for outcome creation.

## Trigger

Invoked automatically by `/outcome.create` and `/outcome.speedrun` when the registry is present. Can also be called directly:

- `/outcome.jtbd-lookup` — match jobs from the current prompt or conversation
- `/outcome.jtbd-lookup --jobs 16,15` — load specific job IDs
- `/outcome.jtbd-lookup --persona alex` — load jobs for a persona
- `/outcome.jtbd-lookup --phase day2` — load jobs for a lifecycle phase
- `/outcome.jtbd-lookup --outcome OUTCOME-NNN` — write context for a specific outcome ID

Batch YAML may pass `research_sources` with `type: jtbd_registry` (see below).

## Prerequisites

1. Registry synced locally: `make sync-jtbd` (requires Red Hat VPN + GitLab SAML)
2. Path exists: `knowledge/jtbd-registry/index.yaml` (default from `config/jtbd-registry.yaml`)
3. **If registry is missing, attempt `make sync-jtbd` once** before giving up. If the sync fails (network/auth), log the failure reason and continue without JTBD context — do not fail the pipeline. Tell the user: "JTBD registry sync failed ([reason]). Run `make sync-jtbd` manually when on VPN."

## Governance (mandatory)

Read `knowledge/jtbd-registry/governance.yaml` before producing output. Follow every rule:

1. **Retrieval only** — surface only fields present in registry YAML; no inference or extrapolation
2. **Source traceability** — every claim cites a registry field and original research source (use citation templates from `config/jtbd-registry.yaml`)
3. **No hallucination** — if no matching job exists, state: "The JTBD registry does not contain research findings related to [topic]."
4. **No reinterpretation** — report OpScores, importance, and satisfaction exactly as recorded
5. **Verbatim quotes** — use exact text from `pain_points`, persona `quote`, and `insights.supporting_data`
6. **Flag staleness** — if `metadata.last_updated` is more than one quarter old, note data vintage when citing OpScores

## Progressive disclosure (mandatory)

Never load all 18 job files. Token budget per lookup:

| Step | Files | Purpose |
|------|-------|---------|
| 1 | `index.yaml` only | Match relevance by name, persona, phase, OpScore |
| 2 | 1–3 `jobs/*.yaml` | Full detail for matched jobs only |
| 3 | 0–2 `personas/*.yaml` | Persona detail when actors/scenarios need it |

Respect `config/jtbd-registry.yaml` → `matching.max_jobs` (default 3).

## Job matching

When `jobs` are not explicitly provided, match from prompt/topic:

1. Read `index.yaml` → `jobs` list (sorted by OpScore desc)
2. Match by job name keywords, lifecycle phase, persona mentions, or struggle themes
3. If `auto_match: true` in batch YAML, select 1–3 best matches
4. If `prefer_underserved: true` (default), prefer jobs with `zone: underserved`
5. If multiple unrelated job threads match, flag for `/outcome.split` — do not merge into one outcome

Explicit selectors (batch YAML or flags):

```yaml
research_sources:
  - type: jtbd_registry
    jobs: [16, 15]           # explicit job IDs
    personas: [alex, maude]    # optional persona filter
    phase: day2              # optional lifecycle phase (day0|day1|day2|day3)
    auto_match: true         # infer from prompt when jobs omitted
```

## Output artifact

Write `artifacts/outcome-originals/<OUTCOME-ID>-jtbd-context.md` using this structure:

```markdown
# JTBD Context — <OUTCOME-ID>

registry_id: jtbd-rhai-2026
registry_last_updated: <from index metadata>
matched_jobs: [16, 15]
matched_personas: [maude, alex]

## Problem Statement seeds

### Job (JTBD)
<from job_statement — solution-agnostic, no paraphrasing that changes meaning>

### Context
<when/where the job arises — derived from job phase + job_steps context only>

### Struggle
<from pain_points — summarize themes in problem statement; verbatim quotes go to Evidence section below>

### Who is involved
<from personas linked to matched jobs; load persona files for role names and pain themes>

## Atomic capability seeds (for milestone planning)

| id | summary | source |
|----|---------|--------|
| cap-1 | <from job_steps[].description, problem-space> | Job N — <step name> |
| ... | ... | ... |

## Evidence seeds

### Opportunity
<zone, OpScore, importance, satisfaction per matched job — exact values>
Source: JTBD Opportunity Survey, Q1 2026 — <url from config>

### Customer / research findings
<verbatim pain_points and insights.supporting_data with citations>
Source: JTBD Qualitative Research V2.5, March 2026 — <url from config>

### Segment notes (if relevant)
<from quant.by_segment and role_overlap when personas diverge>

## Registry gaps
<topics requested but not found in registry — or "None">
```

## Field mapping to outcome sections

| Registry field | Outcome destination |
|----------------|---------------------|
| `job_statement` | Problem Statement → Job (JTBD) |
| `pain_points` (themes) | Problem Statement → Struggle |
| `pain_points` (verbatim) | Evidence → Customers |
| `personas` + persona files | Problem Statement → Who is involved |
| `job_steps` | Milestone plan → `atomic_capabilities` |
| `quant.opportunity_score`, `zone` | Evidence → Opportunity |
| `quant.by_segment` | Scenarios → persona-specific actors |
| `insights.supporting_data` | Evidence with citations |
| `phase` (day0–day3) | User Journey phase sequencing hint |

## Integration with downstream skills

After writing the context artifact:

1. **`/outcome.create`** — use Problem Statement and Evidence seeds when writing the outcome; pass capability seeds to milestone planning
2. **`/outcome.plan-milestones`** — treat `job_steps` capability seeds as inventory source #0 (before Problem Statement struggle bullets)
3. **Frontmatter** — when JTBD jobs were matched, add optional traceability fields:

```yaml
jtbd_jobs: [16, 15]
jtbd_registry_id: jtbd-rhai-2026
```

4. **`/outcome.refine`** — if context artifact exists in `outcome-originals/`, use it to enrich Evidence without duplicating quotes

## Console summary

Print:

- Matched job IDs and names
- OpScores and zones
- Capability seed count
- Any split warnings (unrelated job threads)
- Path to context artifact
