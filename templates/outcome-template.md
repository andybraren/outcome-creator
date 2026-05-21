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

What user or market need does this outcome address? What pain exists today?

State the JTBD explicitly: *When [context], [job executor(s)] need to [job], but [struggle].*
Name each actor and their role in the same job when several are involved.

- **Job (JTBD)**: [What the customer or organization is trying to accomplish — functional job, not a solution]
- **Context**: [When or where the job arises — situation, trigger, environment]
- **Struggle**: [What makes the job hard or fails today — friction, constraints, risks]
- **Who is involved**: [Job executor(s) who share this job; name each and what part of the job they own]

<!-- Ground this in evidence: customer quotes, research findings, telemetry data.
     Frame around the user need, not a missing feature.
     JTBD coherence test: Do all named actors share one job thread?
     If unrelated jobs are bundled, recommend sibling outcomes.
     Multiple personas on the SAME job is fine — unrelated jobs is not. -->

## Business Outcome

How does the business benefit when this outcome is achieved?

- **Metric**: [Specific metric or directional indicator]
- **Strategic Connection**: [How this connects to ${STRATEGIC_GOALS}]
- **Expected Impact**: [What changes for the business]

<!-- Business outcomes are lagging indicators. They tell you what already happened
     as a result of shipping solutions. Examples: revenue growth, market share,
     customer retention, cost reduction. -->

## User Outcome

What can users do, feel, or achieve differently?

- **Who**: [Specific persona or user segment]
- **Outcome Statement**: [Minimize/Maximize the [direction] of [metric] when [doing task/activity]]
- **Experience Change**: [What's different in their day-to-day]

<!-- User outcomes bridge business outcomes and product outcomes.
     They describe the human experience change.
     Good test: "Would this user recognize this as their problem?"
     Good test: "Is it possible to have a happy user who never uses a specific feature?" -->

## End-to-End Customer Arc

What does the customer experience when all releases of this long-lived effort are complete — across all contributing teams?

### Story Map

<!-- Solution-independent: no product names, feature names, or UI paths.
     Each phase describes what the customer can do or what changes in their experience.
     Every scenario below must trace back to a capability listed here. -->

**Phase: [Name]** → **Phase: [Name]** → **Phase: [Name]**

Under [Phase]:
- [Actor]: [Capability / experience change — no product, feature, or UI names]

### Scenarios

<!-- 2–3 scenarios, each tied to a story map phase.
     Rich enough to demo without reading Acceptance Criteria. -->

#### [Title] *(Phase: [phase name])*
- **Actors:** [Who is involved]
- **Context:** [When/where this happens]
- **Today's pain:** [What goes wrong or is hard today]
- **Flow:** [5–10 plain-language steps — roles, decisions, handoffs]
- **Win moment:** [Observable signal that this phase is real]

## Product Outcome

What measurable behavior changes in the product?

- **Leading Indicator**: [Specific product metric that predicts the business outcome]
- **Behavioral Change**: [What users do differently in the product]
- **Connection**: [How this product outcome drives the user outcome above]

<!-- Product outcomes are leading indicators. They give early signal.
     Avoid traction metrics for single features.
     Pair sentiment metrics with behavioral metrics. -->

## Evidence & Research

What data supports this outcome?

### Customer Evidence
<!-- Direct quotes, interview findings, support ticket patterns -->

### Research Findings
<!-- JTBD studies, Top Tasks surveys, user outcome surveys -->

### Market Data
<!-- Analyst reports, competitive analysis, industry trends -->

### Product Telemetry
<!-- Usage data, error rates, adoption metrics -->

## Opportunity Assessment

How underserved is this outcome today?

- **Importance**: [High / Medium / Low — or survey score if available]
- **Satisfaction**: [High / Medium / Low — or survey score if available]
- **Opportunity Score**: [importance + max(importance - satisfaction, 0)]
- **Category**: [Underserved | Overserved | Appropriately-served | Table Stakes]

<!-- Opportunity Score formula:
     Importance = (% Very/Extremely Important) / (total responses)
     Satisfaction = (% Very/Extremely Satisfied) / (total responses)
     Opportunity = Importance + max(Importance - Satisfaction, 0)
     
     Categories:
     - Underserved: Important but unsatisfied — highest opportunity
     - Table Stakes: Important AND satisfied — must maintain
     - Overserved: Satisfied but not important — potential to deprioritize
     - Appropriately-served: Neither critical — monitor -->

## Release Milestones

How does the story map sequence into major customer capability phases?

<!-- Each milestone is a customer capability statement, not a feature list.
     Three-solutions test: Could engineering achieve this milestone three
     different ways and still satisfy the statement? If no, rewrite.
     Note value dependencies between milestones (e.g., "identity before access control"). -->

**Milestone 1 — [What the customer can do after this phase]**
→ Success signal: [Observable signal that this milestone delivered customer value]
- Problem: [Customer problem this milestone addresses]
- Problem: [Customer problem, note value dependency if any]

**Milestone 2 — [Next customer capability, builds on Milestone 1]**
→ Success signal: [Observable signal]
- Problem: [Customer problem]

**Milestone 3 — [Next customer capability]**
→ Success signal: [Observable signal]
- Problem: [Customer problem]

## Downstream Opportunities

What product changes or features might serve this outcome?

<!-- List potential solution directions without committing to any.
     Cross-reference existing RFEs.
     Note open questions for discovery.
     Remember: multiple solutions can serve the same outcome. -->

1. **Opportunity Area**: [Description]
   - Related RFEs: [PROJRFE-XXX, if any]
   - Open Questions: [What we'd need to learn]

## Out of Scope

What related problems or capabilities are explicitly NOT part of this outcome?

<!-- Name 3+ things that are related to the problem but explicitly excluded.
     Include a brief rationale for each (deferred to sibling outcome, future phase,
     different team, out of our control, etc.). The "why" prevents engineers from
     concluding the exclusion was an oversight. -->

- [Exclusion]: [Reason — sibling outcome, future phase, different team, etc.]
- [Exclusion]: [Reason]
- [Exclusion]: [Reason]

## Acceptance Signals

How will we know this outcome is being achieved?

### Quantitative Signals
<!-- Specific metrics with baselines and targets where possible -->

### Qualitative Signals
<!-- User feedback themes, support patterns, interview findings -->

### Measurement Timeframe
<!-- When should we expect to see change? -->
