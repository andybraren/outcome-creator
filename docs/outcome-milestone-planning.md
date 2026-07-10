# Milestone planning (User Journey phases)

How to structure **User Journey & Phases** milestones before writing or refactoring an outcome. Adapted from [rfe-creator `/rfe.split`](https://github.com/jwforres/rfe-creator) — applied at the **milestone** layer, not the RFE layer.

## Why this exists

Theme-based phases ("Trust", "Operate", "Observe") are easy to write but often hide:

- Unrelated problems bundled in one milestone
- Prerequisites split across milestones incorrectly
- Milestones that will explode into many sibling RFEs downstream

Milestone planning runs **bottom-up** from atomic customer gaps, then groups only what is **delivery-coupled**.

## Cardinality

| Layer | Typical cardinality |
|-------|---------------------|
| Outcome → milestones | Typically 2–4 phases (cap at ~4); each phase = one user-capability thread |
| Milestone → RFEs | **1..N** sibling RFEs (see [outcome-rfe-handoff.md](outcome-rfe-handoff.md)) |

Planning milestones well reduces painful `/rfe.split` later.

## Process

### 1. Atomic capability inventory (bottom-up)

Start from **gaps**, not theme names. Sources:

- Problem Statement (struggle, who is involved)
- Evidence (platform gaps, customer quotes)
- Existing phase problem bullets (if refactoring)

For each gap, write a one-sentence **user capability** summary (problem-space, three-solutions test).

Ask per gap:

1. Could this deliver value to a customer **on its own**?
2. Does it **require** another gap to function at all?
3. Does it serve a **different job thread** than adjacent gaps?
4. Would shipping one without the other create a **broken experience**?

Mark **delivery-coupled** pairs (e.g. identity before access control; capability + its prerequisite).

**Avoid:** grouping by theme when gaps serve different segments or can ship independently.

### 2. Propose milestone groupings

Group only gaps that are **inseparable** (delivery-coupled or same job thread). Everything else gets its own milestone candidate.

For each proposed milestone:

- **Name** — short phase label (e.g. Trust, Operate)
- **One-sentence capability** — single headline for the phase
- **Problems addressed** — bullets from the inventory
- **Sequencing** — `depends_on` prior milestone numbers; note value dependencies
- **Success signal sketch** — observable customer value + rough timeframe

Propose **2–3 grouping strategies** when ambiguous; recommend the fewest milestones where each still passes checks below.

### 3. Milestone sizing checks

Run on every proposed milestone:

| Check | Pass | Fail → action |
|-------|------|----------------|
| **Three-solutions test** | Capability is solution-independent | Rewrite headline; move solution language to a linked implementation doc |
| **One-sentence test** | One capability thread; "and" only links coupled sub-needs | Split milestone or mark `expected_rfe_count: 2+` |
| **Job thread** | All problems serve the same JTBD | Split outcome (`/outcome.split`) or separate milestones |
| **Delivery coupling** | Prerequisites live in same milestone or explicit `depends_on` | Merge coupled gaps; don't split identity from access control across phases |
| **RFE forecast** | 1–3 related problems → likely 1 RFE; 2–3 independent problems → plan 1..N RFEs | Use `--per-problem` export or expect `/rfe.split` |

### 4. Write or apply

- **New outcome:** `/outcome.create` runs planning before User Journey (writes plan artifact, then phases).
- **Existing outcome:** `/outcome.plan-milestones` writes plan; apply with `--apply` or `/outcome.refine`.
- **Review:** `/outcome.review` runs milestone sizing checks in Step 4.5.

## Plan artifact

`/outcome.plan-milestones` writes:

`artifacts/outcome-plans/<OUTCOME-ID>-milestone-plan.yaml`

See `templates/milestone-plan-template.yaml`. Set `status: applied` when the User Journey matches the plan.

## Relationship to other skills

| Skill | Layer |
|-------|--------|
| `/outcome.plan-milestones` | Design milestones (this doc) |
| `/outcome.split` | Split **outcomes** (unrelated JTBDs) |
| `/outcome.export-rfe-batch` | Seed **RFE** candidates per milestone |
| `/rfe.split` (rfe-creator) | Split **RFEs** when still oversized |
