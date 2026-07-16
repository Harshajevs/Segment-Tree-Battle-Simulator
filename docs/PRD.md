# Product Requirements Document — Segment Tree Battle Simulator (Full-Stack)

## 1. Overview

Transform the existing C++ console demonstration of segment trees into a
full-stack web application: a playable, visual, turn-based battle game whose
every game mechanic is powered by segment-tree range queries, plus an
interactive visualizer that exposes the data structure itself. The project's
agenda is unchanged — demonstrating segment-tree proficiency — but the
demonstration becomes something anyone can open in a browser.

## 2. Problem statement

The current project proves algorithmic skill but cannot be demonstrated: the
build is broken, input data is missing, the only interface is a 200-prompt
stdin loop, and there is no way to *see* the data structure working. It also
contains correctness bugs (wrong-child recursion, wrong root index, scoring
always tied) that were never caught because there are no tests.

## 3. Current architecture & limitations

See [AUDIT.md](AUDIT.md). Summary: flat C++17 sources, ten duplicated
hand-written trees, interactive console `main()`, no tests/CI/frontend/
backend/persistence, broken CMake config, and eight verified defects.

## 4. Improvement opportunities

1. A REST backend that owns the battle engine and exposes tree operations.
2. A web frontend: battle arena + live segment-tree visualizer.
3. One **generic** segment tree parameterised by operation (kills ~450
   duplicated lines, same asymptotics).
4. A test suite that cross-checks every tree operation against naive O(n)
   computation (property-style), plus API and engine tests.
5. Deterministic, seedable matches persisted to a database and rehydratable
   by replaying the action log.
6. Optional AI battle commentary behind a provider interface (free/local
   providers only by default).

## 5. Functional requirements

### Game (parity with original, bugs fixed)
- FR1: Create a match with configurable team size (8–100,000), RNG seed,
  and max rounds; soldier stats are generated deterministically from the seed
  (replaces the missing `data/*.txt` files) or supplied explicitly.
- FR2: Teams alternate as attacker each round (fixes the always-Team-A bug).
- FR3: Attack resolution: `damage = max(0, attackSum(l₁,r₁) − healthSum(l₂,r₂))`
  over the attacker's chosen attack range and defender's chosen defence range.
  Damage is applied to the defender's **weakest soldier** (min-health index
  query) as a health reduction; the attacker's **strongest soldier**
  (max-attack index query) gains a small rally bonus. This preserves the
  original "query then point-update" flow while making the max/min trees
  load-bearing and the update semantics coherent.
- FR4: Every 10th round is a challenge round: both teams pick a range; GCD of
  attacker's attack vs. GCD of defender's health awards +50, LCM comparison
  awards +50 (preserves original bonus rules, extends LCM to also score).
- FR5: Match ends at max rounds or when a team's total health reaches 0;
  winner is the higher score.
- FR6: Every action is recorded in an ordered action log.

### Data-structure showcase
- FR7: Query playground: run any of the five operations (sum, max-index,
  min-index, GCD, LCM) on any attribute/range of either team, at any time.
- FR8: Tree visualizer: return the internal node array (levels, ranges,
  values) for any (team, attribute, operation) so the frontend can render the
  tree; point updates return the path of recomputed nodes for highlighting.
- FR9: Soldier grid: expose per-soldier stats for heatmap rendering
  (paginated / capped for large teams).

### Platform
- FR10: Matches persist (SQLite by default, Postgres via `DATABASE_URL`);
  in-memory engine state is rehydrated from seed + action-log replay after a
  restart.
- FR11: Optional AI commentary per action via pluggable providers: `local`
  (deterministic templates, zero credentials — default), `ollama`,
  `openrouter` (free models). Provider selected by environment variable;
  failures fall back to `local`.
- FR12: The legacy C++ implementation remains in `legacy/cpp/` with a working
  CMake build and a data generator, as the reference implementation.

## 6. Non-functional requirements

- NFR1: All range operations O(log n); match creation O(n log n); 100k-soldier
  matches must work (visualizer depth-capped, grid paginated).
- NFR2: Engine correctness proven by tests comparing against naive
  recomputation across randomized operation sequences.
- NFR3: Zero paid services required; runs fully offline with no credentials.
- NFR4: Typed end to end — Pydantic schemas on the API, TypeScript on the
  frontend.
