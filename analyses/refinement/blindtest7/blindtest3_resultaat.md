# Blindtest 7 — ronde 3 (2e revisie + typografie volledig genormaliseerd)

**Datum:** 2026-05-28
**Panel (vers, ex toon-fan):** linguist-nederlands, neerlandicus-afgestudeerd, redacteur-uitgeverij

## Wat er veranderde t.o.v. ronde 2
1. **Typografie genivelleerd.** Alle vier teksten door identieke pijplijn: `pdftotext` → `normalize.py` (rechte aanhalingstekens, uniforme spatiëring, herstelde alinea's, hoofdletter begin) → `cupsfilter`. Zelfde font, zelfde opmaak. Leestekens/spatiëring kunnen niets meer verklappen.
2. **2e revisie AI-verhaal** op de structurele ronde-2-tells: spiegel gebroken (snoek draagt geen parallelle last, is laconiek/hongerig), tonale wending toegevoegd, circulair slot vervangen.
3. Watertaart vervangen door "Ik moet op reis" (ingesloten brief liet zich niet schoon normaliseren).

## Scores

| Verhaal | Bron | Linguïst | Neerlandicus | Redacteur | Gemiddeld |
|---------|------|----------|--------------|-----------|-----------|
| A | op reis (MNUHH) — echt | 9 | 9 | 9 | **9,0** |
| B | vergeetboek (MNUHH) — echt | 8,5 | 9 | 8 | **8,5** |
| C | pinguïn (EHODR) — echt | 9,5 | 8,5 | 9 | **9,0** |
| D | karper & snoek **AI v3** | 4 | 5 | 5 | **4,7** |

**Detectie AI:** 3/3 correct (allen D). **Zekerheid:** 82% / 78% / 82% (gem. 80,7%).

## Nieuwe tells
- **Pathetic fallacy / spiegelende omgeving** (linguïst): "het water werd elke dag een beetje donkerder" — bij Tellegen is de wereld onverschillig, geen spiegel.
- **Te netjes geronde slotgedachte** (alle 3): "de zee die hij nooit zou zien... ook al was er niemand geweest om het te proeven" — dit is de nieuw toegevoegde slotzin van v3, die zelf een nieuwe "afgeronde samenvatting"-tell werd.
- **Afwezigheid van de absurde/komische knik** (neerlandicus, redacteur): D blijft van begin tot eind ernstig; geen moment waarop de ernst kantelt (vgl. mier "Doe toch kalm!", huis dat nooit bewoond was, pinguïn die "Een enkele keer!" vergeet).
- **Psychologische explicitering in dialoog**: "Iets dat je niet meer kwijt kunt" — te direct benoemd.

# Vergelijking over drie rondes

| Maat | R1 (origineel) | R2 (1e revisie) | R3 (2e rev. + genormaliseerd) |
|------|----|----|----|
| AI-score (gem.) | 4,3 | **5,7** | 4,7 |
| Detectie | 3/3 | 3/3 | 3/3 |
| Zekerheid | 79,3% | 74,0% | 80,7% |

## Conclusie
De typografie was **niet** de verklikker: met volledig genivelleerde opmaak bleef detectie 3/3 bij ~81% zekerheid. De 2e revisie (asymmetrie, tonale wending, ander slot) bracht ons **niet** dichterbij — sterker, de nieuwe slotzin creëerde een nieuwe "te afgeronde" tell, en de score zakte t.o.v. R2.

Het patroon over alle rondes bevestigt het structurele plafond: elke gerepareerde tell wordt vervangen door een diepere. Wat overblijft is geen losse fout maar een grondeigenschap van AI-imitatie — **te consistente ernst, te nette afronding, afwezigheid van de scheve knik**. De beste menselijke Tellegens scoren 8,5-9,5; de AI hangt rond 4,5-5,7 en blijft herkenbaar.

---

## Methodische verificatie (blindheid van het panel)
- Elke reviewer is een VERSE subagent: krijgt enkel zijn eigen systeemprompt + mijn taakprompt-string. Erft NIET mijn gesprek, de KEY, of de mapping.
- De taakprompt bevat alleen vier neutrale paden (`verhaal_A..D.pdf`) + instructie.
- Elke reviewer deed exact 4 tool-aanroepen = de 4 Reads. Geen `ls`, geen extra bestanden geopend (te zien aan tool_uses=4 per agent in alle 3 rondes).
- PDF-rendering is schoon: alleen verhaaltekst; PDF-metadata bevat geen Title/Author-lek (enkel "Quartz PDFContext").
- Posities zijn elke ronde opnieuw gerandomiseerd (AI = B, dan A, dan D); detectie bleef ~80% met genuanceerde, puur stilistische motivering en reële onzekerheid (72-82%) — gedrag dat een leak zou wegnemen.
- **Caveat:** sprekende bestandsnamen (`ai_karper_v3.txt`, `real_*.txt`) en `KEY.md` bestaan hoger in de boomstructuur. De panel-map (`panel3/`) bevat enkel de vier neutrale PDF's, en de agents navigeerden er niet heen — maar het was niet fysiek onmogelijk. Voor een ijzeren garantie: PDF's in een geïsoleerde map met opake namen, zonder sleutel in de buurt.
