# ShopFlow

Order-management API + minimal storefront for **Riverbend Outfitters**, a
mid-market outdoor-gear retailer. This is a demo codebase used to show how
**Factory Droids** can pick up backlog tickets (GitHub issues), understand the
codebase, implement fixes, write tests, and open PRs — autonomously.

## Stack
- FastAPI + Pydantic (Python 3.10+)
- In-memory data store (seeded on startup)
- Vanilla HTML/JS/CSS storefront
- pytest + GitHub Actions CI

## Quickstart
```bash
cd shopflow
python -m venv .venv && . .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```
- API docs: http://127.0.0.1:8000/docs
- Storefront: http://127.0.0.1:8000/app
- Health: http://127.0.0.1:8000/health

Demo logins (email / password): `dana@example.com` / `trailmix1`,
`miguel@example.com` / `summit2024`.

## Tests
```bash
pytest
```
The suite is green on `main`. The seeded defects below are **latent** — existing
tests don't cover the broken paths, which mirrors how real bugs slip into prod.

## Seeded backlog (the tickets Droid remediates)
See `issues/` for full, ready-to-file GitHub issues. Push them to GitHub with
`scripts/create_issues.ps1` (Windows) or `scripts/create_issues.sh`.

| # | Type | Ticket | Where |
|---|------|--------|-------|
| 01 | Bug | Bulk discount misses the exact-threshold quantity | `app/services/pricing.py` |
| 02 | Bug | Out-of-stock / over-quantity orders are accepted | `app/services/inventory.py` |
| 03 | Feature | Filter orders by status and date range | `app/routers/orders.py` |
| 04 | Test gap | No coverage for tax calculation | `tests/test_pricing.py` |
| 05 | Security | IDOR: any caller can read any order | `app/routers/orders.py` |
| 06 | Refactor | Duplicated quantity validation + magic numbers | `app/routers/*`, `app/utils/validation.py` |

## Project layout
```
shopflow/
  app/            FastAPI app (routers, services, utils, auth, schemas)
  frontend/       Minimal storefront (mounted at /app)
  tests/          pytest suite
  issues/         Seeded GitHub issues (ISSUE-01..06)
  scripts/        gh issue creation scripts
  docs/           DEMO_SCRIPT.md, TALK_TRACK.md
```

> Demo only: auth, persistence, and payments are intentionally simplified.
