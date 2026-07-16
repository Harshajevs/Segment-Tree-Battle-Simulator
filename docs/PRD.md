# Product Requirements Document

## Segment Tree Battle Simulator

| Document field | Value |
|---|---|
| Product | Segment Tree Battle Simulator |
| Release | Full-stack MVP |
| Document version | 2.0 |
| Status | Implementation-aligned product baseline |
| Last updated | 16 July 2026 |
| Primary audience | Product reviewers, engineers, educators, contributors |
| Related documents | [Repository audit](AUDIT.md) · [Execution plan](EXECUTION_PLAN.md) · [Deployment guide](DEPLOYMENT.md) |

> **Product promise:** turn an abstract data structure into a battle that is playable, inspectable, deterministic, and easy to explain from the first click to the final tree update.

---

## 1. Executive summary

The Segment Tree Battle Simulator is an educational, full-stack strategy game in which every important game mechanic is powered by a segment-tree operation. Players select ranges of soldiers, resolve attacks with range sums, identify champions and targets with max/min index queries, and enter periodic GCD/LCM challenge rounds. A dedicated visualizer exposes the tree layout and a query playground lets users inspect the same data structure independently of gameplay.

The product modernizes the original C++17 console project without discarding it. The web application is the primary experience; the repaired C++ implementation remains under **legacy/cpp** as a reference. The backend is authoritative for game rules and persistence, while the frontend is responsible for interaction, presentation, and exploration.

This PRD serves two purposes:

1. Define the complete product experience and system behavior end to end.
2. Separate the delivered MVP from explicitly deferred work so the project scope remains credible.

### 1.1 Product at a glance

| Dimension | Definition |
|---|---|
| Core value | Make segment-tree behavior visible through a memorable game |
| Primary mode | One browser controls both teams in a deterministic match |
| Supported scale | 8–100,000 soldiers per team |
| Core operations | Sum, max index, min index, GCD, LCM |
| Default runtime | Fully local, SQLite, deterministic commentary, no credentials |
| Persistence model | Match configuration plus ordered action log; live engine rebuilt by replay |
| Main surfaces | Match setup, battle arena, tree visualizer, query playground |
| Explicit non-goal | Real-time multiplayer in the MVP |

---

## 2. Product foundation

### 2.1 Problem

The original project demonstrates segment-tree algorithms but makes them difficult to experience or evaluate:

- The interaction is a long terminal loop rather than a demonstrable product.
- The tree and its recomputation path are invisible.
- Missing data and build defects prevent a reliable first run.
- Duplicated tree implementations make correctness difficult to maintain.
- There is no API, frontend, persistence, test suite, or restart recovery.
- Verified defects in recursion, root indexing, scoring, and overflow weaken trust in the demonstration.

The complete baseline audit is recorded in [AUDIT.md](AUDIT.md).

### 2.2 Vision

> A learner should be able to play one round, see which segment-tree operations resolved it, inspect the affected tree, and understand why the result was produced.

### 2.3 Product principles

| Principle | Product implication |
|---|---|
| **Algorithm first** | Game mechanics must use segment-tree queries or point updates; the tree is not decorative. |
| **Visible causality** | The interface must connect a selected range to its query result, affected soldier, score change, and tree state. |
| **Deterministic by design** | The same seed and ordered actions must recreate the same armies and match state. |
| **Progressive disclosure** | The arena is approachable; deeper tree internals remain one navigation step away. |
| **Offline by default** | Core gameplay, persistence, tests, and commentary work without paid services or credentials. |
| **Truth over spectacle** | Large-team limits, big integers, persistence boundaries, and deferred features are documented explicitly. |

### 2.4 Target users

| Persona | Job to be done | Success moment |
|---|---|---|
| Data-structure learner | Understand how queries and point updates affect a segment tree | Connects a battle result to the exact operation and range |
| Interviewer or evaluator | Assess algorithmic depth and software-engineering quality quickly | Can run, inspect, and verify the system without reading every source file |
| Educator or demonstrator | Explain segment trees through an interactive example | Uses the arena and visualizer to show build, query, and propagation |
| Contributor | Extend operations, rules, providers, or UI safely | Finds clear boundaries, contracts, invariants, and tests |

### 2.5 Goals and success measures

| Goal | Measure |
|---|---|
| Make the core concept understandable | Every resolved action names or displays the operation inputs and outcome |
| Make the project demonstrable | A fresh local setup reaches a playable match in 10 minutes or less using the README |
| Preserve algorithmic rigor | All five operations are checked against naive recomputation in automated tests |
| Support meaningful scale | A 100,000-soldier team can be created and queried without changing the API contract |
| Survive restarts | A persisted match returns to the same round, scores, armies, and winner after replay |
| Avoid service dependency | The complete default path works with SQLite and local commentary |
| Keep the code explainable | Domain rules remain pure and independent of HTTP, database, and AI code |

---

## 3. Scope and release boundaries

### 3.1 Delivery legend

| Label | Meaning |
|---|---|
| **Delivered** | Present in the current full-stack MVP |
| **Partial** | Backend or enabling contract exists, but the end-user flow is incomplete |
| **Next** | Logical next-release work, excluded from MVP completion |
| **Future** | Directional idea requiring a new scope decision |

### 3.2 In scope for the full-stack MVP

