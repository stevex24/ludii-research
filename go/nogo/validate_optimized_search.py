import csv
import json
import time
from pathlib import Path
from optimized_search import optimized_search,child
from solve_3x3 import solve,legal_moves

root = Path("go/nogo")

with (root/"exact_3x3.csv").open() as f:
    rows = list(csv.DictReader(f))

evaluators = (
    "mobility",
    "learned_3x3",
    "learned_4x4_A",
    "learned_4x4_D"
)

results = []
overall_start = time.perf_counter()

for evaluator in evaluators:
    for use_tt in (False,True):
        start = time.perf_counter()
        proven = 0
        correct = 0
        preserved = 0
        wins = 0
        errors = 0
        nodes = 0
        hits = 0

        for r in rows:
            b,w,t,y = (
                int(r[k]) for k in
                ("black_bits","white_bits",
                 "turn","winning")
            )

            result = optimized_search(
                b,w,t,3,1.0,evaluator,use_tt
            )

            nodes += result["nodes"]
            hits += result["tt_hits"]

            if result["proven"]:
                proven += 1

            score = result["score"]

            outcome_ok = (
                result["proven"]
                and score is not None
                and (score>0)==bool(y)
            )

            if outcome_ok:
                correct += 1

            options = tuple(legal_moves(b,w,t))
            move = result["move"]

            legal = (
                move in options if options
                else move is None
            )

            preserved_ok = True

            if y:
                wins += 1
                preserved_ok = (
                    legal
                    and move is not None
                    and not solve(
                        *child(b,w,t,move)
                    )[0]
                )

                if preserved_ok:
                    preserved += 1

            if not (
                outcome_ok and legal and preserved_ok
            ):
                errors += 1

                if errors <= 5:
                    print("ERROR:",r,result)

        record = {
            "evaluator":evaluator,
            "use_tt":use_tt,
            "positions":len(rows),
            "proven":proven,
            "correct_outcomes":correct,
            "winning_positions":wins,
            "winning_moves_preserved":preserved,
            "errors":errors,
            "nodes":nodes,
            "tt_hits":hits,
            "seconds":round(
                time.perf_counter()-start,3
            )
        }

        results.append(record)
        print(json.dumps(record,indent=2),flush=True)

(root/"optimized_search_validation.json").write_text(
    json.dumps(results,indent=2)
)

total_errors = sum(r["errors"] for r in results)

print("\nTOTAL SEARCH TESTS:",
      len(rows)*len(results))
print("TOTAL ERRORS:",total_errors)
print("TOTAL SECONDS:",
      round(time.perf_counter()-overall_start,3))

assert total_errors == 0
print("ALL VALIDATION CHECKS PASSED")
