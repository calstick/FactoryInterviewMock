# ShopFlow Live Demo Script (Factory)

Target: ~12-15 min of live demo inside a 30-min MVP walkthrough. The story is
**"backlog ticket → merged PR, autonomously."**

## 0. Pre-flight (before the call)
- [ ] Repo pushed to GitHub; `scripts/create_issues.ps1` run so 6 issues exist.
- [ ] `pip install -r requirements.txt` done in the venv.
- [ ] Two terminals ready: one for `uvicorn app.main:app --reload`, one for Droid.
- [ ] Storefront open at `http://127.0.0.1:8000/app`, API docs at `/docs`.
- [ ] `pytest` green (show the baseline).

## 1. Set the scene (2 min)
"This is ShopFlow — the order platform for Riverbend Outfitters, a mid-market
outdoor retailer. Small team, growing backlog. Here's their GitHub issues list:
bugs, a feature, a security finding, tech debt. Today these sit for weeks because
engineers are heads-down on roadmap work."

Show: storefront, then the GitHub issues list.

## 2. Show the problem is real (2 min)
Reproduce one bug live so it's concrete:
- Add 10 of the water bottle to the cart → discount shows **$0.00** (ISSUE-01).
- Or hit `/orders/1` with no auth in `/docs` → returns someone else's order (ISSUE-05).

"These are exactly the tickets clogging the sprint."

## 3. Hand a ticket to a Droid (5-6 min) — the core moment
Pick **ISSUE-05 (IDOR security bug)** — high business value, clear before/after.

In Droid:
> "Read ISSUE-05 in the issues backlog (GitHub issue: IDOR on GET /orders/{id}).
>  Fix it per the acceptance criteria, add regression tests, and run pytest."

Narrate what Factory does:
1. Reads the issue + locates `app/routers/orders.py`.
2. Understands the auth pattern from `list_orders()` / `get_current_customer_id`.
3. Adds the dependency + ownership check.
4. Writes regression tests (401, cross-customer 404, owner 200).
5. Runs `pytest` → green.

Then: open the PR / show the diff. Re-run the unauth `/orders/1` call → now 401.

## 4. Show range, fast (3 min)
Have a second issue pre-staged (e.g., ISSUE-01 pricing bug or ISSUE-03 feature)
already turned into a PR so you can show breadth without waiting:
- The pricing fix is one operator (`>` → `>=`) **plus** the boundary tests.
- Point out Factory wrote the test that the team never had (ties to ISSUE-04).

## 5. Land the value (2 min)
"Six tickets that would've been a sprint of context-switching — triaged to PRs in
minutes, each with tests and a clean diff a human reviews. Engineers review
instead of grind. That's the Factory loop: ticket → code → validate → ship."

→ Transition to TALK_TRACK.md for value framing and the pilot.

## Backup / if something breaks
- If live Droid run stalls: switch to the pre-staged PR and walk the diff.
- If uvicorn port is busy: `--port 8001`.
- Keep `pytest` output handy as proof of the green baseline.
