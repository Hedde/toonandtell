#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lokale, copyright-veilige stylometrie + plagiaat-audit (pilot, pure Python).
- Burrows' Delta in MFW-ruimte, gestandaardiseerd op het ECHTE Tellegen-corpus.
- Nearest-neighbour-discriminatie (kan een AI-tekst doorgaan voor een echte buur?).
- Lexicale / burstiness-features per groep.
- Verbatim-overlap (gedeelde n-grams + langste gemeenschappelijke woordreeks).
Leest verbatim bron-tekst alleen lokaal; print uitsluitend geaggregeerde getallen
+ de langste gedeelde reeks (ter controle dat die generiek is, geen plagiaat).
Draai vanuit analyses/refinement/.
"""
import re, glob, statistics as st

QUOTES={'‘':"'",'’':"'",'“':'"','”':'"','…':'...','–':'-','—':'-',' ':' '}
def clean(t):
    for k,v in QUOTES.items(): t=t.replace(k,v)
    t=re.sub(r'-\n','',t)
    t=re.sub(r'\s*\n\s*',' ',t)
    t=re.sub(r'\bblz?\.?\s*\d+\b','',t,flags=re.I)
    t=re.sub(r'\s+',' ',t).strip()
    return t
WORD=re.compile(r"[a-zàáâäèéêëìíîïòóôöùúûüçñ]+(?:'[a-z]+)?")
def toks(t): return WORD.findall(t.lower())
def sents(t): return [s for s in re.split(r'(?<=[.!?])\s+', t) if len(s.split())>=2]
def load(p): return clean(open(p,encoding='utf-8').read())

# ---- echte corpus: zinnen groeperen tot ~450-woord-samples (leestekens behouden) ----
real_text=' '.join(load(p) for p in sorted(glob.glob('stylometry/raw/real_*.txt')))
real_tok=toks(real_text)
real_samples=[]; buf=[]; n=0
for s in sents(real_text):
    buf.append(s); n+=len(s.split())
    if n>=450: real_samples.append(' '.join(buf)); buf=[]; n=0
if n>=200: real_samples.append(' '.join(buf))

PREMISE={'zeekomkommer':'blindtest8/proof.txt','olifant':'blindtest9/final.txt',
         'wielewaal':'stylometry/ai_premise/wielewaal.txt','wesp':'stylometry/ai_premise/wesp.txt',
         'zeearend':'stylometry/ai_premise/zeearend.txt'}
THEME={'karper(thema)':'blindtest7/A_v2.txt','spitsmuis':'blindtest8/v3.txt',
       'krekel':'stylometry/ai_theme/krekel_eenzaamheid.txt','karper_gemis':'stylometry/ai_theme/karper_gemis.txt',
       'oudworden':'stylometry/ai_theme/oudworden.txt'}
premise={k:load(v) for k,v in PREMISE.items()}
theme={k:load(v) for k,v in THEME.items()}

# ---- MFW + z-standaardisatie op echt corpus ----
cnt={}
for w in real_tok: cnt[w]=cnt.get(w,0)+1
MFW=[w for w,_ in sorted(cnt.items(),key=lambda x:-x[1])[:100]]
def vec(t):
    tk=toks(t); n=len(tk); c={}
    for w in tk: c[w]=c.get(w,0)+1
    return [c.get(w,0)/n for w in MFW]
rv=[vec(s) for s in real_samples]
mean=[st.mean(c) for c in zip(*rv)]; sd=[(st.pstdev(c) or 1e-9) for c in zip(*rv)]
def zof(t): v=vec(t); return [(v[i]-mean[i])/sd[i] for i in range(len(MFW))]
def d_centroid(t): zz=zof(t); return sum(abs(x) for x in zz)/len(zz)
def delta(za,zb): return sum(abs(za[i]-zb[i]) for i in range(len(MFW)))/len(MFW)

real_z=[zof(s) for s in real_samples]
real_d=[d_centroid(s) for s in real_samples]
rmean,rsd=st.mean(real_d),st.pstdev(real_d)
def zsc(d): return (d-rmean)/rsd
# nearest-neighbour Delta (binnen echt; en AI -> dichtstbijzijnde echte)
def nn_real(zq, exclude=-1):
    best=1e9
    for i,zr in enumerate(real_z):
        if i==exclude: continue
        d=delta(zq,zr)
        if d<best: best=d
    return best
real_nn=[nn_real(real_z[i],i) for i in range(len(real_z))]

# ---- lexicale features ----
def feats(t):
    tk=toks(t); sl=[len(s.split()) for s in sents(t)]; first=tk[:300]
    return {'zinsl_gem':st.mean(sl) if sl else 0,'zinsl_sd':st.pstdev(sl) if len(sl)>1 else 0,
            'burst_cv':(st.pstdev(sl)/st.mean(sl)) if len(sl)>1 and st.mean(sl) else 0,
            'TTR300':len(set(first))/len(first) if first else 0,
            'hapax300':sum(1 for w in set(first) if first.count(w)==1)/len(first) if first else 0,
            'woordlen':st.mean([len(w) for w in tk]) if tk else 0,
            'komma100':t.count(',')/len(tk)*100 if tk else 0}
def gfeat(texts):
    fs=[feats(t) for t in texts]
    return {k:st.mean([f[k] for f in fs]) for k in fs[0]}

# ---- verbatim overlap ----
def ngr(tokens,n): return set(tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1))
real_ng={k:ngr(real_tok,k) for k in (3,4,5,6,7,8,10,12)}
def overlap(t):
    tk=toks(t)
    def frac(n):
        g=[tuple(tk[i:i+n]) for i in range(len(tk)-n+1)]
        return 100*sum(1 for x in g if x in real_ng[n])/len(g) if g else 0
    longest=0; ex=''
    for n in (3,4,5,6,7,8,10,12):
        hit=[tuple(tk[i:i+n]) for i in range(len(tk)-n+1) if tuple(tk[i:i+n]) in real_ng[n]]
        if hit: longest=n; ex=' '.join(hit[0])
    return round(frac(5),1),round(frac(8),1),longest,ex

print("="*74)
print("STYLOMETRIE + PLAGIAAT-AUDIT — pilot (pure Python, n klein: zie caveat)")
print("="*74)
print(f"Echt corpus: {len(real_tok)} woorden -> {len(real_samples)} samples | MFW={len(MFW)}")
print()
print("--- 1. DELTA tot Tellegen-profiel (gem.|z|; ~0.80 = typische ruis; lager=dichterbij) ---")
print(f"ECHT spreiding: mean={rmean:.3f} sd={rsd:.3f} min={min(real_d):.3f} max={max(real_d):.3f}")
def show(group,name):
    ds=[]
    for k,t in group.items():
        d=d_centroid(t); ds.append(d)
        fl="binnen" if d<=max(real_d) else f"BUITEN +{zsc(d):.1f}sd"
        print(f"  {name:9s} {k:15s} delta={d:.3f}  z={zsc(d):+.2f}  [{fl}]")
    print(f"  >> {name} gemiddeld = {st.mean(ds):.3f}")
    return st.mean(ds)
pm=show(premise,"premisse"); print(); tm=show(theme,"thema")
print(f"\nVergelijk: ECHT={rmean:.3f}  premisse={pm:.3f}  thema={tm:.3f}  (verschil premisse-thema={abs(pm-tm):.3f})")
print()
print("--- 2. NEAREST-NEIGHBOUR Delta (kan tekst doorgaan voor een echte buur?) ---")
print(f"ECHT->dichtstbijzijnde echte: mean={st.mean(real_nn):.3f} (max={max(real_nn):.3f})")
for name,group in (("premisse",premise),("thema",theme)):
    for k,t in group.items():
        print(f"  {name:9s} {k:15s} dichtstbijzijnde echte Delta={nn_real(zof(t)):.3f}")
print()
print("--- 3. LEXICALE / BURSTINESS-FEATURES (groepsgemiddelden) ---")
gr={'ECHT':real_samples,'premisse':list(premise.values()),'thema':list(theme.values())}
ks=None
for g,ts in gr.items():
    gf=gfeat(ts)
    if ks is None: ks=list(gf); print("  groep      "+"  ".join(f"{k:>9s}" for k in ks))
    print(f"  {g:9s} "+"  ".join(f"{gf[k]:9.2f}" for k in ks))
print()
print("--- 4. VERBATIM-OVERLAP (plagiaat-audit) ---")
for name,group in (("premisse",premise),("thema",theme)):
    for k,t in group.items():
        f5,f8,lng,ex=overlap(t)
        print(f"  {name:9s} {k:15s} 5-gram={f5}% 8-gram={f8}% langste={lng}w: \"{ex}\"")
