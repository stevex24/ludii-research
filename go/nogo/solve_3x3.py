#!/usr/bin/env python3
"""Exact 3x3 NoGo solver. Black moves first; no captures, suicide, or passes."""
from functools import lru_cache
from collections import Counter
N=3
FULL=(1<<(N*N))-1
ADJ=[]
for p in range(N*N):
 r,c=divmod(p,N)
 ADJ.append(tuple(rr*N+cc for rr,cc in ((r-1,c),(r+1,c),(r,c-1),(r,c+1)) if 0<=rr<N and 0<=cc<N))

def groups_have_liberties(stones,occupied):
 remaining=stones
 while remaining:
  start=remaining & -remaining
  todo=start
  group=0
  while todo:
   bit=todo & -todo;todo-=bit
   if group & bit:continue
   group|=bit
   i=bit.bit_length()-1
   for j in ADJ[i]:
    b=1<<j
    if stones & b and not(group & b):todo|=b
  remaining &= ~group
  for i in range(9):
   if group>>i & 1:
    if any(not(occupied>>j & 1) for j in ADJ[i]):break
  else:return False
 return True

def legal_moves(black,white,turn):
 occupied=black|white
 for i in range(9):
  bit=1<<i
  if occupied&bit:continue
  b,w=(black|bit,white) if turn==0 else (black,white|bit)
  newocc=b|w
  if groups_have_liberties(b,newocc) and groups_have_liberties(w,newocc):yield i

@lru_cache(None)
def solve(black,white,turn):
 """Return (side-to-move can force win, plies under fastest win/slowest loss)."""
 moves=list(legal_moves(black,white,turn))
 if not moves:return False,0
 wins=[];losses=[]
 for i in moves:
  bit=1<<i
  b,w=(black|bit,white) if turn==0 else (black,white|bit)
  opponent_wins,dist=solve(b,w,1-turn)
  (losses if opponent_wins else wins).append((dist+1,i))
 if wins:return True,min(wins)[0]
 return False,max(losses)[0]

def optimal_line():
 b=w=0;turn=0;line=[]
 while True:
  moves=list(legal_moves(b,w,turn))
  if not moves:break
  winning,dt=solve(b,w,turn)
  options=[]
  for i in moves:
   bit=1<<i
   nb,nw=(b|bit,w) if turn==0 else (b,w|bit)
   oppwins,dist=solve(nb,nw,1-turn)
   if winning and not oppwins:options.append((dist+1,i,nb,nw))
   if not winning and oppwins:options.append((-dist-1,i,nb,nw))
  if winning:_,i,b,w=min(options)
  else:_,i,b,w=min(options)
  line.append((turn,i,b,w))
  turn=1-turn
 return line,turn

def board(b,w):
 return '\n'.join(' '.join('B' if b>>(r*3+c)&1 else 'W' if w>>(r*3+c)&1 else '.' for c in range(3)) for r in range(3))

def main():
 result,dt=solve(0,0,0)
 line,loser=optimal_line()
 print('3x3 NoGo — exhaustive minimax (no symmetry reduction)')
 print('Root result:', 'BLACK WINS' if result else 'BLACK LOSES')
 print('Optimal game length (plies):',dt)
 print('Cached reachable states:',solve.cache_info().currsize)
 print('Optimal first moves (row,col; 1-based):')
 for i in legal_moves(0,0,0):
  oppwins,d=solve(1<<i,0,1)
  if oppwins != result:print(' ',(i//3+1,i%3+1),'win' if not oppwins else 'loss','plies',d+1)
 print('One optimal game:')
 for n,(turn,i,b,w) in enumerate(line,1):
  print(f'Ply {n}: {"Black" if turn==0 else "White"} ({i//3+1},{i%3+1})')
  print(board(b,w))
 print('Player unable to move:', 'Black' if loser==0 else 'White')
 print('Winner:', 'White' if loser==0 else 'Black')
 assert len(line)==dt
 assert (loser==1)==result

if __name__=='__main__':main()