- Deterministic match creation from team size, seed, maximum rounds, and challenge interval.
- Recent-match listing and reopening.
- Alternating Team A and Team B attackers.
- Sum-based attacks, min-health targeting, max-attack rally updates, and score accumulation.
- GCD/LCM challenge rounds at a configurable interval.
- Match completion by army wipeout or round limit.
- Ordered, persisted action history with optional commentary.
- Paginated soldier heatmaps and explicit range controls.
- Tree snapshots for team × attribute × operation, capped by depth.
- An arbitrary O(log n) query playground.
- SQLite by default and a configurable SQLAlchemy database URL.
- Engine rehydration from deterministic seed plus action replay.
- Local, Ollama, and OpenRouter commentary providers with local fallback.
- Typed REST contracts and structured domain errors.
- Backend tests, frontend type/build checks, and legacy C++ build validation in CI.
- The repaired original C++ project retained as a reference implementation.

### 3.3 Explicitly deferred

| Capability | Status | Rationale |
|---|---|---|
| Highlight the last recomputation path inside the visualizer | Partial | The backend returns update node paths; the visualizer does not yet consume them across routes. |
| Step-by-step replay viewer | Next | Action data is already persisted, but replay controls and historical tree frames need a dedicated UX. |
| Automated frontend component and end-to-end browser tests | Next | MVP currently validates TypeScript and production builds; interaction regression coverage remains a gap. |
| Accessibility completion and keyboard-only range selection | Next | Native controls exist, but the soldier grid and visual encoding need a full accessibility pass. |
| Match deletion, retention policy, and archive controls | Next | Persistence currently retains matches indefinitely. |
| Engine-cache eviction and per-match mutation locking | Next | Required before broader multi-user or long-running hosted usage. |

### 3.4 Out of scope for the MVP

- Authentication, accounts, roles, or private matches.
- Real-time two-browser multiplayer and WebSocket synchronization.
- Ranked matchmaking, leaderboards, payments, or social features.
- AI decision-making for teams; AI is commentary only.
- Paid infrastructure or a required external model provider.
- Range updates or lazy propagation.
- Multi-instance engine coordination, Redis snapshots, or global scale.
- User-supplied executable code or custom operation definitions.
- Replacing the Python engine with the legacy C++ binary.

### 3.5 Future options

- Real-time multiplayer with server-authoritative turn ownership.
- Area-of-effect mechanics backed by lazy-propagation range updates.
- Replay timeline with historical tree states.
- Redis-backed engine snapshots and multi-instance deployment.
- Alembic migrations, rate limiting, retention rules, and operational dashboards.
- Custom army import with schema validation and deterministic export.

---

## 4. End-to-end product experience

### 4.1 Primary user journey

~~~mermaid
flowchart LR
    A["Open home"] --> B{"Choose entry"}
    B -->|"New match"| C["Configure team size<br/>seed · rounds · challenge interval"]
    B -->|"Recent match"| D["Open persisted match"]
    C --> E["Create deterministic armies<br/>and build segment trees"]
    D --> F["Load cached engine<br/>or rehydrate by replay"]
    E --> G["Battle arena"]
    F --> G
    G --> H["Select attacker and defender ranges"]
    H --> I{"Expected action"}
    I -->|"Attack"| J["Resolve sum, min-index,<br/>max-index, and point updates"]
    I -->|"Challenge"| K["Resolve GCD and LCM duels"]
    J --> L["Refresh scores, soldiers,<br/>highlights, log, commentary"]
    K --> L
    L --> M{"Match finished?"}
    M -->|"No"| G
    M -->|"Yes"| N["Show winner or tie"]
    G -.-> O["Tree visualizer<br/>and query playground"]
    O -.-> G
~~~

### 4.2 Product surfaces

| Surface | Route | Purpose | Essential content and actions |
|---|---|---|---|
| Home | **/** | Start or resume a match | Product explanation, match configuration, create action, recent matches, validation/error state |
| Arena | **/match/{id}** | Play and understand the current battle | Scoreboard, round/attacker, two soldier grids, range inputs, resolve action, last-result highlight, action log, commentary |
| Visualizer | **/match/{id}/visualizer** | Inspect the underlying data structure | Team/attribute/operation selectors, depth control, tree graph, payload/range labels, query playground |
| API documentation | **/docs** | Inspect and exercise typed contracts | OpenAPI-generated endpoint and schema documentation |

### 4.3 Information hierarchy

The arena must answer these questions in order:

1. **Whose turn is it and what action is expected?**
2. **Which ranges are selected?**
3. **What happened when the action resolved?**
4. **How did scores, soldier stats, and the round change?**
5. **Which data-structure operations caused that result?**
6. **Where can the user inspect the tree in more detail?**

### 4.4 UX and visual direction

- Use a dark tactical-arena theme with high-contrast content.
- Keep Team A and Team B visually stable across the product; never rely on color alone.
- Give challenge rounds a distinct treatment from ordinary attacks.
- Show health as an ordered, paginated soldier grid with textual values available per cell.
- Keep range boundaries editable by both direct numeric input and grid interaction.
- Explain max/min trees as storing the winning index, not the raw stat value.
- Truncate extremely large displayed values visually without losing the exact API value.
- Preserve usable layouts from mobile width through wide desktop screens.
- Every loading, empty, validation, unreachable-backend, not-found, and finished state must have a clear next action.

