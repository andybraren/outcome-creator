# Outcome Creator

Takes strategic goals and research inputs — user needs, pain points, market data — and produces well-structured **outcomes** in Jira. Outcomes sit above features and RFEs in the planning hierarchy. They describe the measurable change a user, product, or business should experience — not the specific solution.

The pipeline scores every outcome so the team knows what's ready for downstream work and what needs refinement.

## What This Does

This pipeline:

1. **Creates** an outcome stub from inputs — strategic goals, research, pain points (`outcome-create`)
2. **Refines** the stub into a structured outcome with business, user, and product outcome sections (`outcome-refine`)
3. **Reviews** the outcome across 4 dimensions — measurability, user focus, business alignment, actionability (`outcome-review`)
4. **Human sign-off** — a product leader or strategist reviews and marks it ready (`outcome-signoff`)

Steps 1–3 run in CI. Step 4 is a human workflow using a separate `local/` workspace.

## What Is an Outcome?

An outcome is **not** a feature, a user story, or a task. It is a statement about the change we want to see in the world — for the business, for users, or in the product — as a result of shipping solutions.

Every outcome has three layers:

| Layer | Question | Example |
|-------|----------|---------|
| **Business Outcome** | How does the business benefit? | Increase trial-to-paid conversion from 15% to 25% |
| **User Outcome** | What can users do or feel differently? | Users can confidently deploy agents to production without ops assistance |
| **Product Outcome** | What measurable behavior changes in the product? | 80% of deployed agents have active tracing within 7 days of deployment |

**Business outcomes** are lagging indicators — they tell you what already happened. **Product outcomes** are leading indicators — they give early signal on whether you're headed in the right direction. **User outcomes** bridge the two — they describe the human experience that connects product changes to business results.

Good outcomes are:

- **Measurable or directional**: Every outcome should have a metric or a clear direction, even if the exact measurement isn't defined yet.
- **Solution-agnostic**: Outcomes describe the *what* and *why*, not the *how*. Multiple solutions might serve the same outcome.
- **Durable**: Good outcomes remain relevant across multiple release cycles. If your outcome expires in a sprint, it's probably a feature.

## Why Outcomes Matter for Prototyping

When outcomes get broken down into individual RFEs and strategies further down the pipeline, each piece becomes narrow and feature-focused. Without an outcome to anchor them, you end up with a collection of myopic prototypes that each solve a slice of the problem but never show the full picture.

