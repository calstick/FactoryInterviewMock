# ShopFlow — Mission Backup Segment: Backlog Burn-Down

An optional "if we have extra time" segment that follows the core single-ticket
demo. It showcases **scale**: a Factory Mission plans the whole backlog and
dispatches a fleet of Droids in parallel — one PR per ticket.

## How it fits the demo flow (no live resets)
- **Core demo (depth):** one Droid fixes ONE issue end-to-end — recommended
  **#5 (IDOR security)** → PR + green CI. Full human-in-the-loop control.
- **Mission segment (scale):** a Mission targets the REMAINING issues
  (**#1, #2, #3, #4, #6, #10**) and remediates them concurrently. #10 is the
  net-new **Apple Pay checkout** feature — the revenue/competitor-parity story.
- Because the Mission targets *different* issues than the one fixed live, there
  is **no overlap and nothing to reset** between the two parts.
- Everything runs on a branch off `demo-baseline` and is **never merged**, so
  `main`, the storefront, and the seeded bugs are untouched.

## Easiest + safest way to show it live: PRE-RUN it
Missions take several minutes (planning + parallel workers). For a reliable live
showcase with no waiting and no failure risk:
1. Run the Mission **before the call** and let it finish on its own branch.
2. Keep the Mission Control session open + the PRs it created in browser tabs.
3. Live, walk the completed orchestration view and 2-3 of the resulting PRs.

(Optional: kick a fresh Mission off live to show planning/dispatch, then cut to
the pre-run results so you never wait on it.)

## Pre-run setup (before the call)
```powershell
cd C:\Users\calvi\FactoryResearch\FactoryInterviewMock
git checkout demo-baseline -b mission/backlog-burndown
droid
# In Droid:  /missions   — then paste the brief below.
```

## Mission brief (paste into /missions)
```
Mission: Burn down the ShopFlow backlog.

Goal: Autonomously remediate the open GitHub issues in the
calstick/FactoryInterviewMock repository (the shopflow/ project) — issues
#1, #2, #3, #4, #6, and #10 — dispatching a worker per issue in parallel.
Exclude #5; it is being demoed separately as a single-ticket fix.
(#10 is the net-new "Add Apple Pay checkout (simulated)" feature.)

For each issue:
1. Read the issue and its acceptance criteria.
2. Implement the fix in the shopflow/ codebase, following existing patterns.
3. Add or update tests; run pytest from the shopflow directory until green.
4. Open a pull request whose body includes "Closes #<issue-number>".

Constraints:
- Open exactly one PR per issue. Do NOT merge any PR.
- Work only on this branch's lineage.
- Do not modify .github/workflows, the demo-baseline tag, or files unrelated
  to the issue being solved.
- Keep the full test suite green.

Done when: a PR exists for each of #1, #2, #3, #4, #6, #10, each with passing CI.
```

## Success criteria
- 6 PRs opened (issues #1, #2, #3, #4, #6, #10), each green in CI, each "Closes"
  its issue.

## Talk-track (~60-90 sec)
> "You've just seen one Droid take a single ticket end-to-end — read the issue,
> write the fix and tests, open a PR, pass CI — with you in full control. That's
> depth.
>
> Now here's scale. With Missions, instead of one ticket we point Factory at the
> whole backlog. It plans the work, then dispatches a fleet of Droids in
> parallel — one per ticket. Here it's working six at once: two bugs, a missing-
> test gap, a tech-debt refactor, order filtering — and the one you flagged on
> our last call: Apple Pay checkout. Your competitors already have it, and it's
> been sitting in the backlog costing you conversions.
>
> Minutes later: six reviewable PRs, each with passing CI, each closing its
> issue — including a working Apple Pay flow. Your engineers review a batch in
> one sitting instead of grinding through them across a sprint, and a
> revenue-driving feature that was stuck in the backlog is suddenly ready to
> ship — same human-in-the-loop guarantees, just parallelized across the
> backlog."

## Reset after the demo (off-camera)
```powershell
cd C:\Users\calvi\FactoryResearch\FactoryInterviewMock
gh pr list                                  # find the mission PR numbers
gh pr close <n> --delete-branch             # repeat for each mission PR
git checkout -f main
git branch -D mission/backlog-burndown
git remote prune origin
.\shopflow\scripts\reset_demo.ps1           # reopen any closed issues, reset code
# restart uvicorn to reset in-memory app data
```
