#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zelftoets bij RESULTS §11 (post hoc, verkennend, verandert de beslisregel niet):
kan de uitkomst "kale variant minstens zo dichtbij" een artefact van de opzet zijn?
Gebruikt alleen bestaande teksten, ook de door de lengtepoort afgekeurde pogingen.
  1. ruisvloer: twee pogingen van DEZELFDE arm op DEZELFDE brief (afgekeurd vs geteld);
  2. gevoeligheid voor de lengtepoort: uitslag met de eerste poging van elke cel;
  3. lengte: hangt het lengteverschil A-B samen met het afstandsverschil A-B?
  4. verboden woorden: staan woorden die de volledige prompt verbiedt in het gold?
  5. toevoegingen: wijkt A verder af van de brief / het gold-vocabulaire dan B?
Gebruik (vanuit analyses/refinement/):  python3 stylometry/triad/selfcheck.py
"""
import glob, os, re, statistics as st, sys
sys.path.insert(0, 'stylometry')
import triad as J                                  # zelfde rechter: J.FAM, J.dist, J.load, J.sign_p

T = 'stylometry/triad'
gold = [l.rstrip('\n').split('\t') for l in open(f'{T}/gold.tsv', encoding='utf-8') if not l.startswith('#')]
G = {nr: J.load(p) for nr, _b, _p, _w, p in gold}
def d(text, nr): return {f: J.dist(z(text), z(G[nr])) for f, z in J.FAM.items()}
final = {(a, nr): J.load(f'{T}/{a}_{nr}.txt') for nr in G for a in 'AB'}
tries = {}
for p in sorted(glob.glob(f'{T}/rejected/*.txt')):
    a, nr, k = re.match(r'([AB])_(\d\d)_try(\d)', os.path.basename(p)).groups()
    tries.setdefault((a, nr), []).append(J.load(p))
D = {k: d(t, k[1]) for k, t in final.items()}

print('--- 1. ruisvloer: |afstand poging - afstand getelde versie|, zelfde arm, zelfde brief ---')
noise = {'MFW': [], 'char3': []}
for (a, nr), ts in sorted(tries.items()):
    for i, t in enumerate(ts, 1):
        x = d(t, nr)
        for f in noise: noise[f].append(abs(x[f] - D[(a, nr)][f]))
        print(f'{a}_{nr} poging {i}: MFW {x["MFW"]:.3f} vs {D[(a, nr)]["MFW"]:.3f} | char3 {x["char3"]:.3f} vs {D[(a, nr)]["char3"]:.3f}')
arm = {f: [abs(D[('A', nr)][f] - D[('B', nr)][f]) for nr in G] for f in noise}
for f in noise:
    print(f'{f:6s} binnen arm (n={len(noise[f])}): mediaan {st.median(noise[f]):.3f} gem. {st.mean(noise[f]):.3f} max {max(noise[f]):.3f}'
          f'  ||  tussen armen (n=12): mediaan {st.median(arm[f]):.3f} gem. {st.mean(arm[f]):.3f} max {max(arm[f]):.3f}')

print('\n--- 2. uitslag met de EERSTE poging van elke cel (alsof er geen lengtepoort was) ---')
def tally(pick):
    res = {}
    for f in J.FAM:
        wa = sum(pick('A', nr)[f] < pick('B', nr)[f] for nr in G); wb = sum(pick('B', nr)[f] < pick('A', nr)[f] for nr in G)
        res[f] = (wa, wb, J.sign_p(wa, wb))
    return res
first = lambda a, nr: d(tries[(a, nr)][0], nr) if (a, nr) in tries else D[(a, nr)]
for name, pick in (('geteld (met poort)', lambda a, nr: D[(a, nr)]), ('eerste poging', first)):
    r = tally(pick)
    print(f'{name:20s} MFW A {r["MFW"][0]} - B {r["MFW"][1]} (p={r["MFW"][2]:.3f}) | char3 A {r["char3"][0]} - B {r["char3"][1]} (p={r["char3"][2]:.3f})')
flip = {f: [nr for nr in G if (first('A', nr)[f] < first('B', nr)[f]) != (D[('A', nr)][f] < D[('B', nr)][f])] for f in J.FAM}
print('triades waar de winnaar omslaat door de poort:', flip)
for f in J.FAM:
    floor = st.median(noise[f])
    big = [(nr, D[('A', nr)][f] - D[('B', nr)][f]) for nr in G if abs(D[('A', nr)][f] - D[('B', nr)][f]) > floor]
    print(f'{f}: triades met marge boven de ruisvloer ({floor:.3f}): {len(big)} -> A wint {sum(x < 0 for _, x in big)}, B wint {sum(x > 0 for _, x in big)}')

print('\n--- 3. lengte: verband tussen (woorden A - woorden B) en (afstand A - afstand B) ---')
nw = {k: len(J.toks(t)) for k, t in final.items()}
dl = [nw[('A', nr)] - nw[('B', nr)] for nr in G]
def pearson(x, y):
    mx, my = st.mean(x), st.mean(y)
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y)) ** .5
for f in J.FAM:
    print(f'{f}: r = {pearson(dl, [D[("A", nr)][f] - D[("B", nr)][f] for nr in G]):+.2f}   (A langer in {sum(x > 0 for x in dl)}/12)')

print('\n--- 4. woorden die de volledige prompt verbiedt of afraadt: aantal in gold / A / B ---')
BAN = ['thee', 'drempel', 'zoethout', 'gewoon', 'eigenlijk', 'alsof', 'verdween', 'merkwaardig', 'taart', 'peinsde', 'sprak']
tot = {w: [0, 0, 0] for w in BAN}
for nr in G:
    for w in BAN:
        c = [len(re.findall(r'\b' + w + r'\b', t.lower())) for t in (G[nr], final[('A', nr)], final[('B', nr)])]
        for i in range(3): tot[w][i] += c[i]
for w, c in tot.items(): print(f'{w:12s} gold {c[0]:3d}  A {c[1]:3d}  B {c[2]:3d}')

print('\n--- 5. toevoegingen: inhoudswoorden (>=5 letters, types) van het concept ---')
W = re.compile(r"[a-zàáâäèéêëìíîïòóôöùúûüçñ]{5,}")
na = {'A': [], 'B': []}; ng = {'A': [], 'B': []}
for nr in G:
    brief = set(W.findall(open(f'{T}/briefs/brief_{nr}.md', encoding='utf-8').read().lower())); g = set(W.findall(G[nr].lower()))
    for a in 'AB':
        t = set(W.findall(final[(a, nr)].lower()))
        na[a].append(100 * len(t - brief) / len(t)); ng[a].append(100 * len(t & g) / len(t))
print('niet in de brief:  A %.1f%%  B %.1f%%  (A hoger in %d/12)' % (st.mean(na['A']), st.mean(na['B']), sum(x > y for x, y in zip(na['A'], na['B']))))
print('ook in het gold:   A %.1f%%  B %.1f%%  (A hoger in %d/12)' % (st.mean(ng['A']), st.mean(ng['B']), sum(x > y for x, y in zip(ng['A'], ng['B']))))

print('\n--- 6. lengte nader: zonder triade 10, en alleen lengte-gelijke triades (|A-B| <= 5% van gold) ---')
gw = {nr: int(w) for nr, _b, _p, w, _path in gold}
keep = [nr for nr in G if nr != '10']
for f in J.FAM:
    print(f'{f}: r zonder triade 10 = {pearson([nw[("A", nr)] - nw[("B", nr)] for nr in keep], [D[("A", nr)][f] - D[("B", nr)][f] for nr in keep]):+.2f}')
eq = [nr for nr in G if abs(nw[('A', nr)] - nw[('B', nr)]) <= 0.05 * gw[nr]]
for f in J.FAM:
    print(f'{f}: lengte-gelijk (n={len(eq)}): A wint {sum(D[("A", nr)][f] < D[("B", nr)][f] for nr in eq)}, B wint {sum(D[("B", nr)][f] < D[("A", nr)][f] for nr in eq)}')

print('\n--- 7. gold-echo gemaskeerd: letterlijke reeksen (>=8 woorden uit het eigen gold) uit beide concepten geknipt ---')
WL = re.compile(r"[a-zàáâäèéêëìíîïòóôöùúûüçñ]+")
def mask(text, g):
    gt = WL.findall(g.lower()); G8 = {tuple(gt[i:i + 8]) for i in range(len(gt) - 7)}
    sp = [(m.start(), m.end(), m.group()) for m in WL.finditer(text.lower())]; tk = [s[2] for s in sp]
    cut = []; i = 0
    while i <= len(tk) - 8:
        if tuple(tk[i:i + 8]) in G8:
            j = i + 8
            while j < len(tk) and tuple(tk[j - 7:j + 1]) in G8: j += 1
            cut.append((sp[i][0], sp[j - 1][1])); i = j
        else: i += 1
    out = []; pos = 0
    for a, b in cut: out.append(text[pos:a]); pos = b
    return ' '.join((''.join(out) + text[pos:]).split())
M = {k: d(mask(t, G[k[1]]), k[1]) for k, t in final.items()}
r = tally(lambda a, nr: M[(a, nr)])
print(f'gemaskeerd: MFW A {r["MFW"][0]} - B {r["MFW"][1]} (p={r["MFW"][2]:.3f}) | char3 A {r["char3"][0]} - B {r["char3"][1]} (p={r["char3"][2]:.3f})')
for f in J.FAM: print(f'{f}: gem. afstand gemaskeerd A {st.mean(M[("A", nr)][f] for nr in G):.3f}  B {st.mean(M[("B", nr)][f] for nr in G):.3f}')

print('\n--- 8. waar zit het char3-verschil? bijdrage per trigram aan (afstand A - afstand B), som over 12 triades ---')
feats = J.top(J.cgr(J.real), 300); z = J.FAM['char3']
contrib = [0.0] * 300
for nr in G:
    zg, za, zb = z(G[nr]), z(final[('A', nr)]), z(final[('B', nr)])
    for i in range(300): contrib[i] += (abs(za[i] - zg[i]) - abs(zb[i] - zg[i])) / 300 / 12
punct = [i for i, g in enumerate(feats) if re.search(r"[^a-zàáâäèéêëìíîïòóôöùúûüçñ ]", g)]
letters = [i for i in range(300) if i not in punct]
tot = sum(contrib)
print(f'totaal A-B = {tot:+.4f} | uit {len(punct)} trigrammen met leesteken/quote: {sum(contrib[i] for i in punct):+.4f} | uit {len(letters)} letter/spatie-trigrammen: {sum(contrib[i] for i in letters):+.4f}')
order = sorted(range(300), key=lambda i: -contrib[i])
print('A verder van gold (top 12):', ' '.join(f'[{feats[i]}]{contrib[i]*1000:+.2f}' for i in order[:12]))
print('B verder van gold (top 12):', ' '.join(f'[{feats[i]}]{contrib[i]*1000:+.2f}' for i in order[-12:][::-1]))
# zelfde uitsplitsing voor MFW
feats_w = J.top(J.toks(J.real), 100); zw = J.FAM['MFW']; cw = [0.0] * 100
for nr in G:
    zg, za, zb = zw(G[nr]), zw(final[('A', nr)]), zw(final[('B', nr)])
    for i in range(100): cw[i] += (abs(za[i] - zg[i]) - abs(zb[i] - zg[i])) / 100 / 12
ow = sorted(range(100), key=lambda i: -cw[i])
print('MFW, A verder (top 8):', ' '.join(f'{feats_w[i]}{cw[i]*1000:+.2f}' for i in ow[:8]))
print('MFW, B verder (top 8):', ' '.join(f'{feats_w[i]}{cw[i]*1000:+.2f}' for i in ow[-8:][::-1]))
