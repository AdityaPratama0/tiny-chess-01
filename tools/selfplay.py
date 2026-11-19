#!/usr/bin/env python3
"""Fast engine-vs-depth-2 practice runner. Run from any directory."""
import argparse,pathlib,sys,time
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import engine as E

def legal_moves():
    out=[]
    for m in E.gen():
        if E.make(m):out.append(m);E.unmake()
    return out

def reference(depth,alpha=-E.M,beta=E.M):
    if depth==0:return E.ev(),None
    best=-E.M;bm=None;n=0
    for m in E.gen():
        if not E.make(m):continue
        n+=1;v=-reference(depth-1,-beta,-alpha)[0];E.unmake()
        if v>best:best,bm=v,m
        if v>alpha:alpha=v
        if alpha>=beta:break
    if not n:return (-E.M if E.atk(E.kg[E.side],E.side^1) else 0),None
    return best,bm

def tested_move(nodes):
    E.N=0;E.LB=nodes;E.DL=time.monotonic()+1.5;bm=None
    for depth in range(1,9):
        _,m,done=E.rt(depth,bm)
        if done:bm=m
        if E.N>=E.LB or time.monotonic()>=E.DL:break
    return bm

def play(fen,engine_colour,nodes,maxplies):
    E.load(fen);seen={}
    for ply in range(1,maxplies+1):
        moves=legal_moves()
        if not moves:
            if E.atk(E.kg[E.side],E.side^1):return (engine_colour if E.side!=engine_colour else engine_colour^1),ply-1
            return -1,ply-1
        m=tested_move(nodes) if E.side==engine_colour else reference(2)[1]
        if m is None or not E.make(m):raise RuntimeError('search returned an illegal move')
        key=(tuple(E.I),E.side,E.B,E.A);seen[key]=seen.get(key,0)+1
        if seen[key]>=3:return -1,ply
    # Explicit practice adjudication avoids a slow tail in completely won endings.
    score=E.ev()*(1 if E.side==engine_colour else -1)
    return (engine_colour if score>300 else engine_colour^1 if score < -300 else -1),maxplies

def main():
    p=argparse.ArgumentParser();p.add_argument('games',nargs='?',type=int,default=6)
    p.add_argument('--positions',type=pathlib.Path,default=ROOT/'tools/practice_positions.txt')
    p.add_argument('--nodes',type=int,default=12000);p.add_argument('--max-plies',type=int,default=120)
    a=p.parse_args();fens=[x.strip() for x in a.positions.read_text().splitlines() if x.strip() and not x.startswith('#')]
    w=l=d=0;plies=[]
    for i in range(a.games):
        colour=i&1;winner,n=play(fens[i%len(fens)],colour,a.nodes,a.max_plies);plies.append(n)
        result='D' if winner<0 else 'W' if winner==colour else 'L'
        w+=result=='W';l+=result=='L';d+=result=='D';print(f'{i+1}: {result} ply {n}')
    print(f'W/L/D {w}/{l}/{d}; plies '+','.join(map(str,plies)))
    raise SystemExit(0 if w==a.games and max(plies)<=a.max_plies else 1)
if __name__=='__main__':main()
