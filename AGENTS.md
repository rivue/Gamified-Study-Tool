# Repository Guidelines

## Project Structure & Module Organization
- `backend/`: Flask app (`app.py`), route modules under `routes/`, SQLAlchemy models under `database/`, Alembic migrations in `backend/migrations/`, utilities in `vector_processing/` and `knowledge_net/`. Static frontend is served from `frontend/dist` in production.
- `frontend/`: Vue 3 app (Vue CLI). Source in `src/`, assets in `src/assets/`, Pinia stores in `src/store/`. Build output in `dist/`.
- Scripts: `entrypoint.sh`, `startup.sh`, `Dockerfile`. CI/CD: `cloudbuild.yaml`.
- Tests: backend examples in `backend/tests/`.

## Build, Test, and Development Commands
- Backend: `python backend/app.py` — run Flask dev server on `:5000`.
- Backend (Gunicorn): `gunicorn --chdir backend -b 0.0.0.0:5000 -w 2 app:app` — production entry.
- Migrations: `flask --app backend/app db upgrade` — apply Alembic migrations.
- Frontend dev: `cd frontend && npm install && npm run serve` — Vue dev server.
- Frontend build: `cd frontend && npm run build` — outputs to `frontend/dist`.
- Backend tests: `python -m unittest discover backend/tests -v`.

## Coding Style & Naming Conventions
- Python: 4‑space indent, type where helpful, snake_case for functions/vars; route files named `*_routes.py`. Keep modules under `backend/` import‑safe.
- Vue/TS: Composition API, `.vue` components in PascalCase, Pinia stores in `src/store/*Store.(ts|js)`.
- Linting: Frontend uses ESLint (`npm run lint`). No enforced Python linter; prefer black/isort-style formatting and docstrings.

## Testing Guidelines
- Framework: Standard library `unittest` in `backend/tests/`.
- Naming: Test files `test_*.py`, classes `Test*`, methods `test_*`.
- Running: `python -m unittest discover backend/tests -v`.
- Coverage (optional): add focused tests for routes, models, and utilities; mock external APIs.

## Commit & Pull Request Guidelines
- Commits: Write clear, present‑tense messages (e.g., "add streak endpoint", "fix library join code"). Group related changes; avoid noisy vendor/`dist` diffs.
- PRs: Include purpose, scope, and testing notes. Link issues. For UI changes, add screenshots or short clips. Ensure migrations are included and idempotent. Describe any new env vars.

## Security & Configuration Tips
- Secrets: Do not commit keys. Backend expects `OPENAI_API_KEY`, `RESEND_API_KEY`, DB settings (`DB_*`, `DATABASE`, etc.). Use `.env` locally; set `FLASK_ENV=production` in prod.
- Database: Run `flask --app backend/app db upgrade` before starting app. Validate `frontend/dist` exists in prod builds.
