import json
import time
import argparse
from pathlib import Path
from functools import lru_cache
from features import extract, from_bits, legal_moves

ROOT = Path(__file__).resolve().parent

WEIGHTS = json.loads(
    (ROOT/"evaluator_3x3.json").read_text()
)["weights"]

class Timeout(Exception):
    pass

def child(b,w,t,m):
    if t == 0:
        return b|(1<<m),w,1
    return b,w|(1<<m),0

def timed_search(b,w,t,n,seconds,
                 evaluator="learned"):

    start = time.perf_counter()
    deadline = start+seconds
    nodes = 0

    @lru_cache(maxsize=100000)
    def moves(b,w,t):
        return tuple(sorted(
            legal_moves(from_bits(b,w,n),t+1,n)
        ))

    @lru_cache(maxsize=100000)
    def evaluate(b,w,t):
        if evaluator == "mobility":
            return (
                len(moves(b,w,t))-
                len(moves(b,w,1-t))
            )/(n*n)

        x = extract(b,w,t,n)
        return sum(
            a*v for a,v in zip(
                WEIGHTS,(1.0,)+x
            )
        )

    def check_time():
        if time.perf_counter() >= deadline:
            raise Timeout

    def search(b,w,t,d,alpha,beta):
        nonlocal nodes
        nodes += 1
        check_time()

        options = moves(b,w,t)

        if not options:
            return -1000.0

        if d == 0:
            value = evaluate(b,w,t)
            check_time()
            return value

        best = -float("inf")

        for m in options:
            value = -search(
                *child(b,w,t,m),
                d-1,-beta,-alpha
            )
            best = max(best,value)
            alpha = max(alpha,value)

            if alpha >= beta:
                break

        return best

    options = moves(b,w,t)

    if not options:
        return {
            "move":None,
            "depth":0,
            "score":-1000.0,
            "nodes":0,
            "elapsed":time.perf_counter()-start,
            "proven":True
        }

    best_move = options[0]
    best_score = None
    completed = 0

    for depth in range(
        1,n*n-bin(b|w).count("1")+1
    ):
        try:
            ordered = [best_move]+[
                m for m in options
                if m != best_move
            ]

            score = -float("inf")
            selected = best_move

            for m in ordered:
                check_time()

                value = -search(
                    *child(b,w,t,m),
                    depth-1,
                    -float("inf"),-score
                )

                if value > score:
                    score = value
                    selected = m

            check_time()

            best_move = selected
            best_score = score
            completed = depth

            if abs(score) >= 1000:
                break

        except Timeout:
            break

    return {
        "move":best_move,
        "depth":completed,
        "score":best_score,
        "nodes":nodes,
        "elapsed":time.perf_counter()-start,
        "proven":(
            best_score is not None
            and abs(best_score)>=1000
        )
    }

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--size",type=int,default=3)
    p.add_argument("--seconds",type=float,default=1)
    p.add_argument(
        "--evaluator",
        choices=["mobility","learned"],
        default="learned"
    )
    args = p.parse_args()

    result = timed_search(
        0,0,0,args.size,args.seconds,
        args.evaluator
    )

    print(json.dumps(result,indent=2))
