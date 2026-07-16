# ⚔️ Segment Tree Battle Simulator

[![CI](https://github.com/Harshajevs/Segment-Tree-Battle-Simulator/actions/workflows/ci.yml/badge.svg)](https://github.com/Harshajevs/Segment-Tree-Battle-Simulator/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](https://opensource.org/licenses/MIT)

A full-stack, turn-based battle game where **every game mechanic is a segment
tree operation** — range sums resolve damage, min/max index queries pick
targets and champions, and GCD/LCM range queries drive challenge rounds. All
queries and updates run in O(log n) over teams of up to 100,000 soldiers, and
an interactive visualizer shows the tree recomputing live.

Originally a C++17 console project (Data Structures, Sep–Nov 2024, under
Dr. Anil Shukla); now modernized into a web application while preserving the
original game and algorithms. The original C++ lives on in
[`legacy/cpp/`](legacy/cpp/) as the reference implementation.

## Architecture

```
frontend/  React 19 + TypeScript + Vite + Tailwind (arena, visualizer, playground)
   │ REST/JSON
backend/   FastAPI (Python)
   ├─ api/       thin routers + validation
   ├─ schemas/   Pydantic contracts (big-int-safe serialisation)
   ├─ services/  match lifecycle, replay-based rehydration
   ├─ engine/    generic SegmentTree × 5 operations + battle rules (pure, no I/O)
   ├─ ai/        commentary providers: local (default) | Ollama | OpenRouter
   └─ db/        SQLAlchemy 2.0 — SQLite locally, Postgres via DATABASE_URL
legacy/cpp/  original C++17 implementation (CMake, reference)
docs/        AUDIT · PRD · EXECUTION_PLAN · DEPLOYMENT
```

**Key design points**

- **One generic segment tree** parameterised by operation (sum, max-index,
  min-index, GCD, LCM) replaces ten hand-written trees — identical
  asymptotics, ~450 fewer duplicated lines, property-tested against naive
  O(n) recomputation.
- **Deterministic matches**: armies are generated from a seed; every action is
  persisted; a restarted server rebuilds any match by replaying its action
  log. No engine state is ever serialised.
- **AI commentary is pluggable and optional**: a zero-credential template
  provider is the default; Ollama (local) and OpenRouter (free hosted models)
  are one env var away, and every failure falls back to the local provider.

## The game

1. Two armies are generated from a seed (attack + health per soldier).
2. Teams alternate as attacker. The attacker picks an attack range, the
   defender a defence range: `damage = max(0, attackSum − defenseSum)`.
3. Damage lands on the defender's **weakest** soldier (min-health index
   query); the attacker's **strongest** soldier (max-attack index query)
   gains a rally bonus.
4. Every 10th round is a **GCD/LCM challenge** — +50 points per duel won.
5. Match ends at max rounds (higher score wins) or when an army is wiped out.

## Quick start

Prerequisites: Python 3.12+, Node 20+. No credentials needed.

### Backend

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload          # http://localhost:8000 (docs at /docs)
```

### Frontend

```bash
cd frontend
npm install
npm run dev                            # http://localhost:5173 (proxies /api to :8000)
```

Open http://localhost:5173, start a battle (32–64 soldiers recommended for
the visualizer), and play.

### Legacy C++ (optional)

```bash
cd legacy/cpp
python3 scripts/generate_data.py       # generates the 100k-soldier input files
cmake -B build && cmake --build build
./build/SegmentTreeGame
```

## Configuration

All variables are optional — see [`backend/.env.example`](backend/.env.example).

| Variable | Default | Purpose |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./battle.db` | any SQLAlchemy URL (Neon Postgres works) |
| `CORS_ORIGINS` | `http://localhost:5173,…` | allowed frontend origins |
| `AI_PROVIDER` | `local` | `local` \| `ollama` \| `openrouter` |
| `OLLAMA_BASE_URL` / `OLLAMA_MODEL` | `http://localhost:11434` / `llama3.2` | when `AI_PROVIDER=ollama` |
| `OPENROUTER_API_KEY` / `OPENROUTER_MODEL` | – / `…llama-3.3-70b…:free` | when `AI_PROVIDER=openrouter` |
| `LOG_LEVEL` | `INFO` | backend log verbosity |

Frontend: `VITE_API_URL` (build-time) — leave unset in dev (Vite proxy) and
for same-origin deploys; set to the backend URL for split deploys.

## API overview

Interactive OpenAPI docs at `/docs`. Highlights:

| Endpoint | Purpose |
|---|---|
| `POST /api/matches` | create match `{team_size, seed, max_rounds, challenge_interval}` |
| `POST /api/matches/{id}/actions` | play `{type: attack\|challenge, attack_range, defense_range}` |
| `GET /api/matches/{id}/query` | any range query: `team, attribute, operation, left, right` |
| `GET /api/matches/{id}/tree` | segment-tree nodes for visualization (depth-capped) |
| `GET /api/matches/{id}/soldiers` | paginated soldier stats |
| `GET /api/matches/{id}/actions` | full action log with commentary |

## Testing

```bash
cd backend && .venv/bin/python -m pytest    # 43 tests
cd frontend && npx tsc -b && npm run build  # type-check + production build
```

The engine suite cross-checks every operation × attribute against naive O(n)
recomputation over randomized update/query sequences, and the API suite
covers every endpoint including restart rehydration. CI runs all of it plus
the legacy C++ build on every push.

## Troubleshooting

- **Frontend shows "Could not reach the backend"** — the API isn't running on
  port 8000, or you changed ports without updating the Vite proxy/`VITE_API_URL`.
- **`pip install` fails on Python < 3.12** — upgrade Python; SQLAlchemy/Pydantic
  versions here target modern interpreters.
- **Match creation is slow for 100k soldiers** — expected (~2 s: 10 trees ×
  400k nodes are built); queries afterwards are sub-millisecond.
- **CORS errors in split deploys** — set `CORS_ORIGINS` on the backend to the
  exact frontend origin (scheme + host, no trailing slash).
- **Ollama commentary silent** — `ollama serve` must be running and the model
  pulled; failures fall back to local templates by design (check backend logs).

## Deployment

Free-tier guide (Render + Vercel/Cloudflare Pages + Neon, optional OpenRouter):
[`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md).

## Project documents

- [`docs/AUDIT.md`](docs/AUDIT.md) — audit of the original codebase (including
  the bugs fixed during modernization)
- [`docs/PRD.md`](docs/PRD.md) — product requirements for this rebuild
- [`docs/EXECUTION_PLAN.md`](docs/EXECUTION_PLAN.md) — the phased plan the
  commit history follows

## Future improvements

- WebSocket push for real multiplayer (two browsers, one match)
- Lazy-propagation range updates (area-of-effect damage in O(log n))
- Alembic migrations; Redis-backed engine registry for multi-instance deploys
- Replay viewer: step through any finished match action by action

## License & attribution

MIT — **Author:** Kammari HarshaVardhan ([Harshajevs](https://github.com/Harshajevs))
