# Follow-ups

Deferred enhancements from PR review and pipeline work.

## Market / analyst research subagent

**Source:** [PR #2](https://github.com/andybraren/outcome-creator/pull/2) review — Evidence section could be enriched with automated gathering.

**Idea:** Optional deep-research or web-search step during `/outcome.create` or `/outcome.refine` to populate **Analyst & market** (and optionally customer findings) before the author edits Evidence.

**Status:** Not implemented. Evidence template and citation rules are in place; automation is a follow-up.

## Strategic goal auto-discovery

**Source:** PR #2 review — link outcomes to strat items in Jira automatically.

**Idea:** `--discover-strategic-goals` or submit-time validation that searches PROJGOALS by theme when frontmatter keys are missing.

**Status:** Not implemented. Create/submit link goals when keys are provided in frontmatter or via `--strategic-goal`.

## Product overlay auto-enforcement in CI

**Source:** RHAI Features-to-deliver convention (RFE-only) introduced as `config/product-overlays/rhai.yaml`.

**Idea:** Scripted check in CI / `/outcome.review` scoring that fails or auto-revises when excluded project keys appear under Features to deliver for a matched overlay.

**Status:** Skill guidance + docs only; no automated validator yet.