---

## 5. Game model and rules

### 5.1 Domain vocabulary

| Term | Meaning |
|---|---|
| Match | One deterministic contest between Team A and Team B |
| Team | An ordered array of soldiers and its derived segment trees |
| Soldier | One indexed pair of attack and health values |
| Round | Exactly one attack or one challenge action |
| Attacker | Team allowed to choose the attack range for the current round |
| Defender | The opposing team whose health range is selected |
| Challenge | A scheduled round comparing GCD and LCM rather than applying damage |
| Action log | Ordered canonical actions and outcomes persisted for history and replay |

### 5.2 Match configuration

| Field | Default | Valid range | Behavior |
|---|---:|---:|---|
| Team size | 32 | 8–100,000 | Number of soldiers generated for each team |
| Seed | 42 | 0–2³¹−1 | Produces deterministic Team A then Team B stats |
| Maximum rounds | 20 | 1–1,000 | Round-limit termination boundary |
| Challenge interval | 10 | 2–100 | Every Nth round expects a challenge |

Soldiers are generated in index order from one seeded pseudo-random stream:

- Attack is an integer from 50 through 200.
- Health is an integer from 500 through 1,500.
- The same configuration always produces the same initial armies.

### 5.3 Ordinary attack

For attacker range **[aL, aR]** and defender range **[dL, dR]**:

**damage = max(0, sum(attacker.attack[aL…aR]) − sum(defender.health[dL…dR]))**

Resolution order:

1. Validate both inclusive ranges against their teams.
2. Query the attack sum for the attacker.
3. Query the health sum for the defender.
4. Compute non-negative damage.
5. Query the minimum-health index inside the defender range.
6. Reduce that soldier’s health by damage, floored at zero.
7. Query the maximum-attack index inside the attacker range.
8. Apply a rally bonus equal to **max(1, floor(current attack ÷ 20))**.
9. Add damage to the attacking team’s score.
10. Record the result, advance match state, and persist the action.

Max/min ties resolve to the rightmost index, matching the operation strategy used by the engine. A rally occurs even when damage is zero, so each ordinary action still exercises a point update.

### 5.4 Challenge round

When **round mod challenge interval = 0**, the expected action is **challenge**:

1. Query GCD of the attacker’s selected attack range.
2. Query GCD of the defender’s selected health range.
3. Award 50 points to the team with the larger GCD; award nothing on a tie.
4. Query LCM over the same two ranges.
5. Award another 50 points to the team with the larger LCM; award nothing on a tie.
6. Record the result and advance the match without changing soldier stats.

### 5.5 Turn and termination flow

~~~mermaid
flowchart TD
    A["Receive validated action"] --> B{"Matches expected action?"}
    B -->|"No"| X["Reject with domain error<br/>state unchanged"]
    B -->|"Yes"| C{"Action type"}
    C -->|"Attack"| D["Run sum queries"]
    D --> E["Find weakest defender<br/>and strongest attacker"]
    E --> F["Apply health and rally<br/>point updates"]
    F --> G["Add damage to attacker score"]
    C -->|"Challenge"| H["Run GCD and LCM queries"]
    H --> I["Award up to two<br/>50-point bonuses"]
    G --> J["Evaluate end conditions"]
    I --> J
    J --> K{"Any team health = 0?"}
    K -->|"Yes"| L["Finish match<br/>other team wins"]
    K -->|"No"| M{"Round reached max?"}
    M -->|"Yes"| N["Finish match<br/>higher score wins or tie"]
    M -->|"No"| O["Increment round<br/>swap attacker"]
~~~

### 5.6 Match state machine

~~~mermaid
stateDiagram-v2
    [*] --> InProgress: match created
    state InProgress {
        [*] --> AttackExpected
        AttackExpected --> ChallengeExpected: next round is interval boundary
        AttackExpected --> AttackExpected: next round is ordinary
        ChallengeExpected --> AttackExpected: next round continues
    }
    InProgress --> FinishedByWipeout: team total health reaches zero
    InProgress --> FinishedByScore: maximum round resolves
    FinishedByWipeout --> [*]: surviving team wins
    FinishedByScore --> [*]: Team A, Team B, or tie
~~~

### 5.7 Game invariants

- Ranges are inclusive and satisfy **0 ≤ left ≤ right < team size**.
- Only the action named by **expected_action** may resolve.
- Exactly one action advances one round.
- Attackers alternate after every non-terminal round.
- Health and attack values never become negative.
- Only the defender can lose health during an ordinary attack.
- Scores never decrease.
- A finished match rejects further actions.
- Replaying the same ordered actions against the same configuration yields the same state.
- Wipeout takes precedence over score comparison.

---

## 6. Segment-tree product model

### 6.1 Trees created per match

Each team owns two mutable stat arrays. Each array is represented by five segment trees, producing **10 trees per team and 20 trees per match**.

~~~mermaid
flowchart LR
    M["Deterministic match seed"] --> A["Team A soldiers"]
    M --> B["Team B soldiers"]

    A --> AA["Attack array"]
    A --> AH["Health array"]
    B --> BA["Attack array"]
    B --> BH["Health array"]

    AA --> AAT["sum · max index · min index · GCD · LCM"]
    AH --> AHT["sum · max index · min index · GCD · LCM"]
    BA --> BAT["sum · max index · min index · GCD · LCM"]
    BH --> BHT["sum · max index · min index · GCD · LCM"]
