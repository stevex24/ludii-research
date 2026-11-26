import csv
import json
import time
from pathlib import Path
from timed_search import timed_search, child
from solve_3x3 import solve, legal_moves

root = Path("go/nogo")
start = time.perf_counter()

total = 0
proven = 0
correct = 0
winning_moves = 0
winning_positions = 0
errors = []

with (root/"exact_3x3.csv").open() as f:
    for r in csv.DictReader(f):
        b,w,t,y = (int(r[k]) for k in
            ("black_bits","white_bits",
             "turn","winning"))

        result = timed_search(b,w,t,3,1.0)
        total += 1

        if result["proven"]:
            proven += 1
            prediction = result["score"] > 0

            if prediction == bool(y):
                correct += 1
            else:
                errors.append(
                    ("wrong outcome",b,w,t)
                )
        else:
            errors.append(
                ("unproven",b,w,t)
            )

        options = list(legal_moves(b,w,t))
        m = result["move"]

        if options and m not in options:
            errors.append(
                ("illegal move",b,w,t)
            )

        if not options and m is not None:
            errors.append(
                ("terminal move",b,w,t)
            )

        if y:
            winning_positions += 1
            if m in options:
                opp_win,_ = solve(
                    *child(b,w,t,m)
                )
                if not opp_win:
                    winning_moves += 1
                else:
                    errors.append(
                        ("lost forced win",b,w,t)
                    )

        if total%500 == 0:
            print("Validated:",total,flush=True)

report = {
    "positions":total,
    "proven":proven,
    "correct_outcomes":correct,
    "winning_positions":winning_positions,
    "winning_moves_preserved":winning_moves,
    "errors":len(errors),
    "seconds":round(
        time.perf_counter()-start,3
    )
}

print(json.dumps(report,indent=2))

if errors:
    print("First errors:",errors[:10])
    print("VALIDATION FAILED")
else:
    print("ALL VALIDATION CHECKS PASSED")

(root/"timed_search_validation.json").write_text(
    json.dumps(report,indent=2)
)
