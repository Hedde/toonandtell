# Blindtest 7 — sleutel (NIET aan panel tonen)

Datum: 2026-05-28

## Mapping blindtest 1

| Positie | Verhaal | Bron | Echt/AI |
|---------|---------|------|---------|
| A | mier & eekhoorn, "vergeetboek" | *Maar niet uit het hart* p.5-6 | ECHT |
| B | karper & snoek | toon-tellegen-schrijver (opus) | **AI** |
| C | grauwe gans / watertaart | *Met hart en ziel* p.5-6 | ECHT |
| D | pinguïn verjaardag in de storm | *Een hart onder de riem* p.26-27 | ECHT |

Panel 1 (ex toon-fan): linguist-nederlands, neerlandicus-afgestudeerd, redacteur-uitgeverij.

Bestanden: `panel/verhaal_{A,B,C,D}.pdf` (neutrale namen, gelijk format).
Let op: AI-PDF is monospace, echte zijn serif-boekletter — typografie is ruis, panel hierop geïnstrueerd.

## Mapping blindtest 2 (na revisie, nieuw panel, herhaalde randomisatie)

| Positie | Verhaal | Bron | Echt/AI |
|---------|---------|------|---------|
| A | karper & snoek **v2 (herzien)** | toon-tellegen-schrijver | **AI** |
| B | pinguïn | *Een hart onder de riem* p.26-27 | ECHT |
| C | mier & eekhoorn, "vergeetboek" | *Maar niet uit het hart* p.5-6 | ECHT |
| D | grauwe gans / watertaart | *Met hart en ziel* p.5-6 | ECHT |

Zelfde drie echte verhalen als controle. Panel 2 = verse instanties linguist/neerlandicus/redacteur.
Bestanden: `panel2/verhaal_{A,B,C,D}.pdf`.

## Mapping blindtest 3 (ronde 3: typografie volledig genormaliseerd)

Alle vier teksten door identieke pijplijn: pdftotext -> normalize.py (rechte quotes, uniforme spatiëring, alinea's hersteld, hoofdletter begin) -> cupsfilter. Geen typografie/leesteken-verschil meer.

| Positie | Verhaal | Bron | Echt/AI |
|---------|---------|------|---------|
| A | mier & eekhoorn, "Ik moet op reis" | *Maar niet uit het hart* p.7-8 | ECHT |
| B | mier & eekhoorn, "vergeetboek" | *Maar niet uit het hart* p.5-6 | ECHT |
| C | pinguïn | *Een hart onder de riem* p.26-27 | ECHT |
| D | karper & snoek **v3 (2e revisie)** | toon-tellegen-schrijver | **AI** |

Watertaart vervangen (ingesloten brief liet zich niet schoon auto-normaliseren).
Bestanden: `round3/panel3/verhaal_{A,B,C,D}.pdf`. Panel 3 = verse instanties linguist/neerlandicus/redacteur.