~~~

All trees use the same generic implementation:

- 1-indexed internal nodes.
- Children at **2i** and **2i + 1**.
- Up to **4n** storage slots per tree.
- O(n) build.
- O(log n) range query.
- O(log n) point update.
- A leaf-to-root list of recomputed node IDs returned by updates.
- Breadth-first, depth-capped snapshots for rendering.

### 6.2 Operation traceability

| Operation | Node payload | Identity | Game use | Explorer use |
|---|---|---:|---|---|
| Sum | Aggregated value | 0 | Attack strength, defense strength, total team stats, damage | Range total |
| Max index | Index of highest stat | −1 | Select attacker champion | Find strongest soldier |
| Min index | Index of lowest stat | −1 | Select weakest defender | Find weakest soldier |
| GCD | Aggregated divisor | 0 | Challenge duel | Range GCD |
| LCM | Aggregated multiple | 1 | Challenge duel | Range LCM |

For max/min operations, the API returns both the winning index and the soldier’s underlying stat value. LCM values beyond JavaScript’s safe integer range are serialized as decimal strings.

### 6.3 Complexity and payload constraints

| Operation | Complexity | Product constraint |
|---|---|---|
| Build all trees for one match | O(n) with a fixed 20-tree multiplier | Team size capped at 100,000 |
| One range query | O(log n) | Inclusive, validated range |
| One stat assignment | Five O(log n) tree updates, asymptotically O(log n) | Updates all operations for that attribute |
| Ordinary attack | Constant number of O(log n) queries and updates | No full-array recomputation |
| Challenge | Four O(log n) queries | LCM may be returned as a string |
| Tree snapshot | O(number of exported nodes) | Depth 1–8; at most 511 nodes through depth 8 |
| Soldier page | O(page size) | API limit 1–1,024; arena requests 256 |
| Rehydration | O(n + actions × log n) | Ordered action log is canonical |

---

## 7. Functional requirements

### 7.1 Match lifecycle

| ID | Requirement | Acceptance criteria | Priority | Status |
|---|---|---|---|---|
| FR-01 | Create a configured match | Valid configuration returns a unique ID, two deterministic team summaries, round 1, Team A as attacker, and the correct expected action | P0 | Delivered |
| FR-02 | Reject invalid configuration | Values outside documented bounds return a typed validation error and create no match | P0 | Delivered |
| FR-03 | List recent matches | Home can retrieve recent matches ordered newest first with score, round, size, status, and winner | P0 | Delivered |
| FR-04 | Resume a match | Opening a stored ID returns current scores, teams, state, soldiers, and action history | P0 | Delivered |
| FR-05 | Recover after restart | On an engine-cache miss, the service rebuilds armies from the seed, replays actions in sequence, and returns equivalent state | P0 | Delivered |

### 7.2 Battle

| ID | Requirement | Acceptance criteria | Priority | Status |
|---|---|---|---|---|
| FR-06 | Enforce expected action | Ordinary rounds accept only attack; interval rounds accept only challenge; finished matches accept neither | P0 | Delivered |
| FR-07 | Resolve ordinary attacks | Result includes ranges, sums, damage, target and champion before/after values, update paths, and updated state | P0 | Delivered |
| FR-08 | Resolve challenges | Result includes GCD/LCM inputs, each duel winner or tie, bonus value, and updated state | P0 | Delivered |
| FR-09 | Alternate attackers | Every non-terminal action swaps the attacker exactly once | P0 | Delivered |
| FR-10 | Finish deterministically | Wipeout selects the surviving team; round limit selects higher score or tie; state exposes no further expected action | P0 | Delivered |
| FR-11 | Persist action history | Every successful action is stored once in sequence with canonical ranges, sanitized outcome, timestamp, and optional commentary | P0 | Delivered |
| FR-12 | Refresh affected UI state | After an action, arena refreshes authoritative match and visible soldier pages, appends the log, and highlights the last champion/target | P0 | Delivered |

### 7.3 Data-structure exploration

| ID | Requirement | Acceptance criteria | Priority | Status |
|---|---|---|---|---|
| FR-13 | Run arbitrary range queries | User selects team, attribute, operation, and valid bounds and receives the exact value; max/min also identify the stat value | P0 | Delivered |
| FR-14 | Render a tree snapshot | User selects team, attribute, operation, and depth and sees node payloads with covered ranges and parent-child edges | P0 | Delivered |
| FR-15 | Bound visualization payloads | Depth is restricted to 1–8 and large values remain lossless in transport | P0 | Delivered |
| FR-16 | Show soldier pages | User can inspect and paginate soldier attack/health values without loading the entire team | P0 | Delivered |
| FR-17 | Visualize update propagation | The latest action’s recomputed nodes are highlighted in the corresponding tree | P1 | Partial |

### 7.4 Commentary and platform