- NFR5: 12-factor configuration via environment variables with sane defaults.
- NFR6: Structured logging; consistent JSON error envelopes; input validation
  on every endpoint.
- NFR7: New-developer setup ≤ 10 minutes from README alone.

## 7. Proposed architecture

```
┌─────────────────────┐        ┌──────────────────────────────┐
│ frontend/ (Vite +   │  HTTP  │ backend/ (FastAPI)           │
│ React + TS +        │──────▶ │  api/      thin routers      │
│ Tailwind)           │  JSON  │  schemas/  Pydantic models   │
│  arena · visualizer │        │  services/ match orchestration│
│  playground         │        │  engine/   SegmentTree +     │
└─────────────────────┘        │            BattleEngine (pure)│
                               │  ai/       commentary providers│
                               │  db/       SQLAlchemy + SQLite│
                               └──────────────────────────────┘
legacy/cpp/   original C++ (build fixed) — reference implementation
docs/         AUDIT / PRD / EXECUTION_PLAN
```

- **Engine layer is pure** (no I/O): a generic `SegmentTree` with pluggable
  associative operations, and a `BattleEngine` implementing the rules —
  independently unit-testable, mirrors the original's build/query/update split.
- **Service layer** owns match lifecycle: create, act, rehydrate-from-DB,
  and calls the commentary provider.
- **API layer** is thin routers + validation only.
- **AI providers** implement one `CommentaryProvider` protocol; adding a paid
  provider later is one new class + one env var.

## 8. Technology recommendations

| Layer | Choice | Rationale |
|---|---|---|
| Backend | Python 3.12+, FastAPI, Uvicorn | typed, async, OpenAPI for free |
| Validation | Pydantic v2 | schema-first API contracts |
| DB | SQLAlchemy 2.0 + SQLite (default) / Postgres (Neon) | zero-config locally, free managed option |
| Frontend | React 18 + TypeScript + Vite + Tailwind | modern default stack, fast builds |
| State | Zustand | minimal, no boilerplate for one arena store |
| Tests | pytest (engine/API), `tsc` + production build (frontend) | correctness first |
| AI | provider interface: local templates / Ollama / OpenRouter free models | free & open-source first, swappable |

## 9. Migration strategy

Strangler approach: the original C++ is never deleted — it moves to
`legacy/cpp/` (with its four build/correctness defects fixed so it actually
compiles and runs) and serves as the reference. The Python engine reimplements
identical semantics, proven by tests, then the web stack is built on top.
Original game rules are preserved except where the audit shows they were
bugs (scoring tie, no counterattack, set-vs-increase updates) — deviations are
documented in FR3/FR4.

## 10. Risks

| Risk | Mitigation |
|---|---|
| Python engine diverges from C++ semantics | property tests vs. naive ops; identity elements (sum 0, gcd 0, lcm 1) match originals |
| LCM overflow (pre-existing) | Python ints are arbitrary precision; values capped in schema (≤10⁶) to keep LCM display sane |
| 100k-soldier payloads too large for UI | tree endpoint depth-capped; soldier grid paginated |
| Free AI providers unavailable at runtime | `local` template provider is default & fallback; commentary is decorative, never blocks gameplay |
| Engine state lost on restart | deterministic seed + action-log replay rehydration |

## 11. Assumptions

- Single-player demo (one browser drives both teams); no auth needed — an
  auth layer would be scope creep for a DSA showcase.
- SQLite is acceptable for the demo tier; `DATABASE_URL` swaps to Postgres.
- No real-time multiplayer (no WebSockets) in this phase.

## 12. Execution roadmap

See [EXECUTION_PLAN.md](EXECUTION_PLAN.md) — 7 phases, each independently
testable and committed separately.

## 13. Success criteria

1. Fresh clone → README steps → running app in ≤ 10 minutes, no credentials.
2. `pytest` green, including randomized cross-checks of all 5 operations
   × 2 attributes against naive computation.
3. Frontend type-checks (`tsc`) and produces a production build.
4. A full match is playable in the browser end to end: create → attacks →
   challenge round → winner, with tree visualizer updating live.
5. Legacy C++ builds and runs with the fixed CMake config.
6. Deployable on free tiers (Render + Vercel/Cloudflare Pages + Neon) with
   documented steps.
