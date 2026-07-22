# Product overlays

Product overlays capture **product-specific conventions** that should not be hard-coded into the generic outcome template or skills.

Overlays live in `config/product-overlays/*.yaml`. Skills that write or review **Features to deliver** (`/outcome.create`, `/outcome.derive`, `/outcome.refine`, `/outcome.plan-milestones`, `/outcome.review`) must load matching overlays and apply them.

## When an overlay applies

An overlay matches when any of the following involve its `match.jira_projects` or `match.issue_key_prefixes`:

- Source issues (`derived_from`, derive inputs, JQL results)
- Keys already listed under **Features to deliver**
- Linked strategy / baseline issues the author is folding in

If multiple overlays match, apply all non-conflicting rules; if rules conflict, prefer the overlay whose project keys dominate the source set and note the conflict in the console summary.

## Features to deliver policy

Generic default (no overlay): link Stories / Features / RFEs that deliver the work.

Overlay may restrict which Jira projects appear in that list. Typical pattern:

| Field | Meaning |
|-------|---------|
| `include_projects` | Only these project keys may appear under Features to deliver |
| `exclude_projects` | Never list these under Features to deliver |
| `excluded_issues_home` | What to do with excluded keys: `omit` (default for RHAI — drop from Features only) or `related_resources` |

### RHAI (`config/product-overlays/rhai.yaml`)

RHAI delivery work is tracked in **RHAIRFE**. **RHAISTRAT** items are strategy / planning wrappers (and sometimes parallel STRAT↔RFE pairs for the same capability).

**Rule:** Under **Features to deliver**, list **RHAIRFE only** — not RHAISTRAT.

Prefer the RFE when both exist for the same work. If only a STRAT exists, omit it from Features to deliver — do not park it in Related Resources just because it was excluded. STRAT links may still appear in Evidence / Related Resources when they already serve as baseline or strategic context.

## Adding a new overlay

1. Copy `config/product-overlays/rhai.yaml` as a starting point.
2. Set `id`, `display_name`, and `match`.
3. Define `features_to_deliver` include/exclude rules and `guidance`.
4. No skill code changes required if the skill already says “apply matching product overlays.”
