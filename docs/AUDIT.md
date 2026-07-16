# Repository Audit — Segment-Tree-Battle-Simulator

_Audit date: July 2026. Baseline: last commit on `main` before the modernization branch._

## 1. What the project is

A C++17 console application that demonstrates segment trees applied to a
turn-based battle game. Two teams of 100,000 soldiers (each with `attack` and
`health`) are loaded from text files. Ten parallel segment trees per team
answer range queries — sum, max index, min index, GCD, LCM — over both
attributes, and an interactive loop lets a player run 100 rounds of attacks,
with GCD/LCM "surprise" challenges every 10th round.

## 2. Existing architecture

| Aspect | State |
|---|---|
| Language / build | C++17, CMake ≥ 3.15 |
| Structure | Flat directory: 5 `.cpp`, 3 `.h`, `CMakeLists.txt`, `README.md` |
| Interface | Interactive stdin/stdout console loop |
| Persistence | None (reads `data/team1.txt` / `data/team2.txt` at startup) |
| Tests | None |
| CI/CD | None |
| Frontend | None |
| Backend / API | None |
| Auth | None |
| AI integrations | None |

### Data structure design

`SegmentTree` (SegmentTree.h) owns ten independent trees, one per
(operation × attribute) combination:

- `sumAttackTree`, `sumHealthTree` — range sum
- `maxAttackTreeIndex`, `maxHealthTreeIndex` — index of range maximum
- `minAttackTreeIndex`, `minHealthTreeIndex` — index of range minimum
- `gcdAttackTree`, `gcdHealthTree` — range GCD
- `lcmAttackTree`, `lcmHealthTree` — range LCM

Each tree has hand-written `build` / `query` / `update` recursion
(BuildOperations.cpp, QueryOperations.cpp, UpdateOperations.cpp), 1-indexed,
4n storage. All queries are O(log n); point updates propagate to all ten trees.

## 3. Defects found (verified in source)

1. **Build is broken.** `CMakeLists.txt` compiles `src/SegmentTree.cpp`,
   `src/TreeOperations/*.cpp`, `app/main.cpp` and includes `include/`, but every
   file sits in the repository root. `cmake --build` cannot succeed on a fresh
   clone.
2. **Missing input data.** `main.cpp` hard-requires `data/team1.txt` and
   `data/team2.txt` (100,000 lines each); neither file nor a generator is in
   the repo, so the binary exits with an error even if built.
3. **Wrong-child recursion in index updates.** In `UpdateOperations.cpp`, all
   four of `updateMaxAttackIndex`, `updateMaxHealthIndex`,
   `updateMinAttackIndex`, `updateMinHealthIndex` recurse into `2 * node` in
   **both** the `if` and `else` branches — the right child (`2 * node + 1`) is
   never descended into, corrupting max/min answers after any update to the
   right half.
4. **Wrong root node for index updates.** `SegmentTree::update()`
   (SegmentTree.cpp) calls the four index-update helpers with `node = 0`, but
   the trees are 1-indexed (root = 1). Node 0 is written while queries read
   from node 1.
5. **Scoring bug.** `main.cpp:79-80` adds the *same* value
   (`sumAttack1 - sumHealth2`) to both `teamA_score` and `teamB_score`, so the
   base game can only ever end in a tie; only GCD bonuses differentiate teams.
   Team B never actually attacks, contradicting the README's
   "counterattack" flow.
6. **Integer overflow.** Sum trees are `vector<int>`; 100,000 soldiers with
   4-digit attack values can exceed `INT_MAX` at the root. LCM trees store
   `long long` but `LCM` grows multiplicatively and overflows silently for
   almost any non-trivial range.
7. **Dead code.** `TreeOperations.h` (a full template-based operation library,
   0-indexed children — incompatible with the 1-indexed implementation) and
   `Utils.h` are never included by any translation unit.
8. **Misleading update semantics.** `main.cpp` comments say "Increase attack" /
   "Increase health" but `update()` *sets* attack to 100 and health to 200,
   usually weakening the soldier.

## 4. Technical debt & design issues

- **Massive duplication:** ten near-identical build/query/update triplets that
  differ only in merge function and attribute accessor (~450 lines that could
  be one generic tree parameterised by an operation).
- **No separation of concerns:** game rules, I/O, and validation all live in
  `main()`.
- **No validation layer:** ranges are clamped but never checked `l ≤ r`; a
  reversed range silently returns identity values.
- **No error handling strategy**, no logging, no configuration (team size and
  round count are compile-time constants).
- **No tests** for a codebase whose entire value proposition is algorithmic
  correctness — and defects 3–5 show tests would have caught real bugs.
- **README drift:** documents a directory layout, input format, and features
  (batch updates, atomic propagation, overflow checks) that do not exist in
  the code.

## 5. Security & operational concerns

Minimal surface today (no network, no secrets), but also: unvalidated file
input parsed with `>>` (silent zero-fill on malformed data), and unbounded
stdin reads. Nothing is deployable or demonstrable without a terminal.

## 6. What is worth preserving

- The core concept: one dataset, five range operations, driving game logic —
  a genuinely good segment-tree showcase.
- The game rules: range-sum damage (attack vs. health), alternating
  attack/defence phases, every-10th-round GCD/LCM challenges with +50 bonus.
- O(log n) query / point-update semantics and the 4n array representation.
- The original C++ source, as a reference implementation (moved to
  `legacy/cpp/` with its build fixed).
