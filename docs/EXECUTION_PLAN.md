# Execution Plan — Segment Tree Battle Simulator Modernization

Each phase is one logical commit, independently testable, with rollback =
`git revert` of that commit. Phases build strictly bottom-up so the project is
never in a broken intermediate state.

---

## Phase 1 — Documentation baseline
- **Objective:** Land audit, PRD, and this plan before any code changes.
- **Scope / files:** `docs/AUDIT.md`, `docs/PRD.md`, `docs/EXECUTION_PLAN.md`.
- **Risks:** none (docs only).
- **Testing:** n/a. **Rollback:** revert commit.

## Phase 2 — Legacy preservation & repair
- **Objective:** Move the original C++ to `legacy/cpp/` in the directory
  layout its CMake config always expected, and fix the four defects that
  prevent it from building/running correctly (CMake paths, missing data,
  wrong-child recursion, node-0 root). The original remains the reference
  implementation.
- **Scope / files:** `legacy/cpp/{include,src,app,scripts}/…`,
  `legacy/cpp/CMakeLists.txt`, data generator script; root-level `.cpp/.h`
  files removed from root.
- **Risks:** behavioural change from bug fixes — intended and documented.
- **Testing:** `cmake --build` + a scripted non-interactive smoke run
  (documented; CMake optional on dev machines since the Python engine is the
  go-forward implementation).
- **Rollback:** revert commit (root files restored).

## Phase 3 — Backend engine (pure domain layer)
- **Objective:** Generic `SegmentTree` (one implementation, five pluggable
  operations: sum, max-index, min-index, gcd, lcm) + `BattleEngine`
  implementing the preserved game rules (alternating attackers, range-sum
  damage, weakest-soldier damage application, strongest-soldier rally,
  10th-round GCD/LCM challenges, win conditions).
- **Scope / files:** `backend/app/engine/*.py`, `backend/tests/test_engine_*.py`.
- **Risks:** semantic divergence from original → mitigated by randomized
  property tests vs. naive O(n) recomputation for all op × attribute pairs.
- **Testing:** `pytest backend/tests` — tree correctness (build, query,
  update, randomized sequences, edge ranges), battle rules, determinism by seed.
- **Rollback:** revert commit; nothing depends on it yet.

## Phase 4 — Persistence + service + REST API
- **Objective:** SQLAlchemy models (matches, actions), match service with
  seed+replay rehydration, FastAPI app with typed routes: create/get match,
  act (attack/challenge), arbitrary range query, tree visualization payload,
  soldier grid, health. Structured logging, JSON error envelope, CORS, config
  via env.
- **Scope / files:** `backend/app/{api,schemas,services,db,core}/…`,
  `backend/tests/test_api.py`, `backend/requirements.txt`, `.env.example`.
- **Risks:** state rehydration correctness → covered by a restart-simulation
  test (drop in-memory cache, replay from DB, assert identical state).
- **Testing:** pytest with FastAPI `TestClient` covering every route +
  validation failures + rehydration.
- **Rollback:** revert commit; engine layer unaffected.

## Phase 5 — AI commentary providers
- **Objective:** `CommentaryProvider` protocol; `local` deterministic template
  provider (default, zero credentials); `ollama` and `openrouter` (free
  models) implementations selected by `AI_PROVIDER` env var with automatic
  fallback to `local` on any failure. Commentary attached to action responses.
- **Scope / files:** `backend/app/ai/*.py`, provider tests (network providers
  tested via injected fake transport — no real calls in CI).
- **Risks:** provider outages → decorative feature, hard fallback, never
  blocks gameplay.
- **Testing:** pytest — template determinism, fallback path, provider selection.
- **Rollback:** revert commit; API returns commentary from `local` only.

## Phase 6 — Frontend
- **Objective:** Vite + React + TS + Tailwind app: match setup screen, battle
  arena (soldier heatmap grids, range selectors, action resolution, scores,
  action log with commentary, challenge-round flow), segment-tree visualizer
  (SVG, per team/attribute/operation, update-path highlighting), query
  playground. Zustand store, typed API client, loading/error states, code
  splitting per page.
- **Scope / files:** `frontend/**`.
- **Risks:** payload size at 100k soldiers → grid pagination + tree depth cap
  (already in API design).
- **Testing:** `tsc --noEmit`, production `vite build`, manual E2E pass of a
  full match against the running backend.
- **Rollback:** revert commit; backend fully functional standalone.

## Phase 7 — README & deployment docs
- **Objective:** Rewrite README: architecture, stack, setup, env vars, run
  backend/frontend/AI, DB setup, testing, troubleshooting, structure, future
  work. Add free-tier deployment guide (Render + Vercel/Cloudflare + Neon,
  Ollama/OpenRouter options) and credentials checklist.
- **Scope / files:** `README.md`, `docs/DEPLOYMENT.md`.
- **Testing:** follow README on a clean checkout mentally / command-by-command.
- **Rollback:** revert commit.

---

### Cross-cutting rules
- Every commit: project builds, all tests pass, one logical change, clean
  message, single author.
- No secrets in the repo; `.env.example` documents every variable.
- No paid services anywhere in the default path.
