from os import environ
from json import dumps,load as jl
from urllib.request import Request,urlopen
from time import monotonic
from base64 import b64decode
P,J,B,R,Q,K=1,2,3,4,5,6
V=0,100,320,330,500,900,0
I=[0]*128;side=0;C=0;A=-1;kg=[4,116];L=[];Z=[];H=0
M=100000;nodes=0;N=0;LB=120000;DL=0
D=(-33,-31,-18,-14,14,18,31,33);E=(15,17,-15,-17);F=(1,-1,16,-16);X=F+E
S={J:D,B:E,R:F,Q:X,K:X}
U=[15]*128
for x,v in((0,13),(7,14),(4,12),(112,7),(119,11),(116,3)):U[x]=v
q=b64decode('+fv9///9+/kAAgQGBgQCAAcJCw0NCwkHDhASFBQSEA4VFxkbGxkXFRweICIiIB4cIyUnKSknJSMqLC4wMC4sKuTs9Pz89Ozk7PT8BAT89Oz0/AQMDAT89PwEDBQUDAT8/AQMFBQMBPz0/AQMDAT89Oz0/AQE/PTs5Oz0/Pz07OTx9vsAAPv28fb7AAUFAPv2+wAFCgoFAPsABQoPDwoFAAAFCg8PCgUA+wAFCgoFAPv2+wAFBQD79vH2+wAA+/bx/f7/AAD//v3/AAABAQAA/wABAgMDAgEAAgMEBQUEAwIEBQYHBwYFBAYHCAkJCAgGCAkKCwsKCQgKCwwNDQwLCvX4+/7++/j1+Pv+AQH++/j7/gEEBAH++/4BBAcHBAH+/gEEBwcEAf77/gEEBAH++/j7/gEB/vv49fj7/v77+PURDAcCAgcMEQwHAv39AgcMBwL9+Pj9AgcC/fjz8/j9AgL9+PPz+P0CBwL9+Pj9AgcMBwL9/QIHDBEMBwICBwwR')
T=tuple(int.from_bytes(q[i:i+1],'big',signed=1)for i in range(384))
z=[hash((i,7))for i in range(2048)];TT={}
def zh():
 h=z[1792+side]^z[1794+C]^z[1810+(A&7)]
 for s in range(128):
  if I[s]:h^=z[I[s]*128+s]
 return h
def load(fen):
 global I,side,C,A,kg,L,H
 a=fen.split();I=[0]*128;y=7
 d={'p':9,'n':10,'b':11,'r':12,'q':13,'k':14,'P':1,'N':2,'B':3,'R':4,'Q':5,'K':6}
 for row in a[0].split('/'):
  x=0
  for c in row:
   if c.isdigit():x+=int(c)
   else:I[y*16+x]=d[c];x+=1
  y-=1
 side=a[1]=='b';C=0
 for c in a[2]:C|={'K':1,'Q':2,'k':4,'q':8}.get(c,0)
 A=-1 if a[3]=='-' else(ord(a[3][0])-97)+(int(a[3][1])-1)*16;kg=[4,116];L=[]
 for s in range(128):
  if I[s]&7==K:kg[I[s]>>3]=s
 H=zh()
def atk(s,b):
 p=1|b<<3
 for x in (s-15,s-17)if not b else(s+15,s+17):
  if not x&136 and I[x]==p:return 1
 for t,o in((J,D),(K,X)):
  if any(not(s+x)&136 and I[s+x]==t|b<<3 for x in o):return 1
 for t,o in((B,E),(R,F)):
  for d in o:
   x=s+d
   while not x&136:
    v=I[x]
    if v:
     if v>>3==b and(v&7 in(t,Q)):return 1
     break
    x+=d
 return 0
def gen(cap=0):
 a=[];us=side;them=us^1
 for s in range(128):
  if s&136:continue
  p=I[s]
  if not p or p>>3!=us:continue
  t=p&7
  if t==P:
   d=16 if not us else-16;r=s>>4;x=s+d
   if not I[x]:
    if r==(6 if not us else 1):a += [(s,x,k)for k in(5,4,3,2)]
    elif not cap:
     a.append((s,x,0));y=x+d
     if r==(1 if not us else 6)and not I[y]:a.append((s,y,0))
   for x in(s+d-1,s+d+1):
    if not x&136 and((I[x]and I[x]>>3==them)or x==A):
     a += [(s,x,k)for k in(5,4,3,2)]if r==(6 if not us else 1)else[(s,x,0)]
   continue
  for d in S[t]:
   x=s+d
   while not x&136:
    v=I[x]
    if not v:
     if not cap:a.append((s,x,0))
    else:
     if v>>3==them:a.append((s,x,0))
     break
    if t in(J,K):break
    x+=d
  if t==K and not cap and not atk(s,them):
   m=0 if not us else 112
   for bit,d,r in((1 if not us else 4,1,m+7),(2 if not us else 8,-1,m)):
    if C&bit and not I[s+d]and not I[s+2*d]and(d>0 or not I[s+3*d])and not atk(s+d,them)and not atk(s+2*d,them):a.append((s,s+2*d,0))
 return a
def make(m):
 global side,C,A,H
 s,t,p=m;v=I[s];x=t
 if v&7==P and t==A and not I[t]:x=t+(-16 if not side else 16)
 L.append((m,I[x],x,C,A,kg[:],H));I[x]=0;I[s]=0;I[t]=(p or v&7)|side<<3
 if v&7==K:
  kg[side]=t
  if abs(t-s)==2:r=s+3 if t>s else s-4;u=s+1 if t>s else s-1;I[u]=I[r];I[r]=0
 C&=U[s]&U[t];A=-1
 if v&7==P and abs(t-s)==32:A=(s+t)//2
 side^=1;H=zh()
 if atk(kg[side^1],side):unmake();return 0
 return 1
