import re,glob,sys,statistics as st
QUOTES={'‘':"'",'’':"'",'“':'"','”':'"','…':'...','–':'-','—':'-',' ':' '}
def clean(t):
    for k,v in QUOTES.items(): t=t.replace(k,v)
    t=re.sub(r'-\n','',t);t=re.sub(r'\s*\n\s*',' ',t);t=re.sub(r'\bblz?\.?\s*\d+\b','',t,flags=re.I);return re.sub(r'\s+',' ',t).strip()
WORD=re.compile(r"[a-zàáâäèéêëìíîïòóôöùúûüçñ]+(?:'[a-z]+)?")
def toks(t):return WORD.findall(t.lower())
def sents(t):return [s for s in re.split(r'(?<=[.!?])\s+',t) if len(s.split())>=2]
def load(p):return clean(open(p,encoding='utf-8').read())
real=' '.join(load(p) for p in sorted(glob.glob('stylometry/raw/real_*.txt')));rt=toks(real)
samp=[];buf=[];n=0
for s in sents(real):
    buf.append(s);n+=len(s.split())
    if n>=450:samp.append(' '.join(buf));buf=[];n=0
cnt={}
for w in rt:cnt[w]=cnt.get(w,0)+1
MFW=[w for w,_ in sorted(cnt.items(),key=lambda x:-x[1])[:100]]
def rf(t):tk=toks(t);m=len(tk);c={}; [c.__setitem__(w,c.get(w,0)+1) for w in tk];return {w:c.get(w,0)/m for w in MFW},m
rv=[ [rf(s)[0][w] for w in MFW] for s in samp]
mean=[st.mean(c) for c in zip(*rv)];sd=[(st.pstdev(c) or 1e-9) for c in zip(*rv)]
f=load(sys.argv[1]);fr,m=rf(f)
z=[(fr[MFW[i]]-mean[i])/sd[i] for i in range(len(MFW))]
order=sorted(range(len(MFW)),key=lambda i:-abs(z[i]))
print("MFW-Delta(gem.|z|)=%.3f | woorden=%d"%(sum(abs(x) for x in z)/len(z),m))
print("top-12 afwijkende MFW (z>0 = te VAAK t.o.v. Tellegen, z<0 = te ZELDEN):")
for i in order[:12]:
    print("  %-8s z=%+.2f  (tekst %.1f/1000 vs Tellegen %.1f/1000)"%(MFW[i],z[i],fr[MFW[i]]*1000,mean[i]*1000))
