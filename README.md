# A Coffee Roastery Subscription Manager

A Coffee Roastery Subscription Manager — a focused web app generated, validated and deployed by the Startup Agent team.

## Stack

- Backend: Python + FastAPI + SQLite
- Frontend: React + TypeScript + Vite

## Run locally

```bash
# backend
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload --port 8000

# frontend (new terminal)
cd frontend && npm install && npm run dev
```

- Frontend: http://localhost:5173
- API: http://localhost:8000/api

## Test & build

```bash
python -m pytest backend/tests
npm --prefix frontend run build
```

## API

| Method | Path           | Description   |
| ------ | -------------- | ------------- |
| GET    | /api/health    | Health check  |
| GET    | /api/items     | List items    |
| POST   | /api/items     | Create item   |
| PATCH  | /api/items/:id | Update item   |
| DELETE | /api/items/:id | Delete item   |

Deployed to GitHub and Railway automatically by the Startup Agent factory.
