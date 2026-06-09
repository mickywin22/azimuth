# OpenAPI-First Development Pattern

> Optional advanced pattern for projects with custom FastAPI backends.
> Generates typed React Query hooks and Zod schemas from your API spec.

---

## Why

Replit builds fast because it spends **0% of agent time on API plumbing**. With OpenAPI-first:

1. FastAPI auto-generates `openapi.json` at `/openapi.json`
2. **Orval** reads the spec and generates:
   - Typed React Query hooks (one per endpoint)
   - Zod validation schemas
   - TypeScript request/response types
3. Your frontend never writes `fetch()` calls manually

## Setup

### 1. Install Orval (frontend)

```bash
cd src/frontend
npm install -D orval
```

### 2. Create `orval.config.ts`

```typescript
import { defineConfig } from "orval";

export default defineConfig({
  api: {
    input: {
      target: "http://localhost:8000/openapi.json",
    },
    output: {
      mode: "tags-split",
      target: "src/api/generated",
      schemas: "src/api/models",
      client: "react-query",
      override: {
        mutator: {
          path: "./src/lib/api.ts",
          name: "apiFetch",
        },
        query: {
          useQuery: true,
          useMutation: true,
        },
      },
    },
  },
});
```

### 3. Add script to `package.json`

```json
{
  "scripts": {
    "generate-api": "orval",
    "dev": "orval && next dev"
  }
}
```

### 4. Usage

```bash
# Generate types from running backend
npm run generate-api

# Auto-generates:
# src/api/generated/*.ts  — React Query hooks
# src/api/models/*.ts     — Zod schemas + TypeScript types
```

### 5. Use in components

```tsx
import { useGetSessions } from "@/api/generated/sessions";

export function SessionList() {
  const { data, isLoading } = useGetSessions();

  if (isLoading) return <Skeleton />;
  return <ul>{data?.map(s => <li key={s.id}>{s.name}</li>)}</ul>;
}
```

## When to Use

- **Use it** when your project has a FastAPI backend with 5+ endpoints
- **Skip it** for simple projects or when using external APIs directly
- **Evaluate** after your backend spec stabilizes (don't generate from a moving target)

## Trade-offs

| Pro | Con |
|-----|-----|
| Zero manual fetch code | Extra build step (orval generation) |
| Type safety end-to-end | Learning curve for Orval config |
| React Query hooks auto-generated | Generated code can be verbose |
| Zod validation for free | Requires backend running for generation |

---

*Lesson learned from Replit's architecture — see [[05 Projects/Coding Factory]] for full analysis.*
