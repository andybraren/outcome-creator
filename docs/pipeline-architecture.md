# Pipeline Architecture

Technical documentation for the outcome-creator pipeline.

## Overview

The outcome-creator is a Claude Code skills-based pipeline that creates, refines, reviews, and submits outcomes to Jira. It follows the same architectural pattern as [rfe-creator](https://github.com/jwforres/rfe-creator) and [strat-creator](https://github.com/ederign/strat-creator).

## Pipeline Stages

```
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  outcome-create │────▶│  outcome-refine   │────▶│  outcome-review  │────▶│  outcome-submit  │
│                 │     │                   │     │                  │     │                  │
│ Inputs:         │     │ Adds:             │     │ Scores:          │     │ Writes:          │
│ - Strategic     │     │ - Research data   │     │ - Measurability  │     │ - New issue      │
│   goals         │     │ - User evidence   │     │ - User Focus     │     │ - Or update      │
│ - Research      │     │ - Opportunity     │     │ - Biz Alignment  │     │ - Links to       │
│ - Problem       │     │   assessment      │     │ - Actionability  │     │   strategic      │
│   statement     │     │ - Refined metrics │     │                  │     │   goals          │
└─────────────────┘     └──────────────────┘     └──────────────────┘     └──────────────────┘
        │                                                │
        ▼                                                ▼
  artifacts/                                    artifacts/
  outcome-tasks/                                outcome-reviews/
  outcome-originals/
```

## Execution Modes

### Interactive (Default)

Each skill runs in a Claude Code session. The user invokes skills with `/outcome.create`, `/outcome.refine`, etc. Skills ask clarifying questions and present results for feedback.

### Headless (CI)

Skills accept `--headless` flag to skip interactive prompts. Combined with `--dry-run`, the pipeline can validate without Jira writes. Parsed arguments persist in `tmp/*.yaml` to survive context compression.

### Speedrun

`/outcome.speedrun` chains create → refine → review → submit with reasonable defaults. Supports batch mode via `--input batch.yaml`.

## Artifact Structure

All pipeline artifacts use a consistent format: YAML frontmatter + Markdown body.

### Frontmatter Schema

```yaml
id: string              # OUTCOME-NNN (local) or PROJSTRAT-XXXX (Jira)
title: string            # Descriptive title
status: enum             # draft | review | approved | active | closed
strategic_goals: list    # [PROJGOALS-XXX, ...]
components: list         # [ComponentName, ...]
priority: enum           # Critical | Major | Minor
score:                   # null until scored
  measurability: 0-2
  user_focus: 0-2
  business_alignment: 0-2
  actionability: 0-2
  total: 0-8
  verdict: PASS | REVISE | REWORK
created: date
updated: date
jira_url: string         # Set after submission
labels: list             # Pipeline labels
```

### File Naming

- Outcome tasks: `{ID}-{slug}.md` (e.g., `PROJSTRAT-1344-understand-measure-agents.md`)
- Reviews: `{ID}-{dimension}.md` (e.g., `PROJSTRAT-1344-measurability.md`)
- Originals: `{ID}-inputs.md`

## Scoring Architecture

### Outcome Scorer Agent

A restricted Claude agent (Read/Write/Glob/Grep only) that scores outcome documents. Defined in `.claude/agents/outcome-scorer.md`.

The scorer is invoked by the `outcome-review` skill and produces numeric scores (0–2) for each dimension.

### Prose Reviewers

Four independent reviewers run after scoring, each focused on one dimension:
1. Measurability Reviewer
2. User Focus Reviewer
3. Business Alignment Reviewer
4. Actionability Reviewer

Reviewers can run in parallel as separate agent forks. Each produces a review file in `artifacts/outcome-reviews/`.

### Auto-Revision

When verdict is REVISE, the review skill reads all reviewer findings and applies targeted fixes, then re-scores. Maximum 2 revision cycles to prevent infinite loops.

## Jira Integration

### Read Operations

1. **Atlassian MCP** (preferred): Used when MCP server is available
2. **REST API fallback**: `scripts/jira_utils.py` handles direct API calls

### Write Operations

Always via REST API through `scripts/jira_utils.py`. Operations:
- Create issue (POST /rest/api/3/issue)
- Update issue (PUT /rest/api/3/issue/{key})
- Add/remove labels (PUT /rest/api/3/issue/{key})
- Create issue links (POST /rest/api/3/issueLink)
- Add comments (POST /rest/api/3/issue/{key}/comment)

### Label Convention

Labels track pipeline state:
- `outcome-creator-auto-created` — Created by the pipeline
- `outcome-creator-auto-refined` — Refined by the pipeline
- `outcome-creator-auto-updated` — Updated by the pipeline
- `outcome-creator-rubric-pass` — Scored ≥ 6 with no zeros
- `outcome-creator-needs-attention` — Scored < 6 or has zeros
- `outcome-creator-resubmitted` — Pushed back from local review
- `outcome-creator-signed-off` — Human sign-off complete

## Local vs CI Modes

Skills auto-detect local mode when files are in `local/`:

| Behavior | CI Mode (artifacts/) | Local Mode (local/) |
|----------|---------------------|---------------------|
| Jira reads | Yes | No |
| Jira writes | Yes | No |
| Label management | Yes | No |
| Scoring | Yes | Yes |
| Prose reviews | Yes | Yes |
| Auto-revision | Yes | Yes |

## Configuration

All pipeline parameters are externalized in `config/pipeline-settings.yaml`:
- Jira project keys and issue types
- Label names
- Batch size and limits
- Scoring thresholds
- Research source type definitions

No hardcoded values in skills or scripts.

## Dependencies

- **Python 3.11+**: Scripts runtime
- **requests**: Jira REST API calls
- **pyyaml**: YAML parsing
- **python-frontmatter**: Markdown frontmatter handling
- **jinja2**: Template rendering (report generation)
- **Claude Code**: Skill execution environment
