#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prompt-echo-audit (deterministisch, heeft het echte corpus NIET nodig).
Toetst het "greatest hits"-mechanisme: lekken de cursieve voorbeeldfrasen uit de
schrijfagent-prompt letterlijk in de AI-teksten? Per groep: aandeel 3-/4-woordreeksen
dat uit die voorbeeldfrasen komt (per 1000 woorden) + ruwe frequenties van enkele
stijlmarkers (per 1000 woorden; zonder echt corpus alleen onderling vergelijkbaar).
Draai vanuit analyses/refinement/:  python3 stylometry/echo.py
"""
import re, glob, statistics as st, collections
W=re.compile(r"[a-zàáâäèéêëìíîïòóôöùúûüçñ]+")
def toks(t): return W.findall(t.lower())
prompt=open('../../.claude/agents/toon-tellegen-schrijver.md',encoding='utf-8').read()
# voorbeeldfrasen = cursief in de prompt
ex=[toks(m) for m in re.findall(r"\*([^*\n]{6,200})\*",prompt)]
P3=set(); P4=set()
for e in ex:
    for i in range(len(e)-2): P3.add(tuple(e[i:i+3]))
    for i in range(len(e)-3): P4.add(tuple(e[i:i+4]))
MARK={'het was stil':r"het was (weer )?stil",'dacht hij/ze':r"dacht (hij|ze|zij)\b",'zomaar':r"\bzomaar\b",
'eigenlijk':r"\beigenlijk\b",'misschien':r"\bmisschien\b",'even later/een tijdje':r"\b(even later|een tijdje)\b",
"'O.'":r"['\"]o[.,]['\"]?",'knikte':r"\bknikte\b",'zweeg':r"\bzweeg\b",'brief':r"\bbrie(f|ven|fje)\b",'verkleinw(-je)':r"\b\w{3,}(je|jes)\b"}
G={'pre: thema':['blindtest7/A_v2.txt','blindtest8/v3.txt']+glob.glob('stylometry/ai_theme/*.txt'),
'pre: premisse':['blindtest8/proof.txt','blindtest9/final.txt']+glob.glob('stylometry/ai_premise/*.txt'),
'bestofn (dialoog)':glob.glob('stylometry/bestofn/*.txt'),
'constrained':glob.glob('stylometry/constrained/*.txt'),
'model opus':glob.glob('stylometry/models/opus_*.txt'),
'model sonnet':glob.glob('stylometry/models/sonnet_*.txt'),
'model haiku':glob.glob('stylometry/models/haiku_*.txt'),
'model codex':glob.glob('stylometry/models/codex_*.txt')}
print(f"prompt-voorbeeldfrasen: {len(ex)}  3-grams: {len(P3)}  4-grams: {len(P4)}")
hdr=list(MARK)
print("%-18s %2s %5s %7s %7s | "%("groep","n","wrd","echo3‰","echo4‰")+" ".join("%8s"%h[:8] for h in hdr))
allhits=collections.Counter(); doc=collections.Counter(); N=0
for g,fs in G.items():
    rows=[]
    for f in sorted(fs):
        t=open(f,encoding='utf-8').read(); tk=toks(t); n=len(tk); N+=1
        h3=[tuple(tk[i:i+3]) for i in range(n-2) if tuple(tk[i:i+3]) in P3]
        h4=[tuple(tk[i:i+4]) for i in range(n-3) if tuple(tk[i:i+4]) in P4]
        for x in set(h4): doc[' '.join(x)]+=1
        low=t.lower()
        rows.append([n,1000*len(h3)/n,1000*len(h4)/n]+[1000*len(re.findall(p,low))/n for p in MARK.values()])
    m=[st.mean(c) for c in zip(*rows)]
    print("%-18s %2d %5d %7.1f %7.1f | "%(g,len(rows),m[0],m[1],m[2])+" ".join("%8.1f"%x for x in m[3:]))
print(f"\nprompt-4-grams die in >=4 van {N} AI-teksten terugkomen:")
for k,v in doc.most_common(25):
    if v>=4: print(f"  {v:2d}x  {k}")
