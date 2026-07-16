# Deployment Guide — free-tier options

The app is two deployables: the FastAPI backend and the static React build.
Everything below is on free tiers with zero paid services.

## Recommended architecture

```
Browser ──▶ Vercel / Cloudflare Pages (static frontend, free)
               │  VITE_API_URL
               ▼
            Render Web Service (FastAPI backend, free)
               │  DATABASE_URL
               ▼
            Neon Postgres (free)         [or Render's disk + SQLite]
               (optional) AI_PROVIDER=openrouter + free model
```

## 1. Backend on Render (free)

1. New → Web Service → connect the GitHub repo.
2. Root directory: `backend`
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Environment variables:
   - `DATABASE_URL` — Neon connection string (add `+psycopg2`-free URL as-is;
     install `psycopg2-binary` by adding it to `requirements.txt` when using
     Postgres)
   - `CORS_ORIGINS` — your frontend URL, e.g. `https://segtree-battle.vercel.app`
   - `AI_PROVIDER` — `local` (default) or `openrouter`
   - `OPENROUTER_API_KEY` — only if `AI_PROVIDER=openrouter`

**Free-tier limitation:** Render spins the service down after ~15 min idle;
first request after that takes ~30–60 s (cold start). In-memory engines are
dropped on spin-down, but replay rehydration restores any match from the
database transparently — this codepath is tested.

## 2. Database on Neon (free)

1. Create a project → copy the connection string.
2. Add `psycopg2-binary>=2.9` to `backend/requirements.txt`.
3. Set `DATABASE_URL=postgresql://…` on Render. Tables are created on startup.

SQLite alternative: skip Neon entirely; Render's ephemeral disk resets on each
deploy, which is fine for a demo (fresh leaderboard per deploy).

## 3. Frontend on Vercel (free) — or Cloudflare Pages

1. Import the repo → framework preset **Vite**, root directory `frontend`.
2. Build command `npm run build`, output `dist`.
3. Environment variable: `VITE_API_URL=https://<your-render-service>.onrender.com`
4. For SPA routing add a rewrite: all paths → `/index.html`
   (`vercel.json`: `{"rewrites": [{"source": "/(.*)", "destination": "/index.html"}]}`).

Cloudflare Pages is equivalent (build `npm run build`, output `dist`,
`_redirects` file: `/* /index.html 200`).

## 4. AI commentary (optional, still free)

- **Default (`local`)** — deterministic templates, zero setup, works offline.
- **OpenRouter** — create a free key at openrouter.ai, set
  `AI_PROVIDER=openrouter` and `OPENROUTER_API_KEY`. The default model
  (`meta-llama/llama-3.3-70b-instruct:free`) costs nothing; free models are
  rate-limited, and any failure silently falls back to `local`.
- **Ollama** — for local development only (`AI_PROVIDER=ollama`,
  `ollama pull llama3.2`); free hosts can't run it.

## 5. Cost & limits summary

| Piece | Platform | Cost | Main limitation |
|---|---|---|---|
| Backend | Render free | $0 | cold starts, 512 MB RAM (100k-soldier matches fit; ~10 concurrent large matches don't) |
| Frontend | Vercel/CF Pages free | $0 | none meaningful for this app |
| DB | Neon free | $0 | 0.5 GB storage, autosuspend |
| AI | OpenRouter free models | $0 | rate limits; falls back to local |

## 6. Future production migration

- Move the engine registry to Redis-backed snapshots (or sticky sessions)
  before scaling past one backend instance — replay keeps single-instance
  deploys correct today.
- Swap Render free → Fly.io / Railway paid for always-on latency.
- Add Alembic migrations before the first schema change in production.
- Rate-limit `POST /api/matches` (team_size=100000 costs ~2 s CPU per match).