| ID | Requirement | Acceptance criteria | Priority | Status |
|---|---|---|---|---|
| FR-18 | Generate local commentary | Every action can receive deterministic, zero-credential commentary | P1 | Delivered |
| FR-19 | Support optional model providers | Ollama or OpenRouter may be selected through configuration; provider failure falls back to local without rolling back gameplay | P1 | Delivered |
| FR-20 | Keep AI decorative | Engine resolution and persisted outcome never depend on generated text | P0 | Delivered |
| FR-21 | Expose typed API contracts | Requests and responses are validated by Pydantic and mirrored by TypeScript types | P0 | Delivered |
| FR-22 | Return consistent domain errors | Not-found and domain failures use JSON error envelopes; schema failures use framework validation details | P0 | Delivered |
| FR-23 | Preserve the legacy project | The repaired C++17 reference builds independently through CMake and has reproducible input generation | P1 | Delivered |

---

## 8. System architecture

### 8.1 Component architecture

~~~mermaid
flowchart TB
    U["Player / learner"]

    subgraph FE["Frontend · React 19 + TypeScript + Vite"]
        HOME["Home and recent matches"]
        ARENA["Battle arena"]
        VIS["Tree visualizer and query playground"]
        STORE["Zustand match store"]
        CLIENT["Typed REST client"]
        HOME --> CLIENT
        ARENA <--> STORE
        VIS --> CLIENT
        STORE <--> CLIENT
    end

    subgraph BE["Backend · FastAPI"]
        ROUTES["Thin routes and Pydantic schemas"]
        SERVICE["MatchService orchestration"]
        ENGINE["Pure BattleEngine"]
        TREES["Generic SegmentTree and operations"]
        REGISTRY["In-process engine registry"]
        PROVIDER["Commentary provider factory"]
        LOCAL["Local templates"]
        REMOTE["Ollama or OpenRouter"]
        ROUTES --> SERVICE
        SERVICE <--> ENGINE
        ENGINE --> TREES
        SERVICE <--> REGISTRY
        ROUTES --> PROVIDER
        PROVIDER --> LOCAL
        PROVIDER -. optional .-> REMOTE
        REMOTE -. fallback .-> LOCAL
    end

    subgraph DATA["Persistence"]
        DB["SQLAlchemy<br/>SQLite default · Postgres configurable"]
        MATCHES["matches"]
        ACTIONS["actions"]
        DB --- MATCHES
        DB --- ACTIONS
    end

    LEGACY["legacy/cpp<br/>reference implementation"]

    U --> HOME
    U --> ARENA
    U --> VIS
    CLIENT <-->|"REST / JSON"| ROUTES
    SERVICE <-->|"config · actions · summaries"| DB
    LEGACY -. conceptual parity .-> ENGINE
~~~

### 8.2 Layer responsibilities

| Layer | Owns | Must not own |
|---|---|---|
| Frontend pages/components | Navigation, inputs, visible state, visualization, user feedback | Battle-rule authority or persistence |
| Frontend store/client | Request orchestration, transient ranges/pages, API typing | Reimplementation of damage or winner logic |
| API routes/schemas | HTTP validation, serialization, status codes, dependency wiring | Stateful match logic |
| Match service | Create/get/act lifecycle, engine registry, persistence, replay | Segment-tree algorithms |
| Battle engine | Rules, turn state, deterministic outcomes | HTTP, SQL, environment variables, model calls |
| Segment tree | Build/query/update/snapshot and operation semantics | Game scoring or persistence |
| Commentary providers | Decorative action narration | Any state mutation or winner decision |
| Database | Match configuration, denormalized summaries, canonical action log | Serialized live tree objects |
| Legacy C++ | Historical/reference implementation | Runtime dependency of the web app |

### 8.3 Action orchestration

~~~mermaid
sequenceDiagram
    actor Player
    participant UI as React arena
    participant API as FastAPI route
    participant SVC as MatchService
    participant ENG as BattleEngine
    participant DB as SQL database
    participant AI as Commentary provider

    Player->>UI: Select ranges and resolve
    UI->>API: POST action
    API->>SVC: act(match, request)
    SVC->>SVC: Load cached engine or rehydrate
    SVC->>ENG: apply(expected type, ranges)
    ENG->>ENG: Query trees, mutate stats, advance state
    ENG-->>SVC: Deterministic result and update paths
    SVC->>DB: Insert action and update match summary
    DB-->>SVC: Commit
    SVC-->>API: Action, state, result
    API->>AI: commentate(persisted result)
    alt Selected provider succeeds
        AI-->>API: Commentary
    else Provider fails or is unavailable
        AI-->>API: Local fallback commentary
    end
    API->>DB: Save commentary when present
    API-->>UI: Action response
    par Refresh authoritative match
        UI->>API: GET match
    and Refresh visible Team A page
        UI->>API: GET Team A soldiers
    and Refresh visible Team B page
        UI->>API: GET Team B soldiers
    end
    UI-->>Player: Scores, highlights, log, next action
~~~

### 8.4 Restart and replay orchestration

~~~mermaid
sequenceDiagram
    participant API as Request path
    participant SVC as MatchService
    participant CACHE as Engine registry
    participant DB as SQL database
    participant ENG as BattleEngine

    API->>SVC: get_engine(match_id)
    SVC->>CACHE: Lookup
    alt Cache hit
        CACHE-->>SVC: Live engine
    else Cache miss after restart or eviction
        SVC->>DB: Load match config and ordered actions
        DB-->>SVC: Seed, limits, actions 1…N
        SVC->>ENG: Generate armies and build 20 trees
        loop Every persisted action in sequence
            SVC->>ENG: apply(type, ranges)
        end
        SVC->>CACHE: Store reconstructed engine
        CACHE-->>SVC: Live engine
    end
    SVC-->>API: Current deterministic state
