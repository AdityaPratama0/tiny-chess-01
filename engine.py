o=tuple
K=len
E=ord
P=range
import os,json as Z,urllib.request,time as a,zlib,base64 as p
F,q=0,1
O,T,V,W,b,R=1,2,3,4,5,6
c=[0,100,320,330,500,900,0]
d=33,31,18,14,-14,-18,-31,-33
X=1,-1,16,-16,15,17,-15,-17
e=15,17,-15,-17
f=1,-1,16,-16
g,h,i,j=1,2,4,8
U=[15]*128
for(C,r)in((0,13),(7,14),(4,12),(112,7),(119,11),(116,3)):U[C]=r
s='c-l3PNsHTN9LDv3wOiKmY9vdRtlgHzw&Z1O*|Q`Qd-gb)l4&|iCS)KxNedY!A%r1q=p0HYDRlV)g@#ai%RK}NEtEnJJ@nFZKSNJFbfC?1f3_b%{HLGb1v-8U&*2|f(FLi$cmjtriER}dEi=q=k~hPm*6p$E6vHeTtB_<)=VJ4JGw~aG4a?V$e+1_b_zJeZgpJlyDY*7zasuDO3HloLa2Vg8d=AyL%=y-A+>kSDYH>K@&D}F-sM@vPq5g0j3~SjO_Z^(?UY6vZAC=EMu3qydJD1jOO-Qy7-<nJ$Qn0N4im7pg>$;UeRpVTrkQz&9OxyLcu~{E|FuL=Jy0|kKJ$m{rd<OkJKJIUX`^SD;m-?MGIa%)+po+!pO4kb*f*<dC35JsJ1=PwY^riE?Au(@0-rL!4Z}P}Hn*FF8NXq=-!BL)j9)u*qJv>FS3~f_7$y1fWs$8NJmqrj_&FP-K`6;w~=fN^%%|jx}?1eepp}eG+HiN{-7rOTPb;vib?v8KUcJu1)f|DajezxtYinC#Us0=%mcVPcQf1)?&1$u>^qhHbA=neb=Kb(F#y#Ml)?5JZENG=R5l@>*r0ZtMS!Gmlmie?d%_%7w)h4S!h{_)SymAfSFw(qtRO$A)r3YauaOG*?8{)``TQAUHS(Mj`iGR2cgwmWw_bDGi3XLeneMI5wcRx;=^Yf~}-WRc)#)l@4QLkWx(OB#(0`m~r49Xk?%!%m*zjK>}ySX$LJO{Gw>tP;&Aj3h|~j^=5Ou@HrTVhRe!3$o6ht``m269j_7Sf???0AJ=3oTh_8tW5{gqxT=poFS5;dgEX%R++T3e{|_+Bbtp57FXVDdAVCuL#@!v7CbLoKQ|sWxA}9));F*kMY_ucMpy~Mi>;Ctw%qCcJxfkIgZ@&ViP%PG&{FjpU23#^3FkUzRX9Glw_MkUc6<9@W#oQ('
J=zlib.decompress(p.b85decode(s))
Q=[]
C=0
while C<K(J):
	D=J[C];C+=1
	if D>127:D=D%128+128*J[C];C+=1
	Q.append(D>>1^-(D&1))
Q=o(Q)
t=82,337,365,477,1025,0
u=94,281,297,512,936,0
v={'p':9,'n':10,'b':11,'r':12,'q':13,'k':14,'P':1,'N':2,'B':3,'R':4,'Q':5,'K':6}
w={'K':g,'Q':h,'k':i,'q':j}
I=[0]*128
side=F
B=0
A=-1
kg=[4,116]
L=[]
def load(fen):
	global I,side,B,A,kg,L;C=fen.split();G=[0]*128;M=7
	for O in C[0].split('/'):
		H=0
		for D in O:
			if'1'<=D<='9':H+=E(D)-48
			else:G[(M<<4)+H]=v[D];H+=1
		M-=1
	I=G;side=F if C[1]=='w'else q;B=0
	if K(C)>2 and C[2]!='-':
		for D in C[2]:B|=w.get(D,0)
	A=-1
	if K(C)>3 and C[3]!='-':A=(E(C[3][1])-49)*16+(E(C[3][0])-97)
	kg=[4,116];L=[]
	for N in P(128):
		J=G[N]
		if not J:continue
		Q=J&7
		if Q==R:kg[J>>3]=N
