#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deterministische "gold triad"-rechter (naar Taylor/Every, nov 2026), zonder LLM-jury.

Per triade: één ECHT verhaal (gold) + twee concepten A en B die uit DEZELFDE
inhoudsbrief van dat verhaal zijn geschreven (zelfde inhoud, alleen de
schrijfconfiguratie verschilt). De rechter kiest het concept dat dichter bij het
gold ligt, per vingerafdruk-familie:
  - MFW   : gem.|zA - zGold| over 100 most-frequent words
  - char3 : gem.|zA - zGold| over top-300 karakter-trigrammen
z-standaardisatie op het echte corpus (stylometry/raw/real_*.txt), zoals measure.py.
Volgorde-onafhankelijk en herhaalbaar per constructie (geen positie-bias, geen
contextinstabiliteit). Over alle triades: winstpercentage van A + tweezijdige tekentoets.

Manifest (TSV, één triade per regel, # = commentaar):
    <pad gold>\t<pad concept A>\t<pad concept B>
Gebruik (vanuit analyses/refinement/):
    python3 stylometry/triad.py manifest.tsv
Het gold-verhaal hoort bij voorkeur NIET in de voorbeelden/constraints van de
schrijfconfiguratie te zitten (held-out), anders meet je memorisatie.
"""
import re, glob, sys, os, math, statistics as st

QUOTES={'‘':"'",'’':"'",'“':'"','”':'"','…':'...','–':'-','—':'-',' ':' '}
def clean(t):
    for k,v in QUOTES.items(): t=t.replace(k,v)
    t=re.sub(r'-\n','',t); t=re.sub(r'\s*\n\s*',' ',t)
    t=re.sub(r'\bblz?\.?\s*\d+\b','',t,flags=re.I); return re.sub(r'\s+',' ',t).strip()
WORD=re.compile(r"[a-zàáâäèéêëìíîïòóôöùúûüçñ]+(?:'[a-z]+)?")
def toks(t): return WORD.findall(t.lower())
def sents(t): return [s for s in re.split(r'(?<=[.!?])\s+',t) if len(s.split())>=2]
def load(p): return clean(open(p,encoding='utf-8').read())
def cgr(t):
    s=re.sub(r'\s+',' ',t.lower()); return [s[i:i+3] for i in range(len(s)-2)]

REF=os.environ.get('STYLO_REF','stylometry/raw/real_*.txt')
paths=sorted(glob.glob(REF))
if not paths: sys.exit(f"geen referentiecorpus gevonden op {REF} — draai eerst stylometry/extract_corpus.sh <map met PDF's>")
real=' '.join(load(p) for p in paths)
samp=[]; buf=[]; n=0
for s in sents(real):
    buf.append(s); n+=len(s.split())
    if n>=450: samp.append(' '.join(buf)); buf=[]; n=0

def top(items,k):
    c={}
    for x in items: c[x]=c.get(x,0)+1
    return [x for x,_ in sorted(c.items(),key=lambda kv:(-kv[1],kv[0]))[:k]]
def family(units,k):
    feats=top(units(real),k)
    def vec(t):
        u=units(t); m=len(u) or 1; c={}
        for x in u: c[x]=c.get(x,0)+1
        return [c.get(f,0)/m for f in feats]
    vs=[vec(s) for s in samp]
    mean=[st.mean(c) for c in zip(*vs)]; sd=[(st.pstdev(c) or 1e-9) for c in zip(*vs)]
    return lambda t:[(v-mean[i])/sd[i] for i,v in enumerate(vec(t))]
FAM={'MFW':family(toks,100),'char3':family(cgr,300)}
def dist(za,zb): return sum(abs(a-b) for a,b in zip(za,zb))/len(za)

def sign_p(w,l):
    """tweezijdige exacte tekentoets (gelijkspel telt niet mee)"""
    m=w+l
    if m==0: return 1.0
    k=min(w,l); return min(1.0,2*sum(math.comb(m,i) for i in range(k+1))/2**m)

def main():
    if len(sys.argv)!=2: sys.exit(__doc__)
    tri=[l.rstrip('\n').split('\t') for l in open(sys.argv[1],encoding='utf-8') if l.strip() and not l.startswith('#')]
    wins={f:[0,0] for f in FAM}; both=[0,0,0]
    print("%-28s %8s %8s %3s | %8s %8s %3s"%("gold","MFW:A","MFW:B","win","char3:A","char3:B","win"))
    for g,a,b in tri:
        G,A,B=load(g),load(a),load(b); row=[]; w=[]
        for f,z in FAM.items():
            da,db=dist(z(A),z(G)),dist(z(B),z(G))
            win='A' if da<db else 'B' if db<da else '='
            if win!='=': wins[f][win=='B']+=1
            row+=[da,db,win]; w.append(win)
        both[0 if w==['A','A'] else 1 if w==['B','B'] else 2]+=1
        print("%-28s %8.3f %8.3f %3s | %8.3f %8.3f %3s"%(os.path.basename(g)[:28],*row))
    print()
    for f,(wa,wb) in wins.items():
        tot=wa+wb
        print(f"{f:6s} A wint {wa}/{tot} ({100*wa/tot if tot else 0:.0f}%)  tekentoets p={sign_p(wa,wb):.3f}")
    print(f"beide families eens: A {both[0]}, B {both[1]}, verdeeld {both[2]}  (n={len(tri)})")
    print("Lees: alleen een winst op BEIDE families (char3 = scherpste) én p<0,05 is een bevinding; n<12 is indicatief.")
if __name__=='__main__': main()
