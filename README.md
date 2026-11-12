# Athar Poetry API
REST API for Arabic poetry built with **FastAPI** + **PostgreSQL 18**.

## Overview
- 55,000+ poems across 5 relational tables (poets, poems, meters, eras, topics)
- 12 endpoints: poems, poets, reference, statistics, admin
- Pagination, multi-field filtering, and aggregated statistics
- Token-protected admin SQL endpoint (SELECT only)
- Response time tracking via `X-Process-Time` header

## Tech Stack
Python · FastAPI · SQLModel · PostgreSQL 18 · Uvicorn

## Endpoints
| Module | Endpoints |
|--------|-----------|
| Poems | `GET /poems/` · `GET /poems/{id}` |
| Poets | `GET /poets/` · `GET /poets/{id}` · `GET /poets/{id}/poems` |
| Reference | `GET /topics` · `GET /meters` · `GET /eras` |
| Statistics | `GET /stats/eras` · `GET /stats/meters` · `GET /stats/top-poets` |
| Admin | `POST /admin/query` |

Full API documentation: [`doc.json`](./doc.json) or `/help` endpoint.

## Run Locally
```bash
pip install -r requirements.txt
export DATABASE_URL="postgresql://user:password@localhost:5432/athar"
uvicorn main:app --reload
```

## Note

**Source data and database are private** due to ownership restrictions. Code is shared for portfolio purposes only.

To run this project locally, create a `.env` file in the project root with the following variables:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/athar
ADMIN_TOKEN=your_secret_admin_token
```
