import re,json, pathlib
ROOT=pathlib.Path(__file__).parent
START='6N1/5KR1/2n5/8/8/8/2n5/1k6 w - - 0 1'
def load(fen):
 b={}; ranks=fen.split()[0].split('/')
 for y,row in enumerate(ranks):
  x=0
  for ch in row:
   if ch.isdigit(): x+=int(ch)
   else: b[(x,7-y)]=ch;x+=1
 return b
def name(pos):return 'abcdefgh'[pos[0]]+str(pos[1]+1)
def pseudo(b,src,dst,p):
 x,y=src;X,Y=dst;dx=X-x;dy=Y-y
 if not (0<=X<8 and 0<=Y<8) or src==dst:return False
 if dst in b and b[dst].isupper()==p.isupper():return False
 t=p.upper()
 if t=='K':return max(abs(dx),abs(dy))==1
 if t=='N':return (abs(dx),abs(dy)) in ((1,2),(2,1))
 if t in ('R','B','Q'):
  if t=='R' and dx!=0 and dy!=0:return False
  if t=='B' and abs(dx)!=abs(dy):return False
  if t=='Q' and not (dx==0 or dy==0 or abs(dx)==abs(dy)):return False
  steps=max(abs(dx),abs(dy)); sx=(dx>0)-(dx<0);sy=(dy>0)-(dy<0)
  return all((x+i*sx,y+i*sy) not in b for i in range(1,steps))
 return False
def attacked(b,sq,by_white):return any(p.isupper()==by_white and pseudo(b,s,sq,p) for s,p in b.items())
def legal(b,s,d,p):
 if not pseudo(b,s,d,p):return False
 bb=b.copy();bb[d]=bb.pop(s)
 k=next((q for q,v in bb.items() if v==('K' if p.isupper() else 'k')),None)
 return k is not None and not attacked(bb,k,not p.isupper())
def parse_san(b,san,white):
 clean=san.rstrip('+#?!');m=re.fullmatch(r'([KQRBN])?([a-h])?([1-8])?(x)?([a-h][1-8])',clean)
 if not m:raise ValueError('bad SAN '+san)
 typ,file,rank,cap,dest=m.groups();typ=typ or 'P';p=typ if white else typ.lower();d=('abcdefgh'.index(dest[0]),int(dest[1])-1)
 options=[s for s,v in b.items() if v==p and (file is None or name(s)[0]==file) and (rank is None or name(s)[1]==rank) and legal(b,s,d,p)]
 if len(options)!=1:raise ValueError(f'{san} ambiguous/illegal: {options}, side={white}')
 s=options[0]
 if bool(cap)!=(d in b):raise ValueError(f'capture mismatch {san}')
 nb=b.copy();nb[d]=nb.pop(s)
 return nb, name(s)+name(d)
def fenboard(b,turn):
 rows=[]
 for y in range(7,-1,-1):
  run=0;row=''
  for x in range(8):
   p=b.get((x,y))
   if p:
    if run:row+=str(run);run=0
    row+=p
   else:run+=1
  if run:row+=str(run)
  rows.append(row)
 return '/'.join(rows)+' '+('w' if turn else 'b')+' - - 0 1'
s=ROOT.joinpath('source_moves.txt').read_text(); tokens=re.sub(r'\b\d+\.','',s).split()
b=load(START);frames=[{'fen':fenboard(b,True),'san':'Start','uci':'','move':0}]
for i,san in enumerate(tokens):
 b,uci=parse_san(b,san,i%2==0)
 frames.append({'fen':fenboard(b,(i+1)%2==0),'san':san,'uci':uci,'move':i+1})
print('Validated legal moves:',len(tokens),'final',fenboard(b,False),'last',tokens[-1]);assert len(tokens)==523
assert tokens[-1]=='Rh2#'
assert attacked(b,next(s for s,p in b.items() if p=='k'),True)
ROOT.joinpath('positions.json').write_text(json.dumps({'source':'https://en.chessbase.com/post/just-one-of-17-823-400-766-positions-2','title':'Conrady 262-move KRN vs KNN tablebase line','start_fen':START,'frames':frames},separators=(',',':')))
