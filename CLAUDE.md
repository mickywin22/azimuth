# world-vault

## Overview

Public demonstrator of the HemySphere L1/L2/L3 vault doctrine, fed by Worldmonitor open-intelligence data

## Tech Stack

- **Backend:** Python 3.12, FastAPI, Pydantic v2
- **Frontend:** Next.js 16, Tailwind CSS v4, React Query, Framer Motion
- **UI Components:** shadcn/ui (New York style, dark theme)
- **Typography:** Rajdhani (display) + Inter (body) + JetBrains Mono (data)
- **Database:** Supabase (PostgreSQL)
- **Deployment:** Vercel (frontend) + Hetzner+Coolify (backend) — see `docs/coolify-deploy.md`

## Project Structure

```
src/
  backend/              # FastAPI application
    main.py             # App entry point
    config.py           # Settings (pydantic-settings)
    api/                # Route handlers
    models/             # Pydantic models + DB schemas
    services/           # Business logic
  frontend/             # Next.js 16 application
    src/
      app/              # Next.js App Router pages
        globals.css     # Design system (20+ HSL tokens)
        layout.tsx      # Root layout (fonts + QueryProvider)
        page.tsx        # Home page
      components/
        layout/         # AppLayout, Sidebar, etc.
        ui/             # shadcn/ui components (button, card, badge, skeleton)
        dashboard/      # Project-specific feature components
      lib/
        api.ts          # Typed fetch wrapper with cache
        utils.ts        # cn() utility
        query-provider.tsx  # React Query setup
      hooks/
        use-api.ts      # Generic React Query hooks
tests/
  unit/                 # Fast, isolated tests
  integration/          # API + DB tests
  e2e/                  # End-to-end tests
docs/
  spec.md               # Product specification
  plan.md               # Implementation plan
  architecture.md       # Architecture decisions
  openapi-pattern.md    # OpenAPI-first codegen guide
  changelog.md          # Change log
```

## Development Commands

```bash
# === Backend ===
uv pip install -e ".[dev]"
uvicorn src.backend.main:app --reload --port 8000

# === Frontend ===
cd src/frontend && npm install
cd src/frontend && npm run dev       # Dev server on :3000
cd src/frontend && npm run build     # Production build (must pass clean)

# === Quality (Backend) ===
ruff check src/ tests/ --fix
ruff format src/ tests/
mypy src/
pytest tests/unit/ -v
pytest tests/ --cov=src

# === Pre-commit ===
pre-commit install
pre-commit run --all-files
```

## Quality Rules

1. **TDD enforced** — Write test first (RED), implement (GREEN), refactor. No code without tests.
2. **Type hints everywhere** — mypy strict mode (backend), TypeScript strict (frontend).
3. **Ruff clean** — Zero warnings. Auto-fix on save.
4. **Coverage >= 80%** — CI fails below threshold.
5. **`npm run build` must pass** — No TypeScript errors, no build warnings.
6. **Pre-commit hooks** — Must pass before every commit.

## Frontend Conventions

- **Brand system-of-record** — seed a root `DESIGN.md` (9-section schema) before styling. Drives the Claude Design pipeline (the Replit replacement for visual shaping). Scaffold + lane doctrine: `templates/claude-design-pipeline/`.
- **Design tokens** in `globals.css` — customize the `:root` HSL variables for your brand; they should trace to `DESIGN.md` §2/§3
- **shadcn/ui** for all UI primitives — add more with `npx shadcn add <component>`
- **React Query** for all API calls — use hooks from `use-api.ts`
- **Framer Motion** for animations — wrap components with `motion.div`
- **Mobile-first** — test on iPhone, collapsible sidebar included

## Git Workflow

- `main` — production, always deployable
- `develop` — integration branch
- `feature/<name>` — feature branches off develop
- Commit messages: imperative mood, concise ("Add session endpoint", "Fix telemetry parsing")

## Environment Variables

Copy `.env.example` to `.env` and fill in values. Never commit `.env`.

Frontend env (in `src/frontend/.env.local`):
- `NEXT_PUBLIC_API_URL` — Backend URL (default: `http://localhost:8000`)

## Vault Link

Project note: `05 Projects/World Vault.md` in HemySphere vault (Coding-Factory track, `status: research`).
Research + feasibility: `07 Resources/AI Agents & Agentic Systems/Worldmonitor App – Research.md`.