Outcomes are what tie it all together. They describe the end-to-end user journey — the experience change that cuts across multiple features. The [prototype-creator](https://github.com/andybraren/prototype-creator) uses outcomes to inform what a prototype should demonstrate: not just a single screen or interaction, but the broader journey a user takes to achieve the outcome. Outcomes also provide the success criteria and measurable signals that prototypes can be assessed against — "does this prototype show a path to achieving the stated outcome?"

This is the relationship:

```
outcome-creator (THE GOAL)     →  What change are we trying to achieve?
  └─ prototype-creator (THE SHOW)  →  What does achieving it look and feel like?
       └─ rfe-creator (THE WHAT)   →  What capabilities do we need?
            └─ strat-creator (THE HOW)  →  How do we build them?
```

### Outcome → RFE handoff (right-sized children)

User Journey **phases are milestones**. Each milestone may become **one or several sibling RFEs** — export only seeds the batch. When an outcome is ready:

1. `/outcome.export-rfe-batch` — emits a YAML batch (one phase-candidate per milestone by default; `--per-problem` for independent slices) for [rfe-creator](https://github.com/jwforres/rfe-creator)
2. `/rfe.speedrun --input <batch>` — creates and reviews RFEs in RHAIRFE
3. `/rfe.review` + `/rfe.split` — decompose oversized candidates into sibling RFEs under the same milestone labels

If the **outcome** itself is too big (unrelated jobs bundled), use `/outcome.split` before exporting — sibling outcomes, not a kitchen-sink parent.

See [docs/outcome-rfe-handoff.md](docs/outcome-rfe-handoff.md).

## Quick Start

```bash
# Outcome Pipeline
/outcome.create     # Write a new outcome from strategic goals + research
/outcome.derive     # Derive an outcome from existing Jira features/RFEs
/outcome.plan-milestones  # Bottom-up milestone plan (gap inventory + delivery coupling)
/outcome.refine     # Refine with research data, user insights, measurability
/outcome.review     # Score against the outcome rubric (4 dimensions)
/outcome.submit     # Submit to Jira (PROJSTRAT project, Outcome issue type)
/outcome.speedrun   # Full pipeline end-to-end with minimal interaction

# Derive outcomes from existing Jira features
/outcome.derive RHAIRFE-1234 RHAIRFE-1235 RHAIRFE-1240
/outcome.derive --jql "project = RHAIRFE AND labels = maas"
/outcome.derive RHAIRFE-1234 RHAIRFE-1235 --strategic-goal PROJGOALS-314

# Work with existing Jira outcomes
/outcome.review PROJSTRAT-1344    # Fetch, review, and auto-revise
/outcome.speedrun PROJSTRAT-1344  # Fetch, review, revise, and update

# Human review workflow
/outcome.pull PROJSTRAT-1344      # Pull outcome into local/ for review
/outcome.refine                   # Iterate locally
/outcome.review                   # Re-score locally
/outcome.push PROJSTRAT-1344      # Resubmit to CI
/outcome.signoff PROJSTRAT-1344   # Sign off as ready for downstream work

# Batch operations
/outcome.speedrun --input batch.yaml --headless --dry-run
/outcome.auto-fix --jql "project = PROJSTRAT AND issuetype = Outcome"

# Hand off to rfe-creator (after outcome is ready)
/outcome.export-rfe-batch artifacts/outcome-tasks/OUTCOME-155.md
/outcome.split OUTCOME-155.md   # if outcome scope is too large
```

## Pipeline

### New Outcomes

```
/outcome.create → /outcome.refine → /outcome.review → /outcome.submit
```

Create runs milestone planning before writing User Journey phases. Refine or `/outcome.plan-milestones --apply` when restructuring phases.

`/outcome.review` auto-revises issues it finds (up to 2 cycles). You can also edit artifacts manually between steps.

`/outcome.speedrun` runs the full pipeline with reasonable defaults.

### Derived Outcomes (from existing Jira features)

```
/outcome.derive RHAIRFE-1234 RHAIRFE-1235 → /outcome.review → /outcome.submit
```

Derive synthesizes an experience-oriented outcome from existing feature requests, RFEs, or epics in Jira. It reverse-engineers the user job from solution-shaped issues, clusters them by JTBD, plans milestones bottom-up, and produces a proper outcome — with solution language preserved in linked implementation docs. Accepts explicit Jira keys or a `--jql` query.

### Existing Jira Outcomes

```
/outcome.review PROJSTRAT-1344 → /outcome.submit
```

Or in one step: `/outcome.speedrun PROJSTRAT-1344`

### Batch Operations

Create and review multiple outcomes from a YAML file:

```bash
/outcome.speedrun --headless --dry-run --input batch.yaml
```

YAML format:

```yaml
- prompt: "Enterprise customers need to trust agent behavior in production"
  strategic_goal: PROJGOALS-314
  research_sources:
    - type: jtbd_registry
      jobs: [16, 15]
    - type: jtbd
      url: "https://drive.google.com/drive/folders/example"
  priority: Critical
  components: [Platform, DevTools]

- prompt: "AI engineers waste hours debugging agent failures"
  strategic_goal: PROJGOALS-314
  research_sources:
    - type: jtbd_registry
      auto_match: true
  priority: Major
```

See `examples/batch-with-jtbd.yaml` for JTBD registry batch examples. Requires `make sync-jtbd` (Red Hat VPN).

## JTBD Knowledge Registry (Red Hat OpenShift AI)

The pipeline can ground outcomes in UXR research from the internal [JTBD Knowledge Registry](https://gitlab.cee.redhat.com/yingzhou/jtbd-knowledge-registry). The registry data is **confidential** — it is never committed to this repo.

### Setup (private fork or local use)

```bash
make sync-jtbd   # clone/update into knowledge/jtbd-registry/ (gitignored)
```

Requires Red Hat VPN and GitLab SAML authentication. Override the clone URL with `JTBD_REGISTRY_URL` if needed.

### How it affects outcomes

When the registry is present, `/outcome.create` runs `/outcome.jtbd-lookup` before writing the outcome:

1. Matches 1–3 relevant jobs from the prompt or batch YAML (`type: jtbd_registry`)
2. Pre-populates Problem Statement (job, struggle, actors), Evidence (OpScores, verbatim quotes), and milestone capability inventory (`job_steps`)
3. Writes traceability to `artifacts/outcome-originals/OUTCOME-NNN-jtbd-context.md`
4. Adds optional frontmatter: `jtbd_jobs`, `jtbd_registry_id`

Governance rules (retrieval-only, verbatim quotes, source citations) are enforced per the registry's `governance.yaml`. See `.claude/skills/jtbd-lookup.md` and `config/jtbd-registry.yaml`.

### Batch example

```bash
/outcome.speedrun --headless --dry-run --input examples/batch-with-jtbd.yaml
```

### Public vs. private repo

This integration adds **plumbing only** (skills, config, sync script). The registry YAML stays in `knowledge/jtbd-registry/` (gitignored). For Red Hat use, fork this repo as **private**, run `make sync-jtbd` on each machine, and optionally vendor the registry in your private fork by removing the gitignore entry — do not push confidential data to the public upstream.

## Input Sources

The outcome-creator draws from multiple data sources to build well-grounded outcomes:

| Source | How It's Used |
|--------|---------------|
| **Strategic Goals** (PROJGOALS) | High-level business direction; the outcome must connect back to at least one |
| **JTBD Knowledge Registry** (Red Hat) | Local UXR research — jobs, pain points, OpScores, job steps → Problem Statement, Evidence, milestones |
| **User Research** (JTBD, Top Tasks) | Identifies real user needs, pain points, and jobs-to-be-done |
| **User Outcome Surveys** | Quantitative importance/satisfaction data for prioritization |
| **Customer Feedback** | Direct quotes and scenarios that ground the outcome in reality |
| **Existing RFEs / Features** | Feature requests that hint at unmet needs; `/outcome.derive` synthesizes outcomes from clusters of related Jira issues |
| **Market / Analyst Data** | Industry trends, competitive gaps, analyst recommendations |
| **Product Telemetry** | Usage data showing where users struggle or succeed |

## Scoring Rubric

Outcomes are scored across 4 dimensions, each worth 0–2 points (max 8):

| Dimension | What It Checks |
|-----------|----------------|
| **Measurability** | Does the outcome have a clear metric or directional indicator? Can progress be tracked? |
| **User Focus** | Is the user outcome grounded in real user needs? Does it describe a meaningful change in capability or experience? |
| **Business Alignment** | Does the outcome connect to a strategic goal? Is the business value articulated? |
| **Actionability** | Can teams derive product outcomes and opportunities from this? Is it scoped right — not too broad, not too narrow? |

Scoring:
- **8/8 (PASS)**: Outcome is ready for downstream work (RFE creation, strategy planning)
- **6–7/8 (REVISE)**: Needs targeted improvements before proceeding
- **<6/8 (REWORK)**: Fundamental issues — needs significant rethinking

## Workflows

### CI Pipeline (automated)

The CI pipeline runs `outcome-create` → `outcome-refine` → `outcome-review` in sequence. Each step runs in its own Claude session with artifacts on disk as the handoff. Output lands in `artifacts/`.

Outcomes that score 6+ total (no zeros) get `outcome-creator-rubric-pass`. Everything else gets `outcome-creator-needs-attention`.

### Human Review (local)

After CI finishes, humans use a separate `local/` workspace:

```bash
/outcome.pull PROJSTRAT-1344     # Pull post-CI outcome into local/
/outcome.refine                  # Iterate locally (reads from local/, skips Jira writes)
/outcome.review                  # Re-score locally
/outcome.push PROJSTRAT-1344     # Resubmit needs-attention outcomes to CI
/outcome.signoff PROJSTRAT-1344  # Sign off rubric-pass outcomes as ready
```

| CI Verdict | Label | Human Workflow |
|------------|-------|----------------|
| Approved | `outcome-creator-rubric-pass` | pull → review locally → `/outcome.signoff` |
| Needs attention | `outcome-creator-needs-attention` | pull → fix inputs → refine/review locally → `/outcome.push` → wait for CI → `/outcome.signoff` |

## Outcome Document Structure

Each outcome artifact uses a **lean structure** — five sections, minimal redundancy:

```markdown
---
id: PROJSTRAT-XXXX
title: "Outcome Title"
...
---

# Outcome Title

## Problem Statement
JTBD only — job, context, struggle, who is involved. No quotes or named accounts here.

## User Journey & Milestones
Phases combine experience arc, delivery plan, and **all success metrics** (not a separate Success & Metrics section):
- User capability, when this is true, success signal + timeframe, problems addressed
- Early phases = leading indicators; later phases may include outcome-level lagging targets
- Scenarios per phase: Actors, Context, Flow, Win moment (no "Today's pain")

## Evidence
Customer quotes, analyst/market data, platform gaps, one-line opportunity verdict.

## Open Questions
Discovery questions per capability area — what engineering and product still need to decide.

## Out of Scope
3+ related exclusions with brief rationale.

## Related Resources
Links to external docs: implementation sketch, design/prototype, evidence deep-dive.
```

`/outcome.refine` migrates legacy documents (Business/User/Product Outcome, separate milestones, Acceptance Signals) into this structure.

## Project Structure

```
outcome-creator/
├── scripts/                    # Python/shell scripts
│   ├── frontmatter.py              # YAML frontmatter read/write/schema
│   ├── jira_utils.py               # Jira API, JQL search, filtering
│   ├── fetch_issue.py              # Jira REST API fallback
│   ├── list-strategic-goals.py     # Discover PROJGOALS goals
│   ├── list-outcomes.py            # List existing outcomes
│   ├── pull_outcome.py             # Pull outcome from Jira into local/
│   ├── generate-report.py          # Per-run HTML report
│   ├── generate-dashboard.py       # Aggregate dashboard across runs
│   └── export_rfe_batch.py         # Export rfe-creator batch YAML from outcome phases
├── .claude/
│   ├── settings.json               # Claude Code project settings
│   ├── skills/                     # Claude Code skills (pipeline steps)
│   │   ├── outcome-create.md
│   │   ├── outcome-derive.md
│   │   ├── jtbd-lookup.md
│   │   ├── outcome-refine.md
│   │   ├── outcome-review.md
│   │   ├── outcome-submit.md
│   │   ├── outcome-speedrun.md
│   │   ├── outcome-pull.md
│   │   ├── outcome-push.md
│   │   ├── outcome-signoff.md
│   │   ├── outcome-plan-milestones.md
│   │   ├── outcome-export-rfe-batch.md
│   │   ├── outcome-split.md
│   │   ├── assess-outcome.md
│   │   └── export-rubric.md
│   └── agents/
│       └── outcome-scorer.md       # Restricted scorer agent
├── config/
│   ├── pipeline-settings.yaml      # JQL filters, batch size, labels
│   ├── jtbd-registry.yaml          # JTBD registry path, citations, matching
│   └── rubric.yaml                 # Scoring rubric definition
├── templates/
│   ├── outcome-template.md         # Outcome document template
│   ├── milestone-plan-template.yaml
│   └── review-template.md          # Review output template
├── examples/
│   └── batch-with-jtbd.yaml        # Batch input using JTBD registry
├── docs/
│   ├── human-review-guide.md       # Guide for human reviewers
│   ├── outcome-framework.md        # Outcome theory and best practices
│   ├── outcome-milestone-planning.md  # Bottom-up phase design (from rfe.split patterns)
│   ├── pipeline-architecture.md    # Technical pipeline docs
│   └── outcome-rfe-handoff.md      # Outcome → rfe-creator sizing workflow
├── tests/                          # Test suite
├── local/                          # Human review workspace (gitignored)
│   ├── outcome-tasks/
│   ├── outcome-reviews/
│   └── outcome-originals/
└── artifacts/                      # Pipeline output (gitignored)
    ├── outcome-tasks/              # Outcome documents with YAML frontmatter
    ├── outcome-reviews/            # Review files + review comments
    ├── outcome-originals/          # Original input snapshots
    ├── outcome-rubric.md           # Exported scoring rubric
    └── pipeline-report.html        # Latest HTML report
```

## Development

### Setup

```bash
uv sync
make sync-jtbd   # optional — Red Hat VPN; JTBD Knowledge Registry
```

### Running Tests

```bash
# All tests
make test

# By category
make test-unit          # Unit tests (schemas, frontmatter, scores)
make test-integration   # Integration tests (jira-emulator)
make test-e2e           # E2E pipeline replay

# Or directly via pytest
uv run pytest tests/ -v --tb=short
```

### Environment Variables

```bash
export JIRA_SERVER=https://your-jira.example.com
export JIRA_USER=your-email@example.com
export JIRA_TOKEN=your-api-token
```

### CI / Headless Mode

All skills support `--headless` for non-interactive CI use. Combined with `--dry-run`, you can validate the full pipeline without Jira writes:

```bash
claude -p "/outcome.speedrun --headless --dry-run --input batch.yaml"
```

## Related Projects

- [prototype-creator](https://github.com/andybraren/prototype-creator) — Generates rapid prototypes from RFEs, informed by outcomes for end-to-end journey context
- [rfe-creator](https://github.com/jwforres/rfe-creator) — RFE assessment and creation pipeline (downstream consumer of outcomes)
- [strat-creator](https://github.com/ederign/strat-creator) — Strategy creation from approved RFEs (further downstream)
- [assess-rfe](https://github.com/n1hility/assess-rfe) — RFE quality rubric scorer
- [ambient-code/workflows](https://github.com/ambient-code/workflows) — SDLC workflow definitions

## License

Apache-2.0
