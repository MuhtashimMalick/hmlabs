# HM Labs — Contact Form + Backend

## Setup

```bash
# 1. Install Python deps
pip install -r requirements.txt

# 2. Start the API server
uvicorn server:app --reload --port 8000
```

The SQLite database (`hmlabs.db`) is created automatically on first run.

## Serving the HTML files

Option A — put `index.html` and `projects.html` in the `static/` folder:
```bash
mkdir static
cp index.html projects.html static/
# then open http://localhost:8000
```

Option B — open the HTML files directly in a browser during dev (CORS is open).

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/contact` | Submit a contact form |
| GET | `/api/leads` | View all submissions (admin) |
| GET | `/health` | Health check |

## Database Schema

Table: `leads`

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | Auto PK |
| name | TEXT | Required |
| email | TEXT | Required |
| company | TEXT | Optional |
| role | TEXT | Dropdown selection |
| service | TEXT | Required — dropdown |
| budget | TEXT | Optional |
| timeline | TEXT | Optional |
| message | TEXT | Required, min 20 chars |
| source_page | TEXT | `index` or `projects` |
| created_at | TEXT | UTC ISO timestamp |

## Changing the API URL

If you deploy the backend to a different host, find and replace
`http://localhost:8000/api/contact` in both HTML files.
