---
id: ${ID}
# title → Jira Summary. Default ≤5 words: colloquial shorthand for planning talk.
# Put the full experience / metrics statement in Goal and Phases, not here.
title: "${TITLE}"
status: draft
strategic_goals: [${STRATEGIC_GOALS}]
components: [${COMPONENTS}]
priority: ${PRIORITY}
score: null
created: ${DATE}
updated: ${DATE}
---

## Goal
[What we are trying to enable for customers as a whole — organizational objective, not a solution]

**Context**: [When or where the need arises — situation, trigger, environment]
**Struggle**: [What makes the job hard or fails today — friction, constraints, risks]
**Personas involved**:
- **[Persona name]** — [Their job to be done]
- **[Additional persona (if applicable)]** — [Their job to be done]

---

## Plan

Exactly two subsections — **Next** (near-term delivery) and **Future** (later work). Do not add additional phase headings.

### Next

**Features to deliver:**
- (P1) [PROJ-123](https://redhat.atlassian.net/browse/PROJ-123) — [Story / Feature / RFE summary]
- (P2) [PROJ-456](https://redhat.atlassian.net/browse/PROJ-456) — [Story / Feature / RFE summary]

**Problems to address:**
- [Problem this delivery slice addresses]
- [Value dependency note, if any]

**Value to personas:**
- [Actor]: [Capability / experience change]
- [Actor]: [Capability / experience change]

**Success signal:** [Observable evidence Next delivered value — leading and/or lagging as appropriate] (target: [timeframe])

#### Scenario: [Title]
- **Actors:** [Who is involved]
- **Context:** [When/where this happens]
- **Flow:** [Concise, plain-language steps — roles, decisions, handoffs]
- **Win moment:** [Observable signal that Next is real]

### Future

**Features to deliver:**
- [PROJ-789](https://redhat.atlassian.net/browse/PROJ-789) — [Story / Feature / RFE summary]
- [PROJ-012](https://redhat.atlassian.net/browse/PROJ-012) — [Story / Feature / RFE summary]

---

## Evidence

**Customers** ([named accounts or segments]):
- **[Account/source]:** [Quote or finding] — [URL or document reference]

**Analyst & market:**
- [Analyst report, market trend, or industry data] — [source link or citation]

**Platform today:** [Current state — what exists vs. what's missing]

**Opportunity:** [Underserved | Overserved | etc.] — [one sentence: importance vs. satisfaction]

## Open Questions

What engineering and product still need to decide before or during implementation.

- [Question about scope, architecture, dependency, or trade-off]
- [Question about scope, architecture, dependency, or trade-off]
- [Question about scope, architecture, dependency, or trade-off]

## Related Resources

Link to external docs where implementation details, collaborative artifacts, and extended evidence live — keep the outcome body lean.

- **Implementation sketch:** [URL or Jira link — solution direction, architecture, tech choices]
- **Design / prototype:** [URL — UX flows, wireframes, prototypes]
- **Evidence deep-dive:** [URL — extended research, customer call notes, data analysis]
- **[Other relevant doc]:** [URL — description]