# azimuth — Multi-Tenancy Pattern

> **Status:** Draft
> **Last updated:** 2026-04-22
> **Source:** Emi Factory / Apex Phase K — Multi-User & Security scoping

## Why this doc exists

Every new Factory app has to answer one question early: *what does "tenant" mean here?* Getting this wrong once is painful — retro-fitting isolation after users accumulate state takes weeks. Getting it right once (and reusing the choice) is how the Factory keeps shipping.

This doc defines the **three shapes** a Factory app can take and how to pick one. Every new project note should open with an explicit pick.

---

## The three shapes

### Shape 1 — Shared data, per-user state

> *"One source of truth, many observers."*

The app hosts a single read-mostly dataset that every user sees. Users accumulate their own personalisation, history, favourites, budget against it — but the underlying data is shared.

**Example:** Apex. One FastF1 cache, one OpenF1 cache, one schedule. Per user: analysis history, starred sessions, Anthropic token budget, rate-limit bucket.

**Data model:**
- Domain tables (`sessions`, `laps`, `telemetry`) — no `user_id` column. Seeded once, served to all.
- User-state tables (`analyses`, `favourites`, `usage`) — FK to `users.id`, RLS-enforced to `auth.uid()`.
- Auth: any provider (NextAuth + Supabase adapter is Factory default).

**Isolation surface:**
- API: per-user rate limit (JWT sub → bucket), per-user Anthropic token budget, per-user history query filtered by `auth.uid()`.
- DB: RLS on user-state tables only. Domain tables readable by `authenticated` role.
- Cache: domain cache shared (keyed by domain key, e.g. `session:2025:monaco:race`). User cache keyed by `user_id`.

**When to pick:** data is expensive to fetch/compute, identical for everyone, and the product value is *the personal lens on shared data*.

**Trap:** leaking user state through a domain endpoint (e.g. `/api/sessions` quietly returning "your starred" flag without `auth.uid()` filter). Fix by keeping user-state API paths distinct (`/api/me/...`) and auditing cross-path leaks at review.

---

### Shape 2 — Per-tenant data, per-tenant state

> *"Each tenant is its own universe."*

Every tenant has its own dataset, its own users-within-tenant, its own analytics. Nothing bleeds across tenants. This is the classic B2B SaaS shape.

**Example:** a Factory app where each company uploads its own telemetry and can't see any other company's data.

**Data model:**
- Every table has a `tenant_id` column. Every query filters by `tenant_id`.
- Users belong to one tenant (simplest) or many (complicates auth claims; avoid until asked for).
- Auth: NextAuth + Supabase adapter, extend the JWT with `tenant_id` claim at sign-in.

**Isolation surface:**
- API: middleware extracts `tenant_id` from JWT, attaches to `request.state.tenant`. Every route *must* filter by it — this is the load-bearing invariant.
- DB: RLS using `auth.jwt()->>'tenant_id'`. Prefer a DB-side check over application-side — one missed `WHERE` clause is a data breach.
- Cache: key every cache entry with `tenant_id` prefix (`tenant:123:session:abc`). Never share cache across tenants even for identical domain keys — fingerprinting, side channels.

**When to pick:** customers pay for data isolation as a feature, or regulation requires it, or tenants' data schemas are genuinely disjoint.

**Trap:** one forgotten filter. Mitigation: a repo-wide Grep rule that every query function either (a) accepts `tenant_id` as a required arg, or (b) is marked `@shared` with a docstring explaining why. CI enforces.

---

### Shape 3 — Single-tenant throwaway

> *"Spin up, use, discard. State lives in the URL or the browser."*

No accounts, no DB, no server-side user state. Every visitor gets a clean canvas; their state lives in URL params, localStorage, or a signed share-link. Nothing to protect because there's nothing persistent.

**Example:** a visualiser that takes a CSV upload, renders a chart, lets you tweak, and gives you a share-URL encoding the config. Session ends when the tab closes.

**Data model:**
- None server-side. Or: ephemeral KV (Redis) with TTL ≤ 24h, keyed by an opaque random share-ID.
- Auth: none. Or: share-link signature only (signed-URL pattern).

**Isolation surface:**
- API: stateless. Rate-limit by IP only (no user bucket).
- DB: none. Or: ephemeral KV, keys scoped by random ID, TTL enforced.
- Cache: fine to share — data is public-by-construction anyway.

**When to pick:** no recurring users, no cross-session value, demo/showcase/utility apps, fastest to ship.

**Trap:** letting Shape 3 creep into Shape 1 territory without auth ("just one little login"). Once you add accounts you need isolation — that's a Shape 1 or Shape 2 rewrite, not an add-on. Pick one and stay disciplined.

---

## Picking the shape — 60-second decision

Answer in order, stop at first yes:

1. **Does the app need login at all?**
   - No → **Shape 3.**
2. **Does the app need to show different data to different tenants (companies, orgs)?**
   - Yes → **Shape 2.**
3. **Does the app host shared data that every user observes with personal state on top?**
   - Yes → **Shape 1.**

Default for Factory apps without a clear answer: **Shape 1.** It's the easiest to evolve to Shape 2 later (add `tenant_id`, migrate) and covers ~80% of "post-MVP multi-user" needs.

---

## Cross-shape invariants

Regardless of shape, every Factory app ships with:

- **CORS credentials scoped to matched origins only.** No `Access-Control-Allow-Credentials: true` echoed on origin mismatch (see Apex Phase K / `StrictCORSCredentialsMiddleware`).
- **Per-IP rate limit** on unauthenticated paths, even in Shape 3.
- **X-Real-IP trust model** — bucket key reads from the proxy-set header (unspoofable), with XFF leftmost as fallback (see Apex `get_client_ip()`).
- **Security headers** on every response (HSTS, XCTO, Referrer-Policy, Permissions-Policy).
- **Secrets scoped to `production` environment only** on Vercel — preview URLs are trivially generatable and must not see production secrets.

---

## How to extend this doc

When a new Factory app hits a multi-tenancy edge case not covered here (e.g. "users-span-tenants", "read-only audit tenants", "Shape 1 with tenant-scoped budgets"), add a short sub-section below with the project name + the chosen pattern + the trade-off. Don't rewrite the three shapes — they stay stable.

---

## See also

- Apex Phase K — Multi-User & Security Scoping (reference implementation of Shape 1)
- `docs/coolify-deploy.md` — deploy pattern
- `docs/openapi-pattern.md` — API contract pattern
