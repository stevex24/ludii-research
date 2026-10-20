#!/usr/bin/env python3
"""Independent tuple/DFS NoGo rules and minimax cross-check against Day 4 bitboard solver."""
import sys
from pathlib import Path
from functools import lru_cache
sys.path.insert(0,str(Path(__file__).resolve().parent))
import solve_3x3 as original

NEIGHBORS = tuple(tuple(y for y in range(9) if abs(y//3-x//3)+abs(y%3-x%3)==1) for x in range(9))

def legal_reference(position, player):
    # position: 9-element tuple, 0 empty, 1 black, 2 white
    for location in range(9):
        if position[location]:
            continue
        after=list(position)
        after[location]=player
        visited=set()
        valid=True
        for start in range(9):
            if not after[start] or start in visited:
                continue
            stack=[start]
            visited.add(start)
            liberty=False
            while stack:
                x=stack.pop()
                for y in NEIGHBORS[x]:
                    if after[y]==0:
                        liberty=True
                    elif after[y]==after[x] and y not in visited:
                        visited.add(y)
                        stack.append(y)
            if not liberty:
                valid=False
                break
        if valid:
            yield location

@lru_cache(None)
def reference_minimax(position, player):
    moves=list(legal_reference(position,player))
    if not moves:
        return False,0
    next_results=[]
    for location in moves:
        after=list(position)
        after[location]=player
        wins,dt=reference_minimax(tuple(after),3-player)
        next_results.append((wins,dt))
    wins=[dt+1 for opponent_wins,dt in next_results if not opponent_wins]
    if wins:
        return True,min(wins)
    return False,max(dt+1 for _,dt in next_results)

def as_bitboards(position):
    black=sum(1<<i for i,v in enumerate(position) if v==1)
    white=sum(1<<i for i,v in enumerate(position) if v==2)
    return black,white

def main():
    start=(0,)*9
    result=reference_minimax(start,1)
    states=reference_minimax.cache_info().currsize
    print('Independent 3x3 NoGo validation')
    print('Reference method: tuple board, graph flood fill, independent recursive minimax')
    print('Reference initial outcome:', 'BLACK WINS' if result[0] else 'BLACK LOSES')
    print('Reference initial DTM:',result[1])
    print('Reference reachable states:',states)
    # Enumerate the entire reachable game graph and compare both implementations
    seen=set()
    stack=[(start,1)]
    transitions=0
    while stack:
        pos,player=stack.pop()
        if (pos,player) in seen:
            continue
        seen.add((pos,player))
        black,white=as_bitboards(pos)
        actual=set(original.legal_moves(black,white,player-1))
        expected=set(legal_reference(pos,player))
        assert actual==expected,(pos,player,actual,expected)
        ref=reference_minimax(pos,player)
        got=original.solve(black,white,player-1)
        assert ref==got,(pos,player,ref,got)
        transitions+=len(expected)
        for i in expected:
            after=list(pos)
            after[i]=player
            stack.append((tuple(after),3-player))
    assert len(seen)==states
    assert result==(True,7),result
    assert len(seen)==3884,len(seen)
    print('PASS: identical legal moves and minimax W/L + DTM in',len(seen),'reachable states')
    print('Checked legal transitions:',transitions)
    print('Winning first moves:',sum(not reference_minimax(tuple(1 if j==i else 0 for j in range(9)),2)[0] for i in range(9)),'of 9')
    print('PASS: independent reference agrees with Day 4 solver')
    print('Ludii comparison status: rules inspected; Ludii execution NOT independently tested')

if __name__=='__main__':main()
