#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Controles en groepsgemiddelden voor de 24 triad-concepten (RESULTS §11). Wijzigt niets.
  1. lengte per concept t.o.v. het gold (marge +/-15%) + typografie (dubbele quotes, opmaak);
  2. verbatim-overlap met het corpus via overlap() uit stylometry.py (eis: 8-gram = 0);
  3. measure.py op alle 24 concepten -> gemiddelde afstand tot het corpus-profiel per arm.
Gebruik (vanuit analyses/refinement/):  python3 stylometry/triad/report.py
"""
import contextlib, io, re, statistics as st, subprocess, sys
sys.path.insert(0, 'stylometry')
with contextlib.redirect_stdout(io.StringIO()):
    import stylometry as S                         # voor load() en overlap()

T = 'stylometry/triad'
gold = [l.rstrip('\n').split('\t') for l in open(f'{T}/gold.tsv', encoding='utf-8') if not l.startswith('#')]
print('--- 1. lengte en typografie ---')
print('%-3s %5s | %5s %7s | %5s %7s | A-B%%  | dq(A,B) opmaak(A,B)' % ('nr', 'gold', 'A', 'afw', 'B', 'afw'))
dev = {'A': [], 'B': []}; bad = 0
for nr, _b, _p, w, _path in gold:
    n = int(w); row = {}
    for arm in 'AB':
        raw = open(f'{T}/{arm}_{nr}.txt', encoding='utf-8').read()
        k = len(S.toks(S.clean(raw))); d = 100 * (k - n) / n
        dev[arm].append(d); bad += abs(d) > 15
        row[arm] = (k, d, raw.count('"') + raw.count('“') + raw.count('”'), len(re.findall(r'[*#_`]|^---', raw, flags=re.M)))
    a, b = row['A'], row['B']
    print('%-3s %5d | %5d %+6.1f%% | %5d %+6.1f%% | %+5.1f | %d,%d %d,%d' % (nr, n, a[0], a[1], b[0], b[1], 100 * (a[0] - b[0]) / n, a[2], b[2], a[3], b[3]))
print('gem. afwijking A %+.1f%%  B %+.1f%%  | gem. |afw| A %.1f%%  B %.1f%%  | buiten 15%%: %d' % (
    st.mean(dev['A']), st.mean(dev['B']), st.mean(map(abs, dev['A'])), st.mean(map(abs, dev['B'])), bad))

print('\n--- 2. verbatim-overlap met het corpus (overlap() uit stylometry.py) ---')
worst = 0
for nr, *_ in gold:
    for arm in 'AB':
        f5, f8, longest, ex = S.overlap(S.load(f'{T}/{arm}_{nr}.txt'))
        worst = max(worst, f8)
        print(f'{arm}_{nr}  5-gram={f5:4.1f}%  8-gram={f8:3.1f}%  langste={longest}w: "{ex}"')
print('8-gram-overlap maximaal over 24 concepten: %.1f%%' % worst)

print('\n--- 3. measure.py: afstand tot het corpus-profiel ---')
args = [f'{arm}_{nr}={T}/{arm}_{nr}.txt' for nr, *_ in gold for arm in 'AB']
out = subprocess.run([sys.executable, 'stylometry/measure.py'] + args, capture_output=True, text=True).stdout
print(out.rstrip())
vals = {'A': [], 'B': []}
for line in out.splitlines():
    m = re.match(r'([AB])_(\d\d)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)', line)
    if m: vals[m.group(1)].append([float(x) for x in m.groups()[2:]])
print('\n%-22s %9s %11s %9s %7s' % ('arm (gem. over 12)', 'MFW-Delta', 'char3-Delta', 'komma100', 'TTR300'))
for arm, name in (('A', 'A volledige agent'), ('B', 'B kale variant')):
    c = list(zip(*vals[arm]))
    print('%-22s %9.3f %11.3f %9.1f %7.2f' % (name, *[st.mean(x) for x in c]))
    print('%-22s %9.3f %11.3f %9.1f %7.2f' % ('   sd', *[st.pstdev(x) for x in c]))
    print('%-22s %9s %11s' % ('   bereik', '%.2f-%.2f' % (min(c[0]), max(c[0])), '%.2f-%.2f' % (min(c[1]), max(c[1]))))
for j, name in ((0, 'MFW'), (1, 'char3')):
    less = sum(a[j] < b[j] for a, b in zip(vals['A'], vals['B']))
    print(f'{name}: A dichter bij het profiel dan B in {less}/12 paren (beschrijvend, geen toets)')