def atk(sq,by):
	B=sq;D=I
	if by==F:
		if not B-15&136 and D[B-15]==1:return True
		if not B-17&136 and D[B-17]==1:return True
		E=0
	else:
		if not B+15&136 and D[B+15]==9:return True
		if not B+17&136 and D[B+17]==9:return True
		E=8
	for C in d:
		A=B+C
		if not A&136 and D[A]==2+E:return True
	for C in X:
		A=B+C
		if not A&136 and D[A]==6+E:return True
	for C in e:
		A=B+C
		while not A&136:
			G=D[A]
			if G:
				if G==3+E or G==5+E:return True
				break
			A+=C
	for C in f:
		A=B+C
		while not A&136:
			G=D[A]
			if G:
				if G==4+E or G==5+E:return True
				break
			A+=C
	return False
def make(m):
	global side,B,A;D,C,M=m;E=I;H=E[D];G=side;J=G^1;K=C
	if H&7==O and C==A and not E[C]:K=C-16 if G==F else C+16
	N=E[K];L.append((m,N,K,B,A,kg[0],kg[1]))
	if N:E[K]=0
	E[D]=0;T=M|G<<3 if M else H;E[C]=T
	if H&7==R:
		kg[G]=C
		if C-D==2 or D-C==2:P=D+3 if C>D else D-4;V=D+1 if C>D else D-1;W=E[P];E[P]=0;E[V]=W
	X=B&U[D]&U[C];B=X;A=-1
	if H&7==O and(C-D==32 or D-C==32):
		Q=C+1;S=C-1
		if not Q&136 and E[Q]==O|J<<3 or not S&136 and E[S]==O|J<<3:A=D+C>>1
	side=J
	if atk(kg[G],J):unmake();return False
	return True
def unmake():
	global side,B,A;F,G,Q,H,J,K,M=L.pop();side^=1
	if F is None:B=H;A=J;kg[0]=K;kg[1]=M;return
	C,E,S=F;D=I;N=side;T=D[E];P=O|N<<3 if S else T;D[C]=P;D[E]=0
	if G:D[Q]=G
	if P&7==R:
		kg[N]=C
		if E-C==2:D[C+3]=D[C+1];D[C+1]=0
		elif C-E==2:D[C-4]=D[C-1];D[C-1]=0
	B=H;A=J;kg[0]=K;kg[1]=M
def gen(caps=False):
	U=caps;G=I;J=side;K=J^1;p=J<<3;c=[];H=c.append
	for D in P(128):
		if D&136:continue
		Y=G[D]
		if not Y or Y>>3!=J:continue
		M=Y&7
		if M==O:
			Q=16 if J==F else-16;Z=D>>4;k=6 if J==F else 1;l=1 if J==F else 6;S=D+Q
			if not G[S]:
				if Z==k:
					for a in(b,W,V,T):H((D,S,a))
				elif not U:
					H((D,S,0))
					if Z==l and not G[S+Q]:H((D,S+Q,0))
			for N in(Q-1,Q+1):
				C=D+N
				if C&136:continue
				L=G[C]
				if L:
					if L>>3!=K:continue
					if Z==k:
						for a in(b,W,V,T):H((D,C,a))
					else:H((D,C,0))
				elif C==A:
					if G[C-16 if J==F else C+16]==O|K<<3:H((D,C,0))
			continue
		if M==T or M==R:
			for N in d if M==T else X:
				C=D+N
				if C&136:continue
				L=G[C]
				if not L:
					if not U:H((D,C,0))
				elif L>>3==K:H((D,C,0))
			if M==R and not U:
				m=0 if J==F else 112;E=m+4
				if D==E and not atk(E,K):
					n=g if J==F else i;o=h if J==F else j
					if B&n and not G[E+1]and not G[E+2]and not atk(E+1,K)and not atk(E+2,K):H((E,E+2,0))
					if B&o and not G[E-1]and not G[E-2]and not G[E-3]and not atk(E-1,K)and not atk(E-2,K):H((E,E-2,0))
			continue
		for N in e if M==V else f if M==W else X:
			C=D+N
			while not C&136:
				L=G[C]
				if not L:
					if not U:H((D,C,0))
				else:
					if L>>3==K:H((D,C,0))
					break
				C+=N
	return c
def x():
	A=[]
	for B in gen():
		if make(B):A.append(B);unmake()
	return A
def ev():
	H=J=B=0;D=[0,0]
	for C in P(128):
		if C&136:continue
		E=I[C]
		if not E:continue
		A=(E&7)-1;G=E>>3;K=1 if G==F else-1;D[G]+=A==2;B+=(0,1,1,2,4,0)[A];L=C if G==F else C^112;M=(7-(L>>4))*8+(L&7);H+=K*(t[A]+Q[A*64+M]);J+=K*(u[A]+Q[384+A*64+M])
	B=min(24,B);N=(H*B+J*(24-B))//24+30*((D[0]>1)-(D[1]>1));return(N if side==F else-N)+10
