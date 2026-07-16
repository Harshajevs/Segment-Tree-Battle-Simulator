#!/usr/bin/env python3
"""Generate data/team1.txt and data/team2.txt for the legacy simulator.

Each line is "<attack> <health>" for one soldier. main.cpp expects exactly
100000 lines per file; pass --soldiers to override for quick experiments.
"""
import argparse
import random
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--soldiers", type=int, default=100_000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent.parent / "data")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    args.out.mkdir(parents=True, exist_ok=True)
    for name in ("team1.txt", "team2.txt"):
        path = args.out / name
        with path.open("w") as f:
            for _ in range(args.soldiers):
                f.write(f"{rng.randint(50, 200)} {rng.randint(500, 1500)}\n")
        print(f"wrote {args.soldiers} soldiers to {path}")


if __name__ == "__main__":
    main()