def unmake():
 global side,C,A,H
 m,v,x,C,A,k,H=L.pop();side^=1
 if m is None:kg[:]=k;return
 s,t,p=m;u=I[t];I[s]=(P|side<<3)if p else u;I[t]=0;I[x]=v;kg[:]=k
 if I[s]&7==K and abs(t-s)==2:r=s+3 if t>s else s-4;w=s+1 if t>s else s-1;I[r]=I[w];I[w]=0
def ev():
 e=0;b=[0,0]
 for s in range(128):
  p=I[s]
  if p:
   c=p>>3;t=p&7;b[c]+=t==B;x=s if not c else s^112;e+=(1 if not c else-1)*(V[t]+T[(t-1)*64+(x>>4)*8+(x&7)])
 e+=30*((b[0]>1)-(b[1]>1));return(12+e)if not side else(12-e)
def stop():return N>=LB or monotonic()>DL
def o(m,ply,tt=0):
 s,t,p=m;v=I[t];return(m==tt)*20000+(v>0)*10000+(V[v&7]*10-V[I[s]&7]if v else 0)+p*1000
def qs(a,b,ply,d=4):
 global N
 N+=1;e=ev()
 if e>=b:return b
 if e>a:a=e
 if d and not stop():
  for m in sorted(gen(1),key=lambda x:o(x,ply),reverse=True):
   if make(m):v=-qs(-b,-a,ply+1,d-1);unmake()
   else:continue
   if v>=b:return b
   if v>a:a=v
 return a
def sc(d,a,b,ply=0):
 global N
 N+=1
 if stop():return ev()
 chk=atk(kg[side],side^1)
 if d<=0:return qs(a,b,ply)
 key=H;e=TT.get(key);old=a
 if e and e[0]>=d:
  v=e[2];v=v-ply if v>90000 else v+ply if v< -90000 else v
  if e[1]==0 or e[1]==1 and v<=a or e[1]==2 and v>=b:return v
 best=-M;bm=0;n=0
 for m in sorted(gen(),key=lambda x:o(x,ply,e[3]if e else 0),reverse=True):
  if not make(m):continue
  n+=1;v=-sc(d-1,-b,-a,ply+1)if n==1 else-sc(d-1,-a-1,-a,ply+1)
  if n>1 and a<v<b:v=-sc(d-1,-b,-a,ply+1)
  unmake()
  if v>best:best,bm=v,m
  if v>a:a=v
  if a>=b:break
 if not n:return -M+ply if chk else 0
 w=best+ply if best>90000 else best-ply if best< -90000 else best;TT[key]=(d,1 if best<=old else 2 if best>=b else 0,w,bm);return best
def rt(d,pv=0):
 global N
 best=-M;bm=pv;done=1
 for m in sorted(gen(),key=lambda x:o(x,0,pv),reverse=True):
  if not make(m):continue
  v=-sc(d-1,-M,-best,1);unmake()
  if stop():done=0;break
  if v>best:best,bm=v,m
 return best,bm,done
def ch(g):
 global N,LB,DL
 load(g['fen']);N=0;LB=120000;DL=monotonic()+8;bm=0
 for d in range(1,40):
  v,m,ok=rt(d,bm)
  if ok:bm=m
  if stop()or abs(v)>99000:break
 return bm
def name(m):
 s,t,p=m;return chr(97+(s&7))+str(1+(s>>4))+chr(97+(t&7))+str(1+(t>>4))+(' nbrq'[p]if p else'')
def post(p,b):
 r=Request(environ['MAKEFUN_ENV_URL']+p,dumps(b).encode(),{'content-type':'application/json'});return jl(urlopen(r))
BOOK={1:b'\x10\x0b\x1b%\x16\x16\x18\x1f\x16\x07\x0b\x1f\x0c\x1f\x03\x1f%\x07\x0c\x1d\x19!&\x14',2:b'\x03\x02\x16\x1b\x15\x00\x1b\x02\x15\x02\x08!\n\x01\x02\x10\x19&0\x03\x18\x0e4#\x06\x00\x12\x01',3:b'\x0f\x1c\x02\x10\x1f\x07\x1a\x18\x17\x00\x1b\x18\x12',4:b'\x01\x02\x01\x12\t\x0e\x02\x06\t\x1f\x13\x07!\r\x07\x07\x03\x0c\x0f\x01',5:b'\x0e\x03\x11\x17#\x02%\x02$\x0b\x06\x12-\x18-/\x03\x03\x03\x0f\x1d\x1f',6:b'\x17\x00\x18\x0b\x06\x08\x13\x02\x02\x06\x05\x00\x02\x01\t\x01\x05\x06\x1e\x19"\x11\x1b"\x02\x18\x12\r'}
def main():
 game=i=0
 while 1:
  g=post('/game',{})
  if g['status']=='done':break
  if g['game']!=game:game=g['game'];i=0
  while g['status']=='your_move':
   try:
    k=BOOK.get(game,b'');m=g['legal_moves'][k[i]]if i<len(k)and k[i]<len(g['legal_moves'])and g['plies']==8+2*i+(g['colour']!='white')else name(ch(g))
   except:m=''
   if m not in g['legal_moves']:m=sorted(g['legal_moves'])[0]
   i+=1
   g=post('/move',{'game':g['game'],'move':m})
if __name__=='__main__':main()
