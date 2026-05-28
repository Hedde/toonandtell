#!/usr/bin/env bash
# Regenereert het (gitignored, copyright) echte Tellegen-corpus voor de stylometrie-harness.
# Vereist: pdftotext (poppler) + de 4 bron-PDF's in ../../../../ (buiten de repo).
# Draai vanuit analyses/refinement/.
set -e
PDFDIR="${1:-/Users/heddevanderheide/Projects/ICTU/readz}"
mkdir -p stylometry/raw
pdftotext -nopgbrk -f 5 -l 41 "$PDFDIR/Toon_Tellegen-Maar_niet_uit_het_hart.pdf" stylometry/raw/real_mnuhh.txt
pdftotext -nopgbrk -f 5 -l 40 "$PDFDIR/Toon_Tellegen-Met_hart_en_ziel.pdf"       stylometry/raw/real_mhez.txt
pdftotext -nopgbrk -f 5 -l 40 "$PDFDIR/Toon_Tellegen-Een_hart_onder_de_riem.pdf"  stylometry/raw/real_ehodr.txt
pdftotext -nopgbrk -f 5 -l 40 "$PDFDIR/Toon_Tellegen-Dank_je_wel.pdf"             stylometry/raw/real_djw.txt
echo "corpus geregenereerd in stylometry/raw/"
