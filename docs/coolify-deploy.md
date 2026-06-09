# Coolify Deploy — Factory Default (post-Phase-J)

Canonical recipe for shipping a factory-template app to the Hetzner+Coolify shared backend. Supersedes Render for all new factory apps (Render decommissioned Phase J7, 2026-04-21).

## Prereqs

- Hetzner VM `emi-factory-1` live at `coolify.emi-factory.dev` (Phase J2)
- App repo on GitHub, branch `main`, private or public
- Repo layout: `src/backend/Dockerfile` + `.dockerignore` at repo root
- Coolify GitHub App `codify-emi-factory` installed and scoped to the app repo
- Env vars exported locally (`.env` or password manager)
- Coolify API token in `HemySphere/.env` under `COOLIFY_API_TOKEN`

## Deploy via API (autonomous, preferred)

Autonomous agent path. All calls to `https://coolify.emi-factory.dev/api/v1/...` with `Authorization: Bearer $COOLIFY_API_TOKEN`.

1. **Create project.** `POST /projects` with `{"name": "<app>"}` → capture project UUID from response.
2. **Create application.** `POST /applications/private-github-app` with:
   ```json
   {
     "project_uuid": "<project-uuid>",
     "server_uuid": "<localhost-server-uuid>",
     "environment_name": "production",
     "github_app_uuid": "<github-app-uuid>",
     "git_repository": "mickywin22/<repo>",
     "git_branch": "main",
     "build_pack": "dockerfile",
     "base_directory": "/",
     "dockerfile_location": "src/backend/Dockerfile",
     "ports_exposes": "8000",
     "domains": "https://<app>-api.emi-factory.dev"
   }
   ```
   → capture application UUID.
3. **Post env vars.** One-by-one via `POST /applications/{uuid}/envs` with minimal payload:
   ```json
   {"key": "ANTHROPIC_API_KEY", "value": "sk-ant-..."}
   ```
   **Do not include `is_build_time`** — Coolify v4 rejects it on `POST`. Use a separate `PATCH` if you need build-time semantics.
4. **Add persistent volume** (if the app needs disk state, e.g. cache dir) via `POST /applications/{uuid}/storages`:
   ```json
   {
     "name": "<app>-cache",
     "mount_path": "/app/.cache",
     "type": "persistent"
   }
   ```
   Storage `type` **must be `persistent`** — `volume` / `bind` / `named` are rejected.
5. **Deploy.** `POST /deploy` with `{"uuid": "<application-uuid>"}` → poll the returned deployment UUID via `GET /deployments/{uuid}` until `status: finished`.
6. **Verify.**
   ```bash
   curl -sS https://<app>-api.emi-factory.dev/health | jq
   curl -sI https://<app>-api.emi-factory.dev/health | grep -i strict-transport-security
   ```

Build time budget: 120–180s for a factory-template-sized FastAPI app. If >5 min, pull `GET /deployments/{uuid}` logs and check for cache misses.

## Deploy via UI (manual fallback)

Use when the API workflow errors or when scaffolding a new app interactively.

1. Coolify → **+ New Resource → Application → Private Repo (GitHub App)**.
2. Pick the repo + branch `main`.
3. Build pack: **Dockerfile**. Base directory `/`. Dockerfile path `src/backend/Dockerfile`.
4. Domain: `https://<app>-api.emi-factory.dev`. Coolify auto-issues Let's Encrypt.
5. Environment variables: paste from password manager. One per row. No build-time flag on first pass.
6. Persistent volumes: if needed, add mount path `/app/.cache` with type **persistent**.
7. Click **Deploy**. Watch the build log live.

Reference implementation: [Apex Phase J Runbook J3](https://github.com/mickywin22/HemySphere/blob/master/05%20Projects/Apex%20Phase%20J%20Runbook.md) in the vault.

## DNS

Each app needs a subdomain pointing at the Hetzner VM.

- `A  <app>-api.emi-factory.dev  →  46.225.209.47`
- **DNS-only** (grey cloud in Cloudflare) — orange proxy breaks Let's Encrypt HTTP-01 challenge
- TTL 300 for the first 24h, drop to 3600 after stable

## CORS

Factory convention: backend reads `CORS_ORIGINS_STR` env var (note the `_STR` suffix — Pydantic reads this exact name, not `CORS_ORIGINS`). Comma-separated list of allowed origins. Example:

```
CORS_ORIGINS_STR=https://<app>.vercel.app,https://<app>.emi-factory.dev
```

## Gotchas (learned the hard way — Apex J3, 2026-04-20)

- **`is_build_time` field rejected on `POST /envs`** — use minimal `{key, value}` payload. If you need build-time semantics, separate `PATCH` after creation.
- **Storage `type` must be `persistent`** — `volume`, `bind`, `named` all rejected by the Coolify v4 validator.
- **Git-Bash on Windows rewrites `/`-prefixed argv** — any argv value starting with `/` gets translated to `C:/Program Files/Git/...`. Pass paths via JSON file payload or Python `urllib`, never via shell argv. Bites scripts that POST env vars with absolute mount paths.
- **CORS origin exact match required** — no wildcards, no trailing slash tolerance. Watch the `_STR` suffix.
- **Auto-deploy on `main` push** — wired by the GitHub App webhook. No extra CI glue needed. Trust the webhook; if a push doesn't trigger, check the Coolify GitHub App's installation is active (not expired).
- **`/data/coolify/` permissions** — if a server was hardened before Coolify install, the top-level data dir may need `chmod 755` traversal perms for the non-root user. Dir perms only; file perms stay 600.

## Multi-tenancy

The CX23 VPS (2 vCPU / 4GB RAM) hosts N factory apps via shared Traefik + shared Let's Encrypt. Validated with Apex (J3–J5, 2026-04-20) and throwaway `hello-fastapi` (J8 pending). Budget headroom: Apex uses ~800MB steady-state → plenty for 3–5 factory apps on one VM.

**Escalate to CX31 (8GB / €10/mo) if:** RAM > 75% at 2 apps.
**Escalate to per-app VM if:** cross-contamination (log noise, port conflicts) observed.

## Rollback

Each factory app should keep its prior deploy (Render, Fly, whatever) as a 7-day rollback buffer after cutover. If regression surfaces: flip the frontend's `NEXT_PUBLIC_API_URL` env back to the old URL in Vercel, redeploy, done. 5-min RTO. After 7 days clean, suspend the old service. After 14 days clean, delete.

## Cost

| Item | Monthly | Notes |
|------|---------|-------|
| Hetzner CX23 (2 vCPU / 4GB / 40GB NVMe) | €4.51 | shared across N factory apps |
| IPv4 address | €0.58 | included above |
| Domain `emi-factory.dev` | €0.92 | €11/yr via Cloudflare Registrar |
| Let's Encrypt TLS | €0 | auto-renew via Traefik |
| GitHub (private repos) | €0 | free tier |
| **Total** | **~€6/mo** | one VM hosts the whole factory |

Replaces: Render Pro ($30/mo per app after free tier deprecated). Savings compound with each new factory app.
