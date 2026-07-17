# Milestone planning (Next + Future)

How to structure **User Journey & Phases** before writing or refactoring an outcome. Adapted from [rfe-creator `/rfe.split`](https://github.com/jwforres/rfe-creator) — applied at the **milestone** layer, not the RFE layer.

Outcomes use exactly two subsections: **Next** (near-term delivery with full detail) and **Future** (later features only). Do not invent Phase 3 / thematic multi-phase arcs.

## Why this exists

Theme-based phase arcs ("Trust" → "Operate" → "Observe") are easy to write but often hide:

- Unrelated problems bundled in one milestone
- Prerequisites split across milestones incorrectly
- Milestones that will explode into many sibling RFEs downstream
- Over-specified roadmaps that age poorly

Milestone planning runs **bottom-up** from atomic customer gaps, then assigns each gap to **Next** or **Future**.

## Cardinality

| Layer | Typical cardinality |
|-------|---------------------|
| Outcome → journey | Exactly **Next** + **Future** |
| Next → RFEs | **1..N** sibling RFEs (see [outcome-rfe-handoff.md](outcome-rfe-handoff.md)) |
| Future → RFEs | Deferred — promote into Next later; export focuses on Next |

Planning Next well reduces painful `/rfe.split` later.

## Process

### 1. Atomic capability inventory (bottom-up)

Start from **gaps**, not theme names. Sources:

- Problem Statement (struggle, goal, Personas (JTBD))
- Evidence (platform gaps, customer quotes)
- Existing Next / legacy phase problem bullets (if refactoring)

For each gap, write a one-sentence **user capability** summary (problem-space, three-solutions test).

Ask per gap:

1. Could this deliver value to a customer **on its own**?
2. Does it **require** another gap to function at all?
3. Does it serve a **different job thread** than adjacent gaps?
4. Would shipping one without the other create a **broken experience**?
5. Is this **near-term (Next)** or **later (Future)**?

Mark **delivery-coupled** pairs (e.g. identity before access control; capability + its prerequisite).

**Avoid:** grouping by theme when gaps serve different segments or can ship independently. **Avoid:** inventing more than two journey subsections.

### 2. Assign Next vs Future

- **Next** — the near-term delivery-coupled slice that delivers customer value soonest
- **Future** — remaining in-scope work that can wait (features list only in the outcome body)

For Next, capture:

- **Problems addressed** — bullets from the inventory
- **Personas helped** — actor + experience change (solution-independent)
- **Sequencing** — value dependencies noted inline when needed
- **Success signal sketch** — observable customer value + rough timeframe
- **Features to deliver** — known source issues

For Future, capture:

- **Features to deliver** only

Propose an alternate grouping when ambiguous; recommend the **tightest Next** that still passes checks below.

### 3. Next sizing checks

Run on Next (Future is a feature backlog — re-check when promoting items into Next):

| Check | Pass | Fail → action |
|-------|------|----------------|
| **Three-solutions test** | Persona/capability language is solution-independent | Rewrite; move solution language to a linked implementation doc |
| **One-sentence test** | One capability thread; "and" only links coupled sub-needs | Park some gaps in Future, split outcome, or mark `expected_rfe_count: 2+` |
| **Job thread** | All problems serve the same JTBD | Split outcome (`/outcome.split`) or move outliers out of Next |
| **Delivery coupling** | Prerequisites live in Next or have an explicit sequencing note | Merge coupled gaps into Next |
| **RFE forecast** | 1–3 related problems → likely 1 RFE; 2–3 independent problems → plan 1..N RFEs | Use `--per-problem` export or expect `/rfe.split` |

### 4. Write or apply

- **New outcome:** `/outcome.create` runs planning before User Journey (writes plan artifact, then Next + Future).
- **Existing outcome:** `/outcome.plan-milestones` writes plan; apply with `--apply` or `/outcome.refine`.
- **Review:** `/outcome.review` runs Next/Future structure + sizing checks in Step 4.5.

## Plan artifact

`/outcome.plan-milestones` writes:

`artifacts/outcome-plans/<OUTCOME-ID>-milestone-plan.yaml`

See `templates/milestone-plan-template.yaml`. Set `status: applied` when the User Journey matches the plan.

## Relationship to other skills

| Skill | Layer |
|-------|--------|
| `/outcome.plan-milestones` | Design Next vs Future (this doc) |
| `/outcome.split` | Split **outcomes** (unrelated JTBDs) |
| `/outcome.export-rfe-batch` | Seed **RFE** candidates from **Next** |
| `/rfe.split` (rfe-creator) | Split **RFEs** when still oversized |
