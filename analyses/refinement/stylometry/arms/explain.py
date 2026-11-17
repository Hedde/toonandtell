#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verklarende uitsplitsing bij RESULTS §12 (post hoc, beschrijvend; geen toetsen, geen beslisregel).
Waarom scheidt de detector een arm van echt? Splitst de scheiding in:
  verschuiving = afstand tussen het gemiddelde van de arm en het gemiddelde van echt (z-ruimte, namen gemaskeerd)
  spreiding    = gemiddelde afstand van een tekst tot het gemiddelde van de eigen groep
en toont welke woorden het meest verschoven zijn, plus leestekens per 100 woorden.
Gebruik (vanuit analyses/refinement/):  python3 stylometry/arms/explain.py
"""
import statistics as st, sys
sys.path.insert(0, 'stylometry/arms')
import analyse as A
M = A.M
dr = A.load_drafts(); det = A.Detector([t for ts in dr.values() for t in ts]); real = A.real_units()
def mean(vs): return [sum(c) / len(vs) for c in zip(*vs)]
print('%-9s %-5s | %12s %10s | %12s %10s' % ('groep', '', 'MFW verschuiv', 'spreiding', 'c3 verschuiv', 'spreiding'))
RZ = {f: [det.z(t, f) for t in real] for f in A.FAMS}; RC = {f: mean(RZ[f]) for f in A.FAMS}
print('%-9s %-5s | %12s %10.3f | %12s %10.3f' % ('echt', '', '-', st.mean(A.l1(v, RC['MFW']) for v in RZ['MFW']), '-', st.mean(A.l1(v, RC['char3']) for v in RZ['char3'])))
Z = {}
for m in A.MODELS:
    for a in A.ARMS:
        row = []
        for f in A.FAMS:
            z = [det.z(A.head(t), f) for s in A.SEEDS for t in dr[(m, a, s)]]; c = mean(z); Z[(m, a, f)] = c
            row += [A.l1(c, RC[f]), st.mean(A.l1(v, c) for v in z)]
        print('%-9s %-5s | %12.3f %10.3f | %12.3f %10.3f' % (m, a, *row))
print('\nmeest verschoven woorden per arm (gemiddelde z van de arm min die van echt; + = arm gebruikt het vaker dan Tellegen):')
for m in A.MODELS:
    for a in A.ARMS:
        d = [(Z[(m, a, 'MFW')][i] - RC['MFW'][i], w) for i, w in enumerate(det.feat['MFW'])]
        top = sorted(d, key=lambda x: -abs(x[0]))[:12]
        print(f'  {m:5s} {a}: ' + ' '.join(f'{w}{x:+.1f}' for x, w in top))
print('\nleestekens per 100 woorden (hele tekst):')
PUN = [',', '.', '?', '!', ':', ';', "'", '...', '-']
def rate(texts):
    n = sum(len(M.toks(t)) for t in texts); return [100 * sum(t.count(p) for t in texts) / n for p in PUN]
print('%-12s ' % '' + ' '.join('%6s' % p for p in PUN))
print('%-12s ' % 'echt' + ' '.join('%6.2f' % x for x in rate(real)))
for m in A.MODELS:
    for a in A.ARMS:
        print('%-12s ' % f'{m} {a}' + ' '.join('%6.2f' % x for x in rate([t for s in A.SEEDS for t in dr[(m, a, s)]])))
print('\ngem. zinslengte (woorden) en aandeel woorden in dialoog (tussen enkele quotes):')
import re
def sl(texts):
    s = [len(x.split()) for t in texts for x in A.SPLIT.split(t) if x.strip()]; return st.mean(s)
def dia(texts):
    n = sum(len(M.toks(t)) for t in texts); q = sum(len(M.toks(x)) for t in texts for x in re.findall(r"(?:(?<=\s)|^)'([^']{2,}?)'(?=[\s.,!?]|$)", t)); return 100 * q / n
print('%-12s zinslengte %5.1f  dialoog %4.1f%%' % ('echt', sl(real), dia(real)))
for m in A.MODELS:
    for a in A.ARMS:
        ts = [t for s in A.SEEDS for t in dr[(m, a, s)]]
        print('%-12s zinslengte %5.1f  dialoog %4.1f%%' % (f'{m} {a}', sl(ts), dia(ts)))

print('\nde woorden waar de register-constraints op sturen (z van de arm min z van echt; 0 = als Tellegen):')
TARGET = ['was', 'niet', 'dan', 'nu', 'in', 'uit', 'op', 'zijn']
print('%-9s ' % '' + ' '.join('%6s' % w for w in TARGET) + '   (constraint: minder was/niet/dan/nu, meer in/uit/op/zijn)')
for m in A.MODELS:
    for a in A.ARMS:
        print('%-9s ' % f'{m} {a}' + ' '.join('%+6.1f' % (Z[(m, a, 'MFW')][det.feat['MFW'].index(w)] - RC['MFW'][det.feat['MFW'].index(w)]) for w in TARGET))

print('\ngedeelde reeksen van >=8 woorden met het corpus (alle concepten):')
W = re.compile(r"[a-zàáâäèéêëìíîïòóôöùúûüçñ]+")
corpus = W.findall(M.real.lower()); C8 = {tuple(corpus[i:i + 8]) for i in range(len(corpus) - 7)}
n = 0
for (m, a, s), ts in dr.items():
    for k, t in enumerate(ts, 1):
        tk = W.findall(t.lower()); i = 0
        while i <= len(tk) - 8:
            if tuple(tk[i:i + 8]) in C8:
                j = i + 8
                while j < len(tk) and tuple(tk[j - 7:j + 1]) in C8: j += 1
                n += 1; print(f'  {m} {a} {s} {k}: {j - i} woorden: "{" ".join(tk[i:j])}"'); i = j
            else: i += 1
print(f'{n} reeksen in 216 concepten')
