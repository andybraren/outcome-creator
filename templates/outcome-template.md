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

<!-- Ground this in evidence: customer quotes, research findings, telemetry data.
     Frame around the user need, not a missing feature. -->

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

## Downstream Opportunities

What product changes or features might serve this outcome?

<!-- List potential solution directions without committing to any.
     Cross-reference existing RFEs.
     Note open questions for discovery.
     Remember: multiple solutions can serve the same outcome. -->

1. **Opportunity Area**: [Description]
   - Related RFEs: [PROJRFE-XXX, if any]
   - Open Questions: [What we'd need to learn]

## Acceptance Signals

How will we know this outcome is being achieved?

### Quantitative Signals
<!-- Specific metrics with baselines and targets where possible -->

### Qualitative Signals
<!-- User feedback themes, support patterns, interview findings -->

### Measurement Timeframe
<!-- When should we expect to see change? -->
