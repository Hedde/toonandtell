#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Meet willekeurige teksten op twee ONAFHANKELIJKE vingerafdruk-families t.o.v. Tellegen:
  - MFW-Delta   : gem.|z| over 100 most-frequent words (woordniveau)
  - char3-Delta : gem.|z| over top-300 karakter-trigrammen (HELD-OUT validator)
Plus comma/100w en TTR300. Standaardisatie op het echte corpus.
Gebruik:  python3 stylometry/measure.py <label=pad> [<label=pad> ...]
Draai vanuit analyses/refinement/.
"""
import re, glob, sys, statistics as st
QUOTES={'‘':"'",'’':"'",'“':'"','”':'"','…':'...','–':'-','—':'-',' ':' '}
def clean(t):
    for k,v in QUOTES.items(): t=t.replace(k,v)
    t=re.sub(r'-\n','',t); t=re.sub(r'\s*\n\s*',' ',t)
    t=re.sub(r'\bblz?\.?\s*\d+\b','',t,flags=re.I); t=re.sub(r'\s+',' ',t).strip(); return t
WORD=re.compile(r"[a-zàáâäèéêëìíîïòóôöùúûüçñ]+(?:'[a-z]+)?")
def toks(t): return WORD.findall(t.lower())
def sents(t): return [s for s in re.split(r'(?<=[.!?])\s+',t) if len(s.split())>=2]
def load(p): return clean(open(p,encoding='utf-8').read())

real=' '.join(load(p) for p in sorted(glob.glob('stylometry/raw/real_*.txt')))
rt=toks(real)
samp=[]; buf=[]; n=0
for s in sents(real):
    buf.append(s); n+=len(s.split())
    if n>=450: samp.append(' '.join(buf)); buf=[]; n=0

# MFW
cnt={}
for w in rt: cnt[w]=cnt.get(w,0)+1
MFW=[w for w,_ in sorted(cnt.items(),key=lambda x:-x[1])[:100]]
def mfwvec(t):
    tk=toks(t); m=len(tk); c={}
    for w in tk: c[w]=c.get(w,0)+1
    return [c.get(w,0)/m for w in MFW]
# char trigrams
def cgr(t):
    s=re.sub(r'\s+',' ',t.lower()); return [s[i:i+3] for i in range(len(s)-2)]
ccnt={}
for g in cgr(real): ccnt[g]=ccnt.get(g,0)+1
CG=[g for g,_ in sorted(ccnt.items(),key=lambda x:-x[1])[:300]]
def cgvec(t):
    g=cgr(t); m=len(g); c={}
    for x in g: c[x]=c.get(x,0)+1
    return [c.get(x,0)/m for x in CG]

def zparams(vecs):
    mean=[st.mean(c) for c in zip(*vecs)]; sd=[(st.pstdev(c) or 1e-9) for c in zip(*vecs)]
    return mean,sd
mfw_m,mfw_s=zparams([mfwvec(s) for s in samp])
cg_m,cg_s=zparams([cgvec(s) for s in samp])
def dcent(v,m,s): return sum(abs((v[i]-m[i])/s[i]) for i in range(len(v)))/len(v)
real_mfw=[dcent(mfwvec(s),mfw_m,mfw_s) for s in samp]
real_cg=[dcent(cgvec(s),cg_m,cg_s) for s in samp]

def measure(t):
    tk=toks(t); first=tk[:300]
    return (dcent(mfwvec(t),mfw_m,mfw_s), dcent(cgvec(t),cg_m,cg_s),
            t.count(',')/len(tk)*100 if tk else 0,
            len(set(first))/len(first) if first else 0)

print("REFERENTIE echt corpus  MFW-Delta: mean=%.3f max=%.3f | char3-Delta: mean=%.3f max=%.3f | komma/100=%.1f TTR300=%.2f"%(
    st.mean(real_mfw),max(real_mfw),st.mean(real_cg),max(real_cg),
    st.mean([t.count(',')/len(toks(t))*100 for t in samp]),
    st.mean([len(set(toks(t)[:300]))/min(300,len(toks(t))) for t in samp])))
print("%-22s %9s %11s %9s %7s"%("tekst","MFW-Delta","char3-Delta","komma100","TTR300"))
for arg in sys.argv[1:]:
    label,path=arg.split('=',1) if '=' in arg else (arg,arg)
    md,cd,cm,tt=measure(load(path))
    print("%-22s %9.3f %11.3f %9.1f %7.2f"%(label,md,cd,cm,tt))