~~~

### 8.5 State ownership

| State | Authoritative owner | Persistence | Notes |
|---|---|---|---|
| Selected UI ranges | Browser store | No | Reset when a match is loaded |
| Visible soldier pages | Browser cache | No | Refetched after every action |
| Live arrays, trees, round, scores | Battle engine | Indirect | Cached in process; never serialized |
| Match configuration | Database match row | Yes | Seed and limits drive reconstruction |
| Canonical replay inputs | Database action rows | Yes | Type and two inclusive ranges |
| Historical outcome/commentary | Database action rows | Yes | Display only; not used to replay |
| Recent-list summary | Database match row | Yes | Denormalized round, status, scores, winner |

The supported MVP mutation model is one controlling browser per match. Concurrent writers and multi-instance coordination require per-match locking/idempotency and are outside the current scope.

---

## 9. API contract

### 9.1 Endpoint map

| Method | Endpoint | Purpose | Key inputs | Key outputs |
|---|---|---|---|---|
| GET | **/api/health** | Runtime health/config check | None | Status, app name, selected AI provider |
| POST | **/api/matches** | Create match | Team size, seed, max rounds, challenge interval | Match config, team summaries, current state |
| GET | **/api/matches** | List recent matches | Limit 1–100, default 20 | Newest-first match summaries |
| GET | **/api/matches/{id}** | Load match | Match ID | Current state and team totals |
| POST | **/api/matches/{id}/actions** | Resolve one action | Type, attack range, defense range | Result, commentary, resulting state |
| GET | **/api/matches/{id}/actions** | Read battle log | Match ID | Ordered action outcomes and commentary |
| GET | **/api/matches/{id}/query** | Run a range query | Team, attribute, operation, left, right | Value and optional winning element value |
| GET | **/api/matches/{id}/tree** | Export tree nodes | Team, attribute, operation, max depth | Breadth-first node snapshot |
| GET | **/api/matches/{id}/soldiers** | Read soldier page | Team, offset, limit | Indexed attack/health rows and total |

### 9.2 Error behavior

| Condition | Expected response |
|---|---|
| Unknown match | HTTP 404 with a JSON error message |
| Invalid domain range, wrong action, or finished match | HTTP 422 with a JSON error message |
| Invalid field type or declared bound | HTTP 422 validation detail |
| Commentary provider failure | Action remains committed; local fallback is attempted |
| Frontend cannot reach backend | Non-destructive error with retry/navigation path |

### 9.3 Serialization rule

Integers whose absolute value exceeds **2⁵³−1** must cross the API as decimal strings. This protects GCD/LCM and result payloads from silent JavaScript precision loss while preserving ordinary values as numbers.

---

## 10. Persistence model

