#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mechanische, vooraf vastgelegde gold-selectie voor het triad-experiment (RESULTS §11).
Kijkt naar GEEN enkele stylometrische maat. Print alleen bundel/pagina's/woordtal;
de gold-teksten zelf gaan via pdftotext naar het gitignored stylometry/raw/gold_*.txt.

Regel:
  1. Verhaalgrenzen: een verhaal begint op een pagina waarvan het eerste woord laag
     op de pagina staat (Dank je wel) of '##' is (overige bundels).
  2. Uit: buiten 250-600 woorden; eerder in een blindtest gebruikt; deelt een reeks
     van >=5 woorden of een volledige cursieve voorbeeldfrase (>=4 woorden) met de
     schrijfagent-prompt; bevat een beeld dat de prompt aan Tellegen ontleent.
  3. Per bundel: sorteer de rest op lengte, kies de posities 1/6, 3/6 en 5/6.
Gebruik (vanuit analyses/refinement/):  python3 stylometry/triad/select_gold.py <map met PDF's>
"""
import subprocess, re, sys, html, os
PDFDIR=sys.argv[1] if len(sys.argv)>1 else '../../..'
B={'djw':'Dank_je_wel','ehodr':'Een_hart_onder_de_riem','mnuhh':'Maar_niet_uit_het_hart','mhez':'Met_hart_en_ziel'}
RANGE={'mnuhh':(5,41),'mhez':(5,40),'ehodr':(5,40),'djw':(5,40)}   # zelfde pagina's als extract_corpus.sh
QUOTES={'‘':"'",'’':"'",'“':'"','”':'"','…':'...','–':'-','—':'-',' ':' '}
def clean(t):
    for k,v in QUOTES.items(): t=t.replace(k,v)
    t=re.sub(r'-\n','',t); t=re.sub(r'\s*\n\s*',' ',t)
    t=re.sub(r'\bblz?\.?\s*\d+\b','',t,flags=re.I); return re.sub(r'\s+',' ',t).strip()
WORD=re.compile(r"[a-zàáâäèéêëìíîïòóôöùúûüçñ]+(?:'[a-z]+)?")
def toks(t): return WORD.findall(t.lower())
W=re.compile(r"[a-zàáâäèéêëìíîïòóôöùúûüçñ]+")
def wt(t): return W.findall(t.lower())
def pdf(k): return f'{PDFDIR}/Toon_Tellegen-{B[k]}.pdf'
def firstwords(k):
    out=subprocess.run(['pdftotext','-bbox-layout',pdf(k),'-'],capture_output=True,text=True).stdout
    res=[]
    for pg in re.findall(r'<page [^>]*>(.*?)</page>',out,flags=re.S):
        m=re.search(r'<word xMin="[\d.]+" yMin="([\d.]+)" xMax="[\d.]+" yMax="[\d.]+">(.*?)</word>',pg,flags=re.S)
        res.append((float(m.group(1)),html.unescape(m.group(2))) if m else None)
    return res
def storymap():
    res=[]
    for k in B:
        fw=firstwords(k); lo,hi=RANGE[k]
        starts=[i for i in range(lo,hi+1) if fw[i-1] and (fw[i-1][0]>150 or fw[i-1][1]=='##')]
        for j,s in enumerate(starts):
            e=(starts[j+1]-1) if j+1<len(starts) else hi
            txt=subprocess.run(['pdftotext','-nopgbrk','-f',str(s),'-l',str(e),pdf(k),'-'],capture_output=True,text=True).stdout
            res.append(dict(bundle=k,start=s,end=e,words=len(toks(clean(txt))),text=clean(txt)))
    return res

prompt=open('../../.claude/agents/toon-tellegen-schrijver.md',encoding='utf-8').read()
pt=wt(prompt); PG5={tuple(pt[i:i+5]) for i in range(len(pt)-4)}
ITAL=[' '.join(e) for e in (wt(m) for m in re.findall(r"\*([^*\n]{6,200})\*",prompt)) if len(e)>=4]
IMG=['watertaart','grastaart','beukennotensap','zoethout','mossel','verkreukelen','treurige taart','lepelaar',
     'wanhoop','woede','lijster','ladder','bijna heerlijk']
BLIND={('mnuhh',5):'vergeetboek',('mnuhh',7):'Ik moet op reis',('ehodr',26):'pinguïn',('ehodr',28):'nu of nooit',
       ('mhez',5):'watertaart',('ehodr',11):'blindtest5 leeuw',('djw',28):'blindtest5 boktor'}
sm=storymap(); pool=[]
for s in sm:
    tk=wt(s['text']); low=' '.join(tk); why=[]
    if not 250<=s['words']<=600: why.append('lengte')
    if (s['bundle'],s['start']) in BLIND: why.append('blindtest: '+BLIND[(s['bundle'],s['start'])])
    if 'nachtegaal' in low and s['bundle']=='djw': why.append('blindtest5 nachtegaal')
    if any(tuple(tk[j:j+5]) in PG5 for j in range(len(tk)-4)): why.append('>=5-gram met prompt')
    if any(e in low for e in ITAL): why.append('volledige voorbeeldfrase')
    im=[k for k in IMG if k in low]
    if 'sneeuw' in low and 'brief' in low: im.append('brief/sneeuw')
    if ('muur' in low or 'muren' in low) and 'boos' in low: im.append('boze muur')
    if 'stekels' in low and ('trok' in low or 'uit' in low): im.append('egel/stekels')
    if im: why.append('prompt-beeld: '+','.join(im))
    print(f"{s['bundle']:6s} p{s['start']:02d}-{s['end']:02d} w={s['words']:4d} {'OK ' if not why else 'UIT'} {'; '.join(why)}")
    if not why: pool.append(s)
sel=[]
for b in ('djw','ehodr','mnuhh','mhez'):
    p=sorted([s for s in pool if s['bundle']==b],key=lambda s:(s['words'],s['start']))
    sel+=[p[(2*k+1)*len(p)//6] for k in range(3)]
print(f"\n{len(sm)} verhalen, {len(pool)} geschikt, {len(sel)} gekozen")
os.makedirs('stylometry/raw',exist_ok=True)
with open('stylometry/triad/gold.tsv','w',encoding='utf-8') as f:
    f.write("# nr\tbundel\tpagina's\twoorden\tgold-bestand (gitignored)\n")
    for i,s in enumerate(sel,1):
        dst=f"stylometry/raw/gold_{i:02d}_{s['bundle']}_p{s['start']:02d}.txt"
        subprocess.run(['pdftotext','-nopgbrk','-f',str(s['start']),'-l',str(s['end']),pdf(s['bundle']),dst],check=True)
        f.write(f"{i:02d}\t{s['bundle']}\t{s['start']}-{s['end']}\t{s['words']}\t{dst}\n")
        print(f"gold {i:02d}: {s['bundle']} p{s['start']}-{s['end']} {s['words']} woorden -> {dst}")
