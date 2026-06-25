# ShopFlow Demo — Windows Command Cheat-Sheet

Copy-paste commands for running the live demo on Windows PowerShell. Narration
lives in `DEMO_SCRIPT.md`; this is just the keystrokes.

You will use **two PowerShell windows**:
- **Terminal A** — runs the app server (stays running the whole demo).
- **Terminal B** — your working shell for Droid + API calls.

Repo root: `C:\Users\calvi\FactoryResearch\FactoryInterviewMock`

---

## Pre-flight (before the call)

```powershell
# Terminal B — one-time: auth, push code, seed issues
cd C:\Users\calvi\FactoryResearch\FactoryInterviewMock
gh auth login
git add .
git commit -m "Add ShopFlow demo codebase, seeded issues, docs, slides"
git push origin main
.\shopflow\scripts\create_issues.ps1
```

```powershell
# Terminal A — one-time: install deps + confirm green baseline
cd C:\Users\calvi\FactoryResearch\FactoryInterviewMock\shopflow
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest
```

---

## Start the app (Terminal A — leave running)

```powershell
cd C:\Users\calvi\FactoryResearch\FactoryInterviewMock\shopflow
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

Browser tabs:
- Storefront: http://127.0.0.1:8000/app
- API docs:   http://127.0.0.1:8000/docs
- GitHub Issues + GitHub Actions tabs

---

## Phase 2 — Reproduce the bugs (Terminal B)

> The app must already be running in Terminal A. Open a **second** PowerShell
> window for these. (No venv needed here — these are just HTTP calls.)

```powershell
# 1. Sign in and grab a token
$login = Invoke-RestMethod -Uri http://127.0.0.1:8000/auth/login -Method Post `
  -ContentType "application/json" `
  -Body '{"email":"dana@example.com","password":"trailmix1"}'
$token = $login.token

# 2. Create an order so order #1 exists.
#    This also reproduces ISSUE-02 (overselling): 50 units of a stock-3 item succeeds.
Invoke-RestMethod -Uri http://127.0.0.1:8000/orders -Method Post `
  -ContentType "application/json" `
  -Headers @{ Authorization = "Bearer $token" } `
  -Body '{"items":[{"product_id":1,"quantity":2}]}'

# 3. ISSUE-05 (IDOR): fetch order #1 with NO auth — returns the order (the bug)
Invoke-RestMethod -Uri http://127.0.0.1:8000/orders/1

# 3b. Show the raw status code (200 now; becomes 401 after the fix)
curl.exe -s -o NUL -w "%{http_code}`n" http://127.0.0.1:8000/orders/1

# 4. ISSUE-01 (pricing): qty 10 returns discount = 0.0 (the bug)
Invoke-RestMethod -Uri http://127.0.0.1:8000/cart/preview -Method Post `
  -ContentType "application/json" `
  -Body '{"items":[{"product_id":3,"quantity":10}]}'
```

Optional: reproduce the same bugs visually in the storefront — sign in
(`dana@example.com` / `trailmix1`), add 10 of the water bottle, and watch the
Discount line stay at `$0.00`.

---

## Phase 3 — Hand the ticket to a Droid (Terminal B)

```powershell
cd C:\Users\calvi\FactoryResearch\FactoryInterviewMock
droid
```

Paste this prompt into Droid:

```
Read ISSUE-05 (IDOR on GET /orders/{id}) from the shopflow/issues backlog.
Fix it per the acceptance criteria, add regression tests, run pytest from the
shopflow directory, and open a PR.
```

---

## Phase 3 — Verify the fix (Terminal B)

```powershell
# Same unauth call now returns 401 instead of 200 (--reload picked up the edit)
curl.exe -s -o NUL -w "%{http_code}`n" http://127.0.0.1:8000/orders/1

# Re-run the suite to show green
cd C:\Users\calvi\FactoryResearch\FactoryInterviewMock\shopflow
.\.venv\Scripts\Activate.ps1
pytest
```

---

## Phase 4 — CI green check
No commands. Open the PR on GitHub and show the **Actions** check turn green.

---

## Reset between runs

> Tip: **don't merge** the PR during the demo. Then the issue stays open and
> `main` stays pristine, so resetting is just code + app data.

One-time, during pre-flight (after your first commit) — tag the pristine state:
```powershell
cd C:\Users\calvi\FactoryResearch\FactoryInterviewMock
git tag demo-baseline
```

Between runs:
```powershell
# 1. Reset code + reopen/recreate seeded issues in one shot
cd C:\Users\calvi\FactoryResearch\FactoryInterviewMock
.\shopflow\scripts\reset_demo.ps1

# 2. Reset in-memory app data: Ctrl+C in Terminal A, then re-run
uvicorn app.main:app --reload
# (hard-refresh the browser tab too)
```

Manual equivalents if you prefer:
```powershell
git checkout main
git reset --hard demo-baseline      # discard Droid's local edits
gh issue list --state closed        # find a closed issue number
gh issue reopen <number>            # reopen it (keeps number + labels)
```

Optional GitHub cleanup (remove Droid's PR + branch):
```powershell
gh pr close <pr-number> --delete-branch
```

---

## Fallbacks

```powershell
# Port already in use
uvicorn app.main:app --reload --port 8001

# Reset all in-memory data: Ctrl+C in Terminal A, then restart uvicorn.
# (After a restart, re-run the Phase 2 login + order commands.)

# See the status code when Invoke-RestMethod errors on a 401/404:
try { Invoke-RestMethod http://127.0.0.1:8000/orders/1 } catch { $_.Exception.Response.StatusCode.value__ }
```

**Remember:** data is in-memory and resets on every uvicorn restart, so order #1
only exists after you run the Phase 2 login + order commands. `--reload` means
you do **not** need to restart the server after Droid edits files.
