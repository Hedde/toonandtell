#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Positieve controle voor triad.py (instrument-check, GEEN onderdeel van de beslisregel).
Kan de rechter een bekend verschil zien? Per gold-verhaal:
  A = een ANDER echt Tellegen-verhaal (geschikt maar niet als gold gekozen),
  B = een oud, niet-constrained AI-verhaal uit deze repo (char3 >= 1,05 in RESULTS §8).
Verwachting als het instrument werkt: A (echt) wint ruim, vooral op char3.
Inhoud is hier NIET gelijkgetrokken (geen gedeelde brief); dit toetst alleen gevoeligheid.

Koppeling (vast, vooraf): de niet-gekozen geschikte verhalen op (bundel, pagina), de
eerste 12, in omgekeerde volgorde tegenover gold 01..12; de AI-teksten alfabetisch
uit bestofn/ (8), ai_premise/ (3) en ai_theme/ (eerste 1).
Gebruik (vanuit analyses/refinement/):  python3 stylometry/triad/control.py <map met PDF's>
"""
import contextlib, glob, io, subprocess, sys
sys.path.insert(0, 'stylometry/triad')
with contextlib.redirect_stdout(io.StringIO()):
    import select_gold as sg                       # zelfde verhaalgrenzen en uitsluitingen

chosen = {(s['bundle'], s['start']) for s in sg.sel}
order = {'djw': 0, 'ehodr': 1, 'mnuhh': 2, 'mhez': 3}
rest = sorted((s for s in sg.pool if (s['bundle'], s['start']) not in chosen),
              key=lambda s: (order[s['bundle']], s['start']))[:12][::-1]
ai = (sorted(glob.glob('stylometry/bestofn/*.txt')) + sorted(glob.glob('stylometry/ai_premise/*.txt'))
      + sorted(glob.glob('stylometry/ai_theme/*.txt'))[:1])
gold = [l.split('\t')[4].strip() for l in open('stylometry/triad/gold.tsv', encoding='utf-8') if not l.startswith('#')]
assert len(rest) == len(ai) == len(gold) == 12
with open('stylometry/triad/manifest_control.tsv', 'w', encoding='utf-8') as f:
    f.write('# gold\tA = ander echt verhaal (gitignored)\tB = oud niet-constrained AI-verhaal\n')
    for i, (g, s, a) in enumerate(zip(gold, rest, ai), 1):
        dst = f"stylometry/raw/gold_ctrl_{i:02d}_{s['bundle']}_p{s['start']:02d}.txt"
        subprocess.run(['pdftotext', '-nopgbrk', '-f', str(s['start']), '-l', str(s['end']), sg.pdf(s['bundle']), dst], check=True)
        f.write(f'{g}\t{dst}\t{a}\n')
        print(f"controle {i:02d}: gold {g.split('/')[-1]} | echt {s['bundle']} p{s['start']} ({s['words']}w) | AI {a.split('/')[-1]}")
