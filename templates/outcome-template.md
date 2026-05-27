---
id: ${ID}
title: "${TITLE}"
status: draft
strategic_goals: [${STRATEGIC_GOALS}]
components: [${COMPONENTS}]
priority: ${PRIORITY}
score: null
created: ${DATE}
updated: ${DATE}
---

# ${TITLE}

## Problem Statement

JTBD structure only — no customer quotes or named accounts here (those belong in Evidence).

- **Job (JTBD)**: [What the customer or organization is trying to accomplish — functional job, not a solution]
- **Context**: [When or where the job arises — situation, trigger, environment]
- **Struggle**: [What makes the job hard or fails today — friction, constraints, risks]
- **Who is involved**: [Job executor(s) who share this job; name each and what part of the job they own]

<!-- JTBD coherence test: Do all named actors share one job thread?
     If unrelated jobs are bundled, recommend sibling outcomes.
     Multiple personas on the SAME job is fine — unrelated jobs is not. -->

## Success & Metrics

How will we know this outcome is working — for customers and for the business?

**Lagging (business):**
- [Specific business metric or directional indicator — e.g., strategic accounts, revenue, adoption]
- [Connection to ${STRATEGIC_GOALS}]

**Leading (product):**
- [Observable product or customer behavior that predicts the business outcome]
- [Additional leading indicators as needed]

<!-- Do not repeat per-phase success signals here — those live in Customer Arc & Delivery Plan.
     Lagging = outcome complete; Leading = early signal you're on track. -->

## Customer Arc & Delivery Plan

**[Phase 1]** → **[Phase 2]** → **[Phase 3]** → ...

One section: experience arc and delivery plan combined. Do not create separate Story Map, Release Milestones, or Acceptance Signals sections.

### Phase 1: [Name]

**Customer capability:** [What the customer can do after this phase — passes the three-solutions test]

**When this is true:**
- [Actor]: [Capability / experience change — no product, feature, or UI names]
- [Actor]: [Capability / experience change]

**Success signal:** [Observable evidence this phase delivered customer value] (target: [timeframe])

**Problems this phase addresses:**
- [Customer problem this phase addresses]
- [Note value dependency on a prior phase if any]

#### Scenario: [Title]
- **Actors:** [Who is involved]
- **Context:** [When/where this happens — set the scene only; do not restate struggle or quotes from Evidence]
- **Flow:** [5–10 plain-language steps — roles, decisions, handoffs]
- **Win moment:** [Observable signal that this phase is real]

<!-- 2–3 scenarios across phases. No "Today's pain" — Problem Statement and Evidence cover that.
     Scenarios show the future experience, not re-litigate the problem. -->

### Phase 2: [Name]

**Customer capability:** [...]

**When this is true:**
- [...]

**Success signal:** [...] (target: [...])

**Problems this phase addresses:**
- [...]

#### Scenario: [Title]
- **Actors:** [...]
- **Context:** [...]
- **Flow:** [...]
- **Win moment:** [...]

## Evidence

Single evidence section — no separate Opportunity Assessment.

**Customers** ([named accounts or segments]):
- **[Account/source]:** [Quote or finding]
- **[Account/source]:** [Quote or finding]

**Analyst & market:**
- [Analyst report, market trend, or industry data]

**Platform today:** [Current state — what exists vs. what's missing]

**Opportunity:** [Underserved | Overserved | etc.] — [one sentence: importance vs. satisfaction]

## Example Implementation & Open Questions

One possible path — illustrative, not prescriptive. Align items to customer arc phases where helpful.

**1. [Capability area]** *([Phase name])*
- [Solution direction or architecture sketch — technology names OK here]
- **Open questions:** [What engineering still needs to decide]

**2. [Capability area]** *([Phase name])*
- [...]
- **Open questions:** [...]

**Assumptions:** [What must be true for this approach to work]
**Integrations:** [Systems this path would touch]

*Problem Statement and Customer Arc define what must be true — engineering owns how.*

## Out of Scope

What related problems or capabilities are explicitly NOT part of this outcome?

- [Exclusion]: [Reason — sibling outcome, future phase, different team, etc.]
- [Exclusion]: [Reason]
- [Exclusion]: [Reason]

<!-- Require ≥3 related exclusions with brief rationale. -->
