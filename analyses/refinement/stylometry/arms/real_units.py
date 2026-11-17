#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zet alle 74 losse echte verhalen mechanisch (pdftotext) in het gitignored
stylometry/raw/gold_all_*.txt, als echte vergelijkingseenheden voor arms/analyse.py.
Zelfde verhaalgrenzen als triad/select_gold.py. Print alleen bundel/pagina/woordtal.
Gebruik (vanuit analyses/refinement/):  python3 stylometry/arms/real_units.py <map met PDF's>
"""
import contextlib, io, subprocess, sys
sys.path.insert(0, 'stylometry/triad')
with contextlib.redirect_stdout(io.StringIO()):
    import select_gold as sg
n400 = 0
for i, s in enumerate(sg.sm, 1):
    dst = f"stylometry/raw/gold_all_{i:02d}_{s['bundle']}_p{s['start']:02d}.txt"
    subprocess.run(['pdftotext', '-nopgbrk', '-f', str(s['start']), '-l', str(s['end']), sg.pdf(s['bundle']), dst], check=True)
    n400 += s['words'] >= 400
print(f"{len(sg.sm)} verhalen geschreven; {n400} met >=400 woorden")
