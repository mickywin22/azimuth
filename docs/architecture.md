# world-vault — Architecture

> **Status:** Draft
> **Last updated:** YYYY-MM-DD

## System Overview

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend   │────▶│   Backend   │────▶│  Database    │
│  (Next.js)   │◀────│  (FastAPI)  │◀────│ (Supabase)  │
└─────────────┘     └─────────────┘     └─────────────┘
     Vercel         Hetzner+Coolify       Supabase
```

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Frontend | Next.js 14, Tailwind, shadcn/ui | ... |
| Backend | Python 3.12, FastAPI | ... |
| Database | PostgreSQL (Supabase) | ... |
| Hosting | Vercel + Hetzner+Coolify (apex-api.emi-factory.dev pattern) | see `docs/coolify-deploy.md` |

## Key Decisions

### Decision 1: ...
- **Context:** ...
- **Decision:** ...
- **Consequences:** ...

## API Design

Base URL: `/api/v1/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/resource` | List resources |
| GET | `/resource/{id}` | Get resource |
| POST | `/resource` | Create resource |

## Data Flow

1. User interacts with frontend
2. Frontend calls backend API
3. Backend processes request, queries database
4. Response returned through the chain

## Security

- API keys stored in environment variables
- CORS configured for frontend origin only
- Rate limiting on public endpoints

## Deployment

- **Frontend:** Vercel (auto-deploy from `main`)
- **Backend:** Hetzner+Coolify (auto-deploy from `main`, see `docs/coolify-deploy.md` — supersedes Render since Phase J7, 2026-04-21)
- **Database:** Supabase managed PostgreSQL
