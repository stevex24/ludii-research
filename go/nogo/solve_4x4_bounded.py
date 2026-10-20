#!/usr/bin/env python3
"""Bounded, exact minimax for standard NoGo on a 4x4 board.
Only reports a winner if the entire needed search has completed.
"""
import argparse
import json
import time
from functools import lru_cache
from pathlib import Path

N=4
NEIGHBORS=[]
for i in range(N*N):
    r,c=divmod(i,N)
    NEIGHBORS.append(tuple(rr*N+cc for rr,cc in ((r-1,c),(r+1,c),(r,c-1),(r,c+1)) if 0<=rr<N and 0<=cc<N))

class BudgetExceeded(Exception): pass

def group_has_liberty(board, start, visited):
    color=board[start]
    stack=[start]; visited.add(start)
    liberty=False
    while stack:
        p=stack.pop()
        for q in NEIGHBORS[p]:
            if board[q]==0: liberty=True
            elif board[q]==color and q not in visited:
                visited.add(q); stack.append(q)
    return liberty

def legal(board, at, player):
    if board[at]: return False
    b=board[:at]+(player,)+board[at+1:]
    # The resulting board must have at least one liberty for every group.
    visited=set()
    for i,v in enumerate(b):
        if v and i not in visited and not group_has_liberty(b,i,visited):
            return False
    return True

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--seconds',type=float,default=60)
    p.add_argument('--max-states',type=int,default=300000)
    args=p.parse_args()
    start=time.monotonic(); nodes=0; edges=0
    @lru_cache(maxsize=None)
    def solve(board,player):
        nonlocal nodes,edges
        nodes+=1
        if nodes%128==0 and (nodes>=args.max_states or time.monotonic()-start>=args.seconds):
            raise BudgetExceeded
        moves=[i for i,v in enumerate(board) if v==0 and legal(board,i,player)]
        edges+=len(moves)
        if not moves: return (False,0,None)
        best_win=None; best_loss=None
        for i in moves:
            child=board[:i]+(player,)+board[i+1:]
            opp_win, dtm, _=solve(child,3-player)
            if not opp_win:
                if best_win is None or dtm+1<best_win[0]: best_win=(dtm+1,i)
            elif best_loss is None or dtm+1>best_loss[0]: best_loss=(dtm+1,i)
        if best_win is not None: return (True,best_win[0],best_win[1])
        return (False,best_loss[0],best_loss[1])
    result={'game':'standard 4x4 NoGo','time_limit_seconds':args.seconds,'state_limit':args.max_states}
    try:
        win,dtm,move=solve((0,)*16,1)
        result.update(status='SOLVED',winner='Black' if win else 'White',optimal_plies=dtm,first_move=None if move is None else [move//4+1,move%4+1])
    except BudgetExceeded:
        result.update(status='INCOMPLETE',winner=None,optimal_plies=None,first_move=None)
    result.update(elapsed_seconds=round(time.monotonic()-start,2),expanded_states=nodes,cached_states=solve.cache_info().currsize,legal_edges_considered=edges)
    Path('reports').mkdir(exist_ok=True)
    Path('reports/day05_4x4_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    print('Saved reports/day05_4x4_results.json')
    if result['status']=='INCOMPLETE':
        print('No outcome claim: search stopped at its computational budget.')

if __name__=='__main__': main()
