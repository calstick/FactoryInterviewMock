# ShopFlow Talk Track & Value Panel (Assignment #2)

A customer-facing narrative built around the ShopFlow MVP. Use with the 5-slide
deck in `docs/slides/`.

## Scenario setup
- **Customer:** Riverbend Outfitters — mid-market outdoor-gear retailer, ~40
  engineers, e-commerce + internal order platform (the ShopFlow repo).
- **Prior call:** They're already piloting an AI coding assistant (GitHub Copilot
  / Cursor) for autocomplete, but the backlog of bugs and small tickets keeps
  growing. We're here to show autonomous ticket-to-PR.

### Suggested roles for the panel
- **VP of Engineering** — cares about throughput, cycle time, risk.
- **Head of Developer Productivity / Platform** — cares about adoption, tooling
  sprawl, measurable ROI, governance.
- **Engineering Manager** — cares about sprint predictability, code quality,
  reviewer load.

## Discovery questions (ask early, adapt the demo)
1. Where does work actually stall today — triage, implementation, review, or release?
2. How big is the "small but never-prioritized" backlog (bugs, flaky tests, tech debt)?
3. What's your current cycle time from issue opened → PR merged?
4. How are you using Copilot/Cursor today, and where does it stop helping?
5. What would you need to see to trust an agent to open a PR a human merges?
6. Constraints: where does code/data have to live (cloud, hybrid, on-prem, air-gapped)?

## Problem framing
- Autocomplete assistants speed up *typing*, not *throughput*. The bottleneck is
  the long tail of tickets no one has time to pick up.
- That tail = security findings sitting open, missing tests, latent pricing bugs
  that cost real revenue, and tech debt that slows every future change.
- Result: slow cycle time, reviewer fatigue, and risk accumulating quietly.

## Where Factory fits (positioning vs. alternatives)
- **vs. Copilot / Cursor (in-IDE autocomplete):** Factory is an *agent across the
  SDLC* — it reads the ticket, navigates the whole repo, implements, tests, and
  opens a PR. Complementary to IDE assistants, not a replacement for the typist.
- **vs. Devin / single-agent tools:** Factory is a platform — Droids on CLI,
  desktop, Slack, and CI; model-agnostic routing; org analytics; Agent Readiness;
  and **sovereign deployment** (SaaS / hybrid / on-prem / air-gapped).
- **vs. internal agent platform:** you get enterprise controls (SSO, cost
  budgets, OTEL, centralized config) without building/maintaining the harness.

## Demo → value mapping
| What they saw | Business value |
|---------------|----------------|
| IDOR fixed with tests, in minutes | Security risk closed without pulling a senior eng off roadmap |
| Pricing boundary bug + new tests | Direct revenue protection; regression won't recur |
| Feature (order filtering) shipped from a ticket | Roadmap velocity on the long tail |
| Every change is a reviewable PR with tests | Quality + human-in-the-loop trust preserved |

## Pilot proposal (4-6 weeks)
- **Scope:** 1-2 repos, a triaged backlog of 20-30 bug/tech-debt/test tickets.
- **Workflow:** Droids open PRs; engineers review and merge; weekly readout.
- **Guardrails:** branch protection, required review, CI must pass, scoped repos.
- **Deployment:** match their constraint (SaaS or hybrid; on-prem if needed).

### Success metrics
- **Cycle time:** issue opened → PR merged (target: meaningful reduction).
- **Backlog burn-down:** % of seeded backlog resolved.
- **Auto-resolution rate:** % of assigned tickets reaching a mergeable PR.
- **Quality:** test coverage delta; change-failure / revert rate (must not rise).
- **Engineer time reclaimed:** hours/week shifted from toil to roadmap.
- **Adoption:** active developers, PRs reviewed/merged per week.

## Likely objections & responses
- *"Can we trust agent code?"* → Everything is a PR with tests behind branch
  protection; humans still merge. Start with low-risk tickets; expand on results.
- *"We already pay for Copilot."* → Keep it. Different layer: autocomplete vs.
  autonomous ticket-to-PR. Measure incremental throughput in the pilot.
- *"Security / data residency."* → Sovereign deployment incl. air-gapped; only an
  LLM endpoint required; SSO, OTEL, cost controls built in.
- *"Will it make a mess in our repo?"* → Scoped repos, Agent Readiness to prep the
  codebase, and small reviewable diffs — not giant rewrites.
- *"What about cost / runaway spend?"* → Per-team/project budgets, model routing
  for price-performance, and analytics to attribute spend.

## One-line close
"Your engineers should review software, not grind through the backlog. Factory
turns the tickets you already have into PRs you can trust — across your whole
SDLC, on your infrastructure."