~~~mermaid
erDiagram
    MATCH ||--o{ ACTION : contains
    MATCH {
        string id PK
        datetime created_at
        int team_size
        int seed
        int max_rounds
        int challenge_interval
        string status
        int winner
        int round
        int attacker
        int score_a
        int score_b
    }
    ACTION {
        int id PK
        string match_id FK
        int sequence
        string type
        int attack_left
        int attack_right
        int defense_left
        int defense_right
        json result
        text commentary
        datetime created_at
    }
~~~

### 10.1 Persistence rules

- Match IDs are 32-character UUID-derived strings.
- Action sequence is monotonic within a match.
- Replay reads configuration plus actions ordered by sequence.
- Stored result objects are audit/history material and are not replay inputs.
- Update paths are returned to the client but intentionally excluded from the persisted result to control log size.
- Match summary fields are updated with the same action commit.
- SQLite is the zero-configuration default; other SQLAlchemy URLs are deployment options.

---

## 11. Non-functional requirements

### 11.1 Performance and scale

| ID | Requirement |
|---|---|
| NFR-01 | Range queries and point updates remain O(log n); match construction remains O(n). |
| NFR-02 | A team size of 100,000 must complete creation and subsequent actions without contract changes or full-array API payloads. |
| NFR-03 | The arena requests at most 256 soldiers per team page; the API permits at most 1,024 per request. |
| NFR-04 | A visualizer request exports no more than depth 8, bounding the full snapshot to 511 nodes. |
| NFR-05 | External commentary latency is bounded by provider timeout and failure fallback; the engine outcome is committed before commentary is generated. |
| NFR-06 | Hosted deployments must account for the memory cost of up to 20 Python segment trees per live match and must evict inactive engines before supporting sustained multi-match traffic. |

### 11.2 Correctness and reliability

| ID | Requirement |
|---|---|
| NFR-07 | Every operation × attribute combination is verified against naive O(n) computation across randomized query/update sequences. |
| NFR-08 | Tests cover right-half point updates, tie-breaking, invalid ranges, deterministic generation, attacks, challenges, alternation, and termination. |
| NFR-09 | API tests cover each endpoint, validation failure, not-found behavior, big-integer serialization, and cache-drop rehydration. |
| NFR-10 | Commentary failure must never change an engine result, score, soldier stat, round, or winner. |
| NFR-11 | CI must run backend tests, frontend type/build checks, and the C++ reference build on pushes and pull requests. |

### 11.3 Usability and accessibility

| ID | Requirement |
|---|---|
| NFR-12 | A first-time user can identify the attacker, expected action, selected ranges, and score without documentation. |
| NFR-13 | Interactive controls use semantic elements, visible focus, readable labels, and keyboard access. |
| NFR-14 | Team, health, selection, challenge, and result states are not communicated by color alone. |
| NFR-15 | Tree nodes expose payload and range in text; index operations explain that payloads are soldier indices. |
| NFR-16 | Mobile layouts reflow without hiding core actions; large trees may scroll horizontally inside their own bounded region. |

### 11.4 Security, privacy, and operations

| ID | Requirement |
|---|---|
| NFR-17 | No credentials are required or stored in the default path; secrets enter only through environment variables. |
| NFR-18 | Every API input is validated and CORS origins are configurable. |
| NFR-19 | Logs contain operational context without leaking API keys or full model credentials. |
| NFR-20 | The application stores no personal data in MVP scope. |
| NFR-21 | Configuration is environment-driven with working local defaults. |
| NFR-22 | Database and provider failures produce actionable diagnostics and do not corrupt canonical match history. |

### 11.5 Maintainability

| ID | Requirement |
|---|---|
| NFR-23 | The engine remains pure and independently testable. |
| NFR-24 | One generic segment-tree implementation serves every operation strategy. |
| NFR-25 | Backend schemas and frontend types remain aligned when contracts change. |
| NFR-26 | Adding a commentary provider requires a provider implementation and factory registration, not battle-engine changes. |
| NFR-27 | Setup, configuration, test, troubleshooting, and deployment paths remain documented. |

---

## 12. Testing and quality strategy

| Layer | Coverage intent | Release gate |
|---|---|---|
| Operation strategies | Identities, merges, rightmost tie behavior, zero-aware LCM | Backend tests pass |
| Generic tree | Build, full/partial/single ranges, invalid inputs, left/right updates, snapshots, randomized cross-check | Backend tests pass |
| Battle engine | Seed determinism, expected action, attack math, rally, challenges, alternation, wipeout, score/tie finish | Backend tests pass |
| Match service | Persistence, ordered actions, cache behavior, replay equivalence | Backend tests pass |
| REST API | Success schemas, bounds, errors, all endpoints, pagination, safe integers | Backend tests pass |
| AI providers | Local determinism, selection, failure fallback, fake network transports | Backend tests pass without live providers |
| Frontend | Type safety, production bundle, route compilation | TypeScript and production build pass |
| User experience | Full match, challenge round, visualizer query, pagination, resume after restart | Manual smoke pass for MVP; automated E2E is next |
| Legacy C++ | Generated data, CMake configure/build | CI build passes |

### 12.1 Critical regression scenarios

1. Update a soldier in the right half and verify all five affected trees.
2. Run max/min queries with equal values and verify deterministic rightmost selection.
3. Resolve an attack with zero damage and verify rally, score, round, and log.
4. Resolve an attack that reduces total team health to zero and verify immediate winner.
5. Resolve the maximum round with equal scores and verify tie.
6. Reject an attack during a challenge round and a challenge during an ordinary round.
7. Produce an LCM larger than the JavaScript safe integer and verify exact string transport.
8. Drop the cached engine, reload the match, and compare arrays, trees, round, attacker, scores, status, and winner.
9. Fail the selected AI provider and verify local commentary plus unchanged canonical outcome.
10. Load a 100,000-soldier match without returning an unbounded grid or tree payload.

---

## 13. Deployment and runtime topology

~~~mermaid
flowchart LR
    B["Browser"] -->|"Static assets"| F["Vercel or Cloudflare Pages"]
    B -->|"HTTPS REST"| A["FastAPI service<br/>Render or equivalent"]
    A -->|"SQLAlchemy"| D["SQLite for local/demo<br/>or Neon Postgres"]
    A -. optional .-> R["OpenRouter free model"]
    A -. local development .-> O["Ollama"]
    A -->|"always available"| L["Local commentary fallback"]
~~~

### 13.1 Runtime profiles

| Profile | Frontend | Backend | Database | Commentary |
|---|---|---|---|---|
| Local default | Vite dev server | Uvicorn | SQLite | Local templates |
| Local model | Vite dev server | Uvicorn | SQLite | Ollama with local fallback |
| Split hosted demo | Static host | Render-style web service | Neon Postgres or ephemeral SQLite | Local or OpenRouter with fallback |

The detailed setup and free-tier constraints are maintained in [DEPLOYMENT.md](DEPLOYMENT.md).

---

## 14. Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Python engine diverges from reference semantics | Incorrect educational claims | Naive property tests, documented intentional rule changes, legacy reference |
| Large live matches consume significant memory | Hosted process exhaustion | Payload caps, single-instance scope, future TTL/LRU engine eviction, concurrency limits |
| Engine registry grows without eviction | Long-running server degradation | Add inactive-match eviction before sustained hosted traffic |
| Concurrent actions race on sequence/state | Duplicate or inconsistent actions | Single-controller MVP assumption; add per-match locking and idempotency before multiplayer |
| LCM becomes extremely large | Slow serialization or unreadable UI | Arbitrary-precision backend, safe string transport, visual truncation with exact value retained |
| AI provider times out or rate-limits | Slower action response | Bounded timeout, deterministic local fallback, AI excluded from rules |
| Database unavailable after engine mutation | Live memory could temporarily differ from persistence | Treat database commit failure as an operational error; production hardening should use transaction-aware recovery and request idempotency |
| Frontend visualizer implies live path highlighting | Product overclaim | Mark current state as partial and complete FR-17 before advertising propagation animation |
| SQLite or schema evolves without migrations | Deployment drift | Add Alembic before the first production schema change |
| External free tiers change limits | Demo instability | Keep fully local setup as the canonical supported path |

---

## 15. Delivery plan

The original seven-phase modernization sequence is preserved in [EXECUTION_PLAN.md](EXECUTION_PLAN.md). Product delivery is grouped here by outcome:

| Release | Outcome | Included work |
|---|---|---|
| R1 — Foundation | Trustworthy algorithm and reference baseline | Audit, repaired C++, generic tree, pure engine, randomized tests |
| R2 — Full-stack MVP | Complete playable and inspectable browser experience | REST API, persistence/replay, commentary providers, arena, visualizer, query playground, CI, deployment docs |
| R2.1 — Experience polish | Close known UX and robustness gaps | Update-path highlighting, accessibility pass, frontend tests, replay UX, retention/cache policy |
| R3 — Collaborative scale | Expand beyond a single controlling browser | WebSockets, per-match concurrency control, auth if required, Redis/multi-instance architecture |
| R4 — Advanced algorithms | Extend the educational surface | Lazy propagation, range updates, new battle mechanics, comparative complexity views |

---

## 16. Decision log

| Decision | Chosen direction | Reason |
|---|---|---|
| Primary backend language | Python | Typed FastAPI contracts, rapid testing, arbitrary-precision integers |
| Primary frontend stack | React 19, TypeScript, Vite, Tailwind, Zustand | Small typed client with fast development/build loop |
| Match authority | Backend engine | Prevents UI drift from rules |
| Persistence | Config + ordered actions, not tree snapshots | Deterministic replay keeps storage small and state explainable |
| Default database | SQLite | Zero setup and fully offline |
| Default commentary | Local templates | Reliable, deterministic, free |
| Multiplayer | Deferred | Would introduce identity, concurrency, synchronization, and operational scope unrelated to the MVP’s core learning goal |
| Legacy C++ | Preserve as reference | Retains project history and demonstrates modernization rather than replacement |
| Tie-breaking | Rightmost max/min index | Matches the current operation merge semantics and is deterministic |
| Challenge scoring | 50 points independently for GCD and LCM wins | Keeps both challenge operations load-bearing |

### 16.1 Open product decisions

These do not block the MVP but must be decided before the corresponding next release:

1. How long hosted matches should be retained and whether users may delete them.
2. Whether replay should reconstruct frames on demand or persist periodic snapshots.
3. What reference hardware and latency budgets should define published 100,000-soldier benchmarks.
4. Whether custom army import belongs in the learning product or a separate advanced mode.

---

## 17. Definition of done

The full-stack MVP is complete when:

1. A fresh clone can run locally without credentials by following the README in 10 minutes or less.
2. A user can create or resume a match, play ordinary and challenge rounds, and reach a deterministic winner or tie.
3. Every battle action is traceable to the segment-tree queries and updates that caused it.
4. A user can inspect any team × attribute × operation tree and run arbitrary valid range queries.
5. Soldier and tree payloads remain bounded for 100,000-soldier teams.
6. Match state survives a backend restart through seed-and-action replay.
7. Commentary failure cannot alter or lose a game action.
8. Backend tests, frontend type/build checks, and legacy C++ CI jobs pass.
9. API contracts, deployment, configuration, risks, and known deferred gaps are documented.
10. The PRD, README, implementation, and execution plan make no contradictory claims about delivered scope.

---

## 18. Requirement-to-system traceability

| Product capability | Frontend | API | Service/domain | Persistence |
|---|---|---|---|---|
| Create/resume match | Home, Arena | Create/list/get match | MatchService, BattleEngine | Match row, action rows |
| Ordinary attack | Arena, store | Post action | Sum/min/max queries, stat updates | Action outcome, match summary |
| Challenge | Arena, store | Post action | GCD/LCM queries, scoring | Action outcome, match summary |
| Battle history | Action log | Get actions | Ordered relationship | Action rows |
| Soldier inspection | Team panels | Get soldiers | Team arrays | Rebuilt from seed + replay |
| Tree inspection | Visualizer, TreeView | Get tree | SegmentTree snapshot | Not persisted |
| Query playground | Visualizer | Get query | Team query dispatch | Not persisted |
| Commentary | Action log | Post action response | Provider factory and fallback | Action commentary |
| Restart recovery | Loading states | Any match read | MatchService rehydrate | Config + ordered actions |
| Legacy reference | None | None | Independent C++ implementation | Generated input files |

---

**Document ownership:** Update this PRD whenever game rules, scope boundaries, public API contracts, persistence strategy, or release status changes. Implementation details that do not alter product behavior belong in code documentation rather than here.
