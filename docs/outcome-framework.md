# Outcome Framework

This document describes the outcome framework used by the outcome-creator pipeline. It explains what outcomes are, why they matter, and how to write good ones.

## The Planning Hierarchy

Outcomes sit at a specific level in the product planning hierarchy:

```
Strategic Goal          ← "What direction are we heading?"
  └─ Outcome            ← "What change do we want to see?" (THIS LEVEL)
       └─ RFE / Feature ← "What capability do we need?"
            └─ Strategy  ← "How do we build it?"
                 └─ Epic → Story → Task
```

Each level answers a different question. Outcomes answer: **"What measurable change in the world — for users, the product, or the business — would indicate that our strategy is working?"**

## Three Layers of Outcomes

Every well-formed outcome has three layers. Each layer serves a different purpose and has a different audience:

### Business Outcome

**Audience**: Leadership, product leadership, finance
**Question**: How does the organization benefit?
**Characteristics**:
- Lagging indicator — tells you what already happened
- Typically financial or market-position oriented
- Changes slowly; measured quarterly or annually
- Examples: revenue, market share, customer retention, cost per acquisition

**Why it matters**: Connects product work to business value. Without this, teams can't articulate why their work matters to the organization.

### User Outcome

**Audience**: Product teams, design, research
**Question**: What can users do, feel, or achieve differently?
**Characteristics**:
- Bridges business outcomes and product outcomes
- Describes a meaningful change in capability or experience
- Should be recognizable by actual users as their problem/need
- Solution-agnostic — multiple features could serve the same user outcome
- Based on real research, not assumptions

**Format**: User outcome statements follow the pattern:
> Minimize/Maximize [direction] the [metric] of [doing some task or activity]

Examples:
- Minimize the time it takes to diagnose an agent failure in production
- Maximize the confidence that deployed agents are behaving correctly
- Minimize the number of tools required to get a complete picture of agent health

**Why it matters**: Keeps teams focused on user needs rather than feature lists. Forces the question: "Is it possible to have a happy customer who never uses a specific feature we'd build for this?"

### Product Outcome

**Audience**: Product teams, engineering, data/analytics
**Question**: What measurable behavior changes in the product?
**Characteristics**:
- Leading indicator — gives early signal of whether you're on track
- Predicts business outcomes (if product outcome improves, business outcome should follow)
- Measurable through product telemetry, analytics, or instrumentation
- Spans features — describes value, not adoption of a single tool
- Pairs behavior metrics with sentiment metrics

**Why it matters**: Gives teams something concrete to optimize for. Unlike business outcomes (which are too lagging) or user outcomes (which can be hard to measure), product outcomes are directly observable in the product.

## The Outcome Chain

The three layers form a chain:

```
Product Outcome (leading indicator)
    ↓ drives
User Outcome (experience change)
    ↓ drives
Business Outcome (lagging indicator)
```

A strong outcome has a clear chain. If you can't explain how improving the product outcome would lead to a better user experience, which would lead to a business benefit, the chain is broken.

## Opportunity Assessment

Not all outcomes are equally worth pursuing. The opportunity assessment helps prioritize by measuring two things:

1. **Importance**: How important is this outcome to users?
2. **Satisfaction**: How satisfied are users with their ability to achieve this today?

These combine into an **Opportunity Score**:

```
Opportunity = Importance + max(Importance - Satisfaction, 0)
```

This produces four categories:

| Category | Importance | Satisfaction | Action |
|----------|-----------|-------------|--------|
| **Underserved** | High | Low | Highest opportunity — invest here |
| **Table Stakes** | High | High | Must maintain — don't regress |
| **Appropriately-served** | Low | Low | Monitor — not urgent |
| **Overserved** | Low | High | Potential to deprioritize |

The most valuable outcomes to pursue are **underserved** ones: important to users but poorly satisfied by current solutions.

## Naming the Outcome (Jira Title)

The outcome `title` becomes the Jira Summary. Teams refer to outcomes by this name in planning conversations, so keep it short enough to say out loud and still be understood.

**Default:** ≤5 words — a colloquial shorthand that captures the gist.

| Prefer | Avoid |
|---|---|
| `Deploy Agents Confidently` | `AI engineers can deploy a new agent version to production in under 15 minutes with automated rollback` |
| `Diagnose Agent Failures` | `Minimize the time it takes for platform engineers to diagnose agent failures in production without ops assistance` |
| `Govern Model Access` | `Enterprise admins can govern which teams can access which models across all environments` |

The measurable, experience-oriented statement still belongs in the outcome — in **Goal**, **Value to personas**, and **Success signal** — not in the title. Exceed 5 words only when the author explicitly wants a longer Summary.

## Common Anti-Patterns

### 1. Output Disguised as Outcome
**Bad**: "Ship an observability dashboard"
**Good**: "Engineers diagnose agent failures in under 5 minutes without ops assistance"

**Test**: Is it a yes/no deliverable, or a measurable change in the world?

### 2. Vanity Metric
**Bad**: "Increase page views on the monitoring tab"
**Good**: "Engineers who encounter an agent failure use the monitoring tools to resolve it without escalation"

**Test**: Could you game this metric without actually helping users?

### 3. Kitchen Sink Outcome
**Bad**: "Improve the entire agent development and deployment experience"
**Good**: "AI engineers can deploy a new agent version to production in under 15 minutes with automated rollback"

**Test**: Could one team own this? Or would it take five?

### 4. Feature in Disguise
**Bad**: "Users can filter traces by agent ID"
**Good**: "Engineers can isolate the behavior of a specific agent across all its interactions"

**Test**: Can you imagine 3 different solutions that would serve this outcome?

### 5. Sentiment Without Behavior
**Bad**: "Increase NPS score by 10 points"
**Good**: "Increase NPS by 10 points, driven by a 40% increase in successful first-deployment rate"

**Test**: What would you see change in the product if this succeeded? If you can't answer that, you need a product outcome paired with the sentiment metric.

### 6. Traction Metric as Outcome
**Bad**: "Increase the number of users who view the traces page"
**Good**: "Engineers use production trace data to improve their agent's behavior within 2 iterations"

**Test**: Is it possible to have a happy, successful user who never does this specific thing? If yes, it's a traction metric, not an outcome.

## Writing Process

1. **Start with the strategic goal**: What business direction are we pursuing?
2. **Identify the user need**: What pain exists? Who feels it? What evidence do we have?
3. **Write the user outcome first**: Describe the experience change, not the solution
4. **Derive the product outcome**: What would we see change in the product if the user outcome were achieved?
5. **Connect to the business outcome**: How does this user change translate to business value?
6. **Assess the opportunity**: How important is this? How satisfied are users today?
7. **List downstream opportunities**: What solution areas might teams explore? (Without committing to any)
8. **Define acceptance signals**: How will we know it's working?
