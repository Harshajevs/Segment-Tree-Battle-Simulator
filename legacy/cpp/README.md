# Legacy C++ Implementation (Reference)

The original Sep–Nov 2024 course project, preserved as the reference
implementation for the segment-tree semantics now reimplemented in
`backend/app/engine/`. The go-forward application is the full-stack web app at
the repository root — see the top-level README.

Changes from the original sources (see `docs/AUDIT.md` for details):

1. Files moved into the `include/` / `src/` / `app/` layout that
   `CMakeLists.txt` always referenced (the flat layout never built).
2. Fixed wrong-child recursion in the four max/min index update functions
   (`2 * node` was used for both children; right child is `2 * node + 1`).
3. Fixed `SegmentTree::update()` passing root node `0` to the 1-indexed
   index-update trees.
4. Added `scripts/generate_data.py` for the previously missing
   `data/team1.txt` / `data/team2.txt` input files.

## Build & run

```bash
cd legacy/cpp
python3 scripts/generate_data.py            # creates data/ (100k soldiers/team)
mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build .
./SegmentTreeGame                           # interactive 100-round loop
```
