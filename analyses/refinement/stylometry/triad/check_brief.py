#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inhoudslek-controle: een brief mag geen reeks van 5 of meer opeenvolgende woorden
delen met het gold-verhaal waarvan hij de inhoud samenvat (anders bevoordeelt hij
beide armen gelijk en meet de triade niets meer).
Gebruik:  python3 stylometry/triad/check_brief.py <brief> <gold>
Print 'OK' of de gedeelde reeksen; exit-code 1 bij een lek.
"""
import re, sys
W=re.compile(r"[a-zàáâäèéêëìíîïòóôöùúûüçñ]+")
def toks(p):
    t=open(p,encoding='utf-8').read()
    for k,v in {'‘':"'",'’':"'",'“':'"','”':'"'}.items(): t=t.replace(k,v)
    return W.findall(re.sub(r'-\n','',t).lower())
b,g=toks(sys.argv[1]),toks(sys.argv[2]); N=5
G={tuple(g[i:i+N]) for i in range(len(g)-N+1)}
hits=[]; i=0
while i<=len(b)-N:
    if tuple(b[i:i+N]) in G:
        j=i+N
        while j<len(b) and tuple(b[j-N+1:j+1]) in G: j+=1
        hits.append(' '.join(b[i:min(j,i+12)])+(f' ... ({j-i} woorden)' if j-i>12 else '')); i=j
    else: i+=1
if hits:
    print(f"LEK: {len(hits)} gedeelde reeks(en) van >={N} woorden:")
    for h in hits: print("  -",h)
    sys.exit(1)
print(f"OK: geen gedeelde reeks van >={N} woorden ({len(b)} woorden brief, {len(g)} woorden gold)")
