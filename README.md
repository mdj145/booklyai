# BooklyAI – MVP (FastAPI + HTML/JS)
Appointments CRUD + simple auth endpoints + static dashboard. SQLite DB.

## Run Online (GitHub → Render)
1) Push all files to a new GitHub repo.
2) Go to https://render.com → New → Web Service → pick your repo.
3) Render auto-reads `render.yaml`. If not, set:
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
4) Once Live, open your URL:
   - Home: `/`
   - Dashboard: `/dashboard.html`
   - API docs: `/docs`

## Run Locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```
Open http://localhost:8000  (dashboard: /dashboard.html)

## Notes
- Demo user is created automatically so you can use the app immediately.
- Auth endpoints exist (/api/auth/signup, /api/auth/login) but JWT enforcement is relaxed for MVP.
- For production: enforce JWT, use PostgreSQL, add rate limiting & CSRF for forms.
