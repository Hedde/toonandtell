#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gold-echo-audit: uitwerking van de vooraf afgesproken 8-gram-controle (RESULTS §11).
Waar komt de verbatim-overlap van een concept vandaan: uit het EIGEN gold-verhaal of
uit de rest van het corpus? En staat de gedeelde tekst in de brief? Print alleen getallen.
  own8   : % van de 8-grams van het concept dat in het eigen gold staat
  rest8  : % dat alleen elders in het corpus staat
  runs   : aantal gedeelde reeksen van >=8 woorden met het eigen gold; max = langste
  cov    : % van de woorden van het concept dat in zulke reeksen valt
  nb     : aantal van die reeksen met >=1 inhoudswoord (>=5 letters) dat NERGENS in de brief staat
Gebruik (vanuit analyses/refinement/):  python3 stylometry/triad/gold_echo.py
"""
import glob, re, statistics as st
W = re.compile(r"[a-zàáâäèéêëìíîïòóôöùúûüçñ]+")
def tk(p):
    t = open(p, encoding='utf-8').read()
    for k, v in {'‘': "'", '’': "'", '“': '"', '”': '"'}.items(): t = t.replace(k, v)
    return W.findall(re.sub(r'-\n', '', t).lower())
def grams(t, n): return {tuple(t[i:i + n]) for i in range(len(t) - n + 1)}
def runs(d, G8, n=8):
    out = []; i = 0
    while i <= len(d) - n:
        if tuple(d[i:i + n]) in G8:
            j = i + n
            while j < len(d) and tuple(d[j - n + 1:j + 1]) in G8: j += 1
            out.append((i, j)); i = j
        else: i += 1
    return out
T = 'stylometry/triad'
gold = [l.rstrip('\n').split('\t') for l in open(f'{T}/gold.tsv', encoding='utf-8') if not l.startswith('#')]
corpus = [w for p in sorted(glob.glob('stylometry/raw/real_*.txt')) for w in tk(p)]
C8 = grams(corpus, 8)
print('%-5s %5s %5s %5s %4s %5s %3s' % ('tekst', 'own8', 'rest8', 'runs', 'max', 'cov', 'nb'))
agg = {'A': [], 'B': []}
for nr, _b, _p, _w, gpath in gold:
    g = tk(gpath); G8 = grams(g, 8); brief = set(tk(f'{T}/briefs/brief_{nr}.md'))
    for arm in 'AB':
        d = tk(f'{T}/{arm}_{nr}.txt'); d8 = [tuple(d[i:i + 8]) for i in range(len(d) - 7)]
        own = 100 * sum(x in G8 for x in d8) / len(d8)
        rest = 100 * sum(x in C8 and x not in G8 for x in d8) / len(d8)
        rs = runs(d, G8); cov = 100 * sum(j - i for i, j in rs) / len(d)
        nb = sum(any(len(w) >= 5 and w not in brief for w in d[i:j]) for i, j in rs)
        mx = max((j - i for i, j in rs), default=0)
        agg[arm].append((own, rest, len(rs), mx, cov, nb))
        print('%s_%s %5.1f %5.1f %5d %4d %5.1f %3d' % (arm, nr, own, rest, len(rs), mx, cov, nb))
for arm in 'AB':
    c = list(zip(*agg[arm]))
    print('arm %s gemiddeld: own8 %.1f%%  rest8 %.2f%%  reeksen %.1f  langste (max over 12) %d  dekking %.1f%%  reeksen met woord buiten brief %d van %d' % (
        arm, st.mean(c[0]), st.mean(c[1]), st.mean(c[2]), max(c[3]), st.mean(c[4]), sum(c[5]), sum(c[2])))
more = sum(a[4] > b[4] for a, b in zip(agg['A'], agg['B']))
print(f'A heeft meer gold-dekking dan B in {more}/12 triades')