def y(m):B,C,A=m;return chr(97+(B&7))+str((B>>4)+1)+chr(97+(C&7))+str((C>>4)+1)+('..nbrq'[A:A+1]if A else'')
M=100000
N=0
LB=90000
DL=0
k={}
H=[0]*128
l=[0]*1024
def G():return N>=LB or a.monotonic()>=DL
def Y(m,ply):
	J,B,C=m;D=I;E=D[B];F=D[J]&7
	if E:A=8000+c[E&7]*8-c[F]
	elif C:A=7000+C
	else:
		A=l[F*128+B];G=(ply&63)*2
		if m==H[G]:A+=900
		elif m==H[G+1]:A+=800
	return A
def z():global side,A;A=-1;side^=1
def m(a,b,d,ply):
	B=ply;global N;N+=1
	if G():return ev()
	C=atk(kg[side],side^1);A=ev()
	if not C:
		if A>=b or d<=0:return A
		if A>a:a=A
	D=[(Y(A,B),A)for A in gen(not C)];D.sort(reverse=True);E=0
	for(I,H)in D:
		if G():break
		if not make(H):continue
		E+=1;F=-m(-b,-a,d-1,B+1);unmake()
		if F>A:
			A=F
			if A>a:
				a=A
				if A>=b:return b
	if C and not E:return-M+B
	return A
def S(d,a,b,ply):
	C=ply;global N;N+=1
	if G():return ev()
	Q=atk(kg[side],side^1)
	if Q and d<9:d+=1
	if d<=0:return m(a,b,4,C)
	Z=o(I),side,B,A;c=k.get(Z);R=0
	if c is not None:
		i,e,F,j=c;R=j
		if i>=d:
			if F>90000:F-=C
			elif F<-90000:F+=C
			if e==0:return F
			if e==1:
				if F<=a:return F
			elif F>=b:return F
	n=a
	if not Q and d>2:
		L.append((None,0,0,B,A,kg[0],kg[1]));z();D=-S(d-3,-b,-b+1,C+1);unmake()
		if D>=b:return b
	J=[(Y(A,C),A)for A in gen()];J.sort(reverse=True)
	if R:
		for f in P(K(J)):
			if J[f][1]==R:J.insert(0,J.pop(f));break
	E=-M;g=R;T=0
	for(t,O)in J:
		if G():break
		p,V,q=O;h=not I[V]and not q and V!=A;r=I[p]&7
		if not make(O):continue
		T+=1
		if T==1:D=-S(d-1,-b,-a,C+1)
		else:
			s=1 if h and d>2 and T>4 and not Q else 0;D=-S(d-1-s,-a-1,-a,C+1)
			if D>a:D=-S(d-1,-b,-a,C+1)
		unmake()
		if D>E:
			E=D;g=O
			if D>a:
				a=D
				if D>=b:
					if h:
						U=(C&63)*2
						if H[U]!=O:H[U+1]=H[U];H[U]=O
						l[r*128+V]+=d*d
					break
	if not T:return-M+C if Q else 0
	if E>90000:W=E+C
	elif E<-90000:W=E-C
	else:W=E
	if E<=n:X=1
	elif E>=b:X=2
	else:X=0
	k[Z]=d,X,W,g;return E
def rt(d,pv):
	global N;A=[]
	for B in gen():
		if not make(B):continue
		unmake();A.append((Y(B,0),B))
	if not A:return-M,0,True
	A.sort(reverse=True)
	if pv:
		for H in P(K(A)):
			if A[H][1]==pv:A.insert(0,A.pop(H));break
	F=-M;C=-M;D=A[0][1]
	for(I,B)in A:
		if G():return C,D,False
		if not make(B):continue
		E=-S(d-1,-M,-F,1);unmake()
		if G():return C,D,False
		if E>C:C=E;D=B
		if E>F:F=E
	return C,D,True
def A0(g):
	global N,LB,DL;load(g['fen']);B=x()
	if not B:return
	A=B[0];N=0;LB=120000;DL=a.monotonic()+8
	for C in P(1,41):
		D,E,F=rt(C,A)
		if F:A=E
		if G():break
		if D>M-1000:break
	return A
A1=os.environ.get('MAKEFUN_ENV_URL')
def n(p,b):A=urllib.request.Request(A1+p,Z.dumps(b).encode(),{'content-type':'application/json'});return Z.load(urllib.request.urlopen(A))
def main():
	while True:
		A=n('/game',{})
		if A['status']=='done':break
		while A['status']=='your_move':
			try:B=y(A0(A))
			except Exception:B=None
			if B not in A['legal_moves']:B=sorted(A['legal_moves'])[0]
			A=n('/move',{'game':A['game'],'move':B})
if __name__=='__main__':main()
