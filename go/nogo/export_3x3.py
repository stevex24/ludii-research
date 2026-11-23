#!/usr/bin/env python3
"""Export exact reachable 3x3 NoGo positions."""
import csv
from pathlib import Path
from solve_3x3 import solve, legal_moves

def main():
    solve(0, 0, 0)
    records = []
    for (black, white, turn), (winning, dtm) in solve.cache_info_and_items() if hasattr(solve, "cache_info_and_items") else []:
        records.append((black, white, turn, winning, dtm))

    # Traverse reachable positions explicitly; functools.lru_cache
    # does not expose its stored keys.
    seen = set()
    stack = [(0, 0, 0)]
    while stack:
        black, white, turn = stack.pop()
        state = (black, white, turn)
        if state in seen:
            continue
        seen.add(state)
        for move in legal_moves(black, white, turn):
            bit = 1 << move
            nb, nw = (black | bit, white) if turn == 0 else (black, white | bit)
            stack.append((nb, nw, 1-turn))

    for black, white, turn in sorted(seen):
        winning, dtm = solve(black, white, turn)
        records.append((black, white, turn, int(winning), dtm,
                        len(list(legal_moves(black, white, turn)))))

    assert len(records) == 3884, len(records)
    out = Path("go/nogo/exact_3x3.csv")
    with out.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["black_bits", "white_bits", "turn",
                         "winning", "dtm", "legal_moves"])
        writer.writerows(records)
    print(f"Exported {len(records)} exact states to {out}")
    print("Root:", records[0] if records[0][:3] == (0,0,0) else "included")

if __name__ == "__main__":
    main()
