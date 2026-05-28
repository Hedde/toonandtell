# Stylometrie + plagiaat-audit — resultaten (pilot)

**Datum:** 2026-05-28. Pure-Python harness (`stylometry.py`), copyright-veilig (bron-tekst lokaal; alleen metrics hieronder).

**Opzet.** Echt corpus: ~31.660 woorden uit de 4 bundels (inhoudspagina's), 69 samples van ~450 woorden. AI premisse-eerst (n=5: zeekomkommer, olifant, wielewaal, wesp, zeearend) vs AI thema-eerst (n=5: karper, spitsmuis, krekel, karper-gemis, oud-worden). Maten: Burrows'-achtige Delta (gem.|z| over 100 MFW, gestandaardiseerd op het echte corpus), nearest-neighbour-Delta, lexicale/burstiness-features, en verbatim n-gram-overlap.

## 1. Delta tot Tellegen-profiel (MFW)
- ECHT-spreiding: 0,765 ± 0,069 (0,615–0,945).
- premisse-eerst gemiddeld **0,850**; thema-eerst **0,869**. Verschil **0,019** — ruim binnen de ruis (≪ sd 0,069).
- Beide AI-groepen liggen ~1 sd boven het echte gemiddelde, grotendeels binnen de natuurlijke spreiding; één uitschieter (wielewaal, +3,1 sd).

→ **Premisse-eerst is stylometrisch niet dichter bij Tellegen dan thema-eerst.** Het in de blindtests gevonden voordeel zit in de *leesindruk*, niet in de function-word-vingerafdruk.

## 2. Nearest-neighbour (MFW)
ECHT→dichtstbijzijnde echte: 0,808 (max 0,987). Alle AI-teksten hebben een echte buur op Delta 0,79–0,94 — binnen het echte NN-bereik. Een naïeve NN-MFW-test scheidt onze AI dus niet van Tellegen. **Caveat:** dit is géén geldige discriminatietest (geen contrast-auteur, geen getrainde classifier, kleine n) en weerlegt de literatuur niet.

## 3. Lexicale / burstiness-features (groepsgemiddelden)
| groep | zinsl. gem | zinsl. sd | burstiness CV | TTR300 | hapax300 | woordlengte | komma/100w |
|---|---|---|---|---|---|---|---|
| ECHT | 12,73 | 8,40 | 0,66 | 0,50 | 0,34 | 4,20 | **5,60** |
| premisse | 13,18 | 9,03 | 0,68 | 0,46 | 0,30 | 4,03 | **7,87** |
| thema | 13,16 | 8,15 | 0,62 | 0,46 | 0,30 | 3,94 | **7,29** |

Bevindingen:
- **Zinslengte/burstiness:** AI ≈ Tellegen — géén grotere uniformiteit hier (premisse zelfs iets bursty-er). De verwachte "vlakheid" toont zich niet op deze maat.
- **Concrete, blijvende AI-tells, identiek in beide modi:** komma-overgebruik (~7,5 vs 5,6 = +34%), iets lagere lexicale diversiteit (TTR 0,46 vs 0,50; hapax 0,30 vs 0,34), kortere woorden. **Premisse-eerst repareert deze niet.**

## 4. Verbatim-overlap (plagiaat-audit)
- 8-gram-overlap met het corpus ≈ **0%** (één geval 0,2%); 5-gram 0–1,7%.
- Langste gedeelde reeksen: 5–6 generieke woorden ("hij keek om zich heen", "terwijl de zon onderging en de", "hij wist niet wat hij").
- **Eén 8-woord-collisie** (AI-karper, blindtest7): *"dat geeft niet zei de karper de snoek"* — geverifieerd aanwezig in het echte corpus. Oorzaak: de stockfrase *"Dat geeft niet"* + de canonieke personages karper/snoek die Tellegen zelf samen gebruikt. Geen overname van distinctieve expressie, maar wél een eerlijk te melden drift naar bestaande tekst op één punt.

→ **Geen plagiaat:** overlap op het niveau van veelvoorkomende function-word- en stockfrasen, niet van eigen Tellegen-formuleringen. Voldoet aan het criterium uit `PROTOCOL.md` (hoge stijlgelijkenis + verwaarloosbare tekstoverlap).

## 5. Conclusie van de pilot
1. **De stylometrie ontkracht de sterke lezing van de "doorbraak".** Premisse-eerst verandert de leesindruk, niet de forensische vingerafdruk; meetbare tells (komma's, lexicale diversiteit) blijven en zijn gelijk in beide modi. Een getrainde classifier zou AI waarschijnlijk nog steeds scheiden. Dit **strookt met** de geciteerde literatuur (surface/architectuur ≠ diepe vingerafdruk).
2. **Het werk is in de kern niet-plagiërend** (één stockfrase-collisie eerlijk gemeld).
3. **Caveats:** kleine n (5/groep), één corpus-deelverzameling, MFW=100, geen contrast-auteur, geen getrainde classifier, geen significantietoets. Dit is een pilot, geen vervanging van het volledige ontwerp in `PROTOCOL.md` (menselijke raters, ROC, getrainde stylometrie, meer trials).

**Netto:** op de maatlat die het vakgebied hanteert hebben we **geen** verbetering aangetoond; ons enige gefundeerde resultaat blijft (a) een reader-impression-strategie en (b) dat LLM-jury's onbetrouwbare detectoren zijn. De stylometrie-pilot maakt dat scherper, niet rooskleuriger.

---

## 6. Fingerprint-in-the-loop: werkt kennis van de vingerafdruk?
Test of we, nu we de tells kennen, het proces kunnen aanscherpen tot lagere stylometrische afstand. Anti-Goodhart-waarborg: een **held-out** vingerafdruk (karakter-3-gram-Delta) die de ingreep niet direct kon targeten (`measure.py`).

Twee ingrepen op 3 premisse-eerste teksten:
- **A — mechanische komma-fix** (komma-rate → Tellegens 5,6/100w).
- **B — holistische herziening** door de schrijfagent richting Tellegens gemeten profiel (minder komma's, meer woordvariatie, gevarieerde zinslengte).

| tekst | MFW-Delta | char3-Delta | komma/100 |
|---|---|---|---|
| echt (ref) | 0,765 (max 0,945) | 0,779 (max 0,940) | 5,6 |
| zeekomkommer basis → A → B | 0,843 → 0,843 → 0,840 | 1,007 → 1,001 → 0,992 | 7,1 → 5,6 → 3,9 |
| olifant basis → A → B | 0,828 → 0,828 → 0,851 | 0,848 → 0,840 → 0,854 | 9,1 → 5,7 → 4,7 |
| wielewaal basis → A → B | 0,978 → 0,978 → 0,901 | 1,116 → 1,116 → 1,069 | 8,2 → 5,7 → 3,8 |

**Uitkomst: het werkt niet.**
- Komma-fix raakt het doel exact maar laat MFW-Delta **ongewijzigd** (0 verandering) en char3-Delta nauwelijks → één feature is niet de vingerafdruk; dit is Goodhart-gaming.
- Holistische herziening beweegt beide vingerafdrukken verwaarloosbaar en inconsistent (olifant zelfs slechter; wielewaal iets beter maar char3 blijft ver boven de echte max). Geen convergentie.

**Conclusie:** de stylometrische afstand reflecteert de output-distributie van het model, niet de oppervlaktekeuzes die ons proces kan bijsturen. Kennis van de vingerafdruk levert via prompting/herziening **geen** scherper stylometrisch resultaat — consistent met de literatuur. Het sluiten van de gap zou ingrepen op modelniveau vergen (fine-tuning/DPO op een discriminator), buiten dit project.

---

## 7. Vervolg: oppervlakte-chirurgie vs vorm-matching (waarom de loop wél/niet werkt)
Diagnose (`diag.py`) toonde dat de grootste MFW-afwijkingen van de zeekomkommer STRUCTUREEL/vorm-gedreven zijn, niet oppervlakte-tics: `zei`=0 (geen dialoog; Tellegen 14,6/1000), `het` veel te vaak, `de` veel te zelden, `was`/`werd` te vaak — kenmerken van een solo-descriptieve modus i.p.v. Tellegens dialoogvorm.

Twee chirurgie-armen op de zeekomkommer (echt: MFW 0,765/max 0,945; char3 0,779/max 0,940):

| arm | MFW-Delta | char3-Delta (held-out) |
|---|---|---|
| basis | 0,843 | 1,007 |
| A — functiewoord-chirurgie (het→de, minder was/werd; vorm ongemoeid) | **0,906** (slechter) | 1,006 (onveranderd) |
| B — vorm-matching (dialoog toegevoegd, premisse behouden) | **0,755** | **0,914** |

- **Arm A faalt en verergert.** Functiewoorden lokaal forceren duwt andere features uit balans (whack-a-mole over 100 gecorreleerde dimensies) en raakt de structurele afwijking (zei=0) niet. Held-out char3 beweegt niet → geen vooruitgang.
- **Arm B werkt echt.** Tellegens VORM matchen (dialoog-gedreven) bracht béíde vingerafdrukken binnen de Tellegen-spreiding; de niet-getargete char3 volgde mee → genuine convergentie, geen Goodhart.

**Conclusie (verfijning van §6).** Een chirurgie/review-lus kan wél stylometrische vooruitgang boeken — maar alleen door de **compositievorm** te matchen (hier: dialoogdichtheid), niet via oppervlakte-woordkeuze. De vingerafdruk wordt gedomineerd door vorm. Kosten/voorbehoud: vorm-matching = convergeren naar Tellegens dialoog-mal (de solo-deadpan vorm-eigenheid verdwijnt), gevalideerd op n=1 en twee feature-families; een neurale/perplexiteits-detector kan nog steeds scheiden.
