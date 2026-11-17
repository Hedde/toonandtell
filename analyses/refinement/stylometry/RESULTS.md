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

---

## 8. Best-of-N + selectie — en CORRECTIE op §7 (eerst verifiëren)
Hypothese: genereer N vorm-gematchte (dialoog-gedreven) premisse-eerst kandidaten, selecteer op MFW-Delta, valideer op de held-out char3. n=8 (mol, egel, reiger, kreeft, das, uil, mees, slak).

**Harness-controle:** échte losse verhalen door `measure.py` → vergeetboek MFW 0,894 / char3 0,978; pinguïn MFW 0,824 / char3 0,763. Echte verhalen scoren dus laag (harness deugt); per-verhaal char3-bereik ~0,76–0,98.

**Kandidaten:** MFW 0,82–0,98; char3 **1,05–1,30** — álle boven het echte bereik. MFW-beste = uil (0,824) maar char3 1,088. Pearson r(MFW,char3)=0,40 (zwak).

Bevindingen — **correctie op §7:**
- **Best-of-N + MFW-selectie sluit de gap niet.** Selectie op MFW transfereert nauwelijks naar char3 (r=0,40); de MFW-beste blijft op char3 ver buiten het echte bereik.
- **char3 (karakter-trigram) is de discriminerende vingerafdruk**, niet MFW. AI clustert op char3 ≥1,05; echt ≤0,98. Dialoog-vorm verwijdert die gap NIET (n=8).
- **De arm-B-uitkomst uit §7 (char3 0,914 "binnen") repliceert niet** — dat was een n=1-uitschieter. MFW is bovendien een zwakke discriminator (AI en echt overlappen), dus "binnen de MFW-spreiding" is zwak bewijs.

**Netto, gecorrigeerd:** geen van de geteste prompt/proces-hefbomen (premisse, vorm, best-of-N-selectie) sluit de karakter-niveau-vingerafdruk betrouwbaar. De diepe vingerafdruk persisteert — consistent met de literatuur; alleen modelniveau-ingrepen (fine-tunen) zijn geïndiceerd. Wat de prompt/proces-laag wél oplevert is een betere léésindruk, geen stylometrische convergentie. (Bewaard: de 8 kandidaten als leesbaar materiaal; char3 + harness als gevalideerde maat. Vervallen als gap-closer: best-of-N en de n=1-vorm-claim.)

---

## 9. Constraints-in-de-agent vs per-tekst-surgery — de balans (bewezen)

**(a) Iteratieve surgical loop** (mees; char3 = held-out): r0 MFW 0,931 / char3 1,140 → r1 0,906 / 1,016 → r2 0,914 / 1,072. Eén data-gedreven pas helpt (óók de held-out char3), de tweede plateaut/regresseert. Surgery = één corrigerende pas, geen monotone optimizer.

**(b) Systematiek over 16 AI-teksten** (gem. z + richting-consistentie): consistent (≥80%) te vaak `was/niet/dan/nu`, te zelden `in/zijn/uit` (+ komma-overmaat, lage TTR) = systematisch → constraint. Wisselend per tekst (`zei/het/daar/naar`) = idiosyncratisch → surgery.

**(c) Constraints in de agent** (systematische bevindingen als register-richtlijnen). Baseline ZONDER surgery (echt: MFW mean 0,765/max 0,945; char3 per-verhaal ~0,76–0,98):

| tekst | MFW | char3 (held-out) |
|---|---|---|
| niet-constrained best-of-N (8, gem.) | 0,917 | 1,118 |
| eekhoorn | 0,937 | 0,823 |
| mier | 0,765 | 0,827 |
| beer | 0,800 | 0,907 |
| **reiger** (confound-controle, zelfde dier) | 0,952 → **0,795** | 1,296 → **0,896** |
| **kreeft** (confound-controle, zelfde dier) | 0,903 → **0,677** | 1,085 → **0,825** |

**Uitkomst:** constraints brengen de baseline op béíde families binnen het echte bereik — inclusief de held-out char3 — reproduceerbaar (5 teksten char3 0,82–0,91) en óók bij identieke exotische dieren (animal-confound uitgesloten). Teksten blijven goed leesbaar. Sterkste positieve hefboom van het project; het corrigeert de eerdere "geen enkele prompt/proces-hefboom sluit de gap".

**De balans (bewezen):** systematische, terugkerende afwijkingen → **constraint in de agent** (groot, goedkoop, generaliseert); idiosyncratische rest → hooguit **één** surgical pass. Constraints doen het zware werk, surgery is marginale opschoning.

**Terughoudendheid:** twee feature-families (MFW + char-3-gram), onze eigen harness, n klein (5), één auteur; constraints afgeleid van diezelfde auteur (char3 wél held-out van de ingreep). Een getrainde neurale/perplexiteits-detector, menselijke lezers en andere auteurs zijn niet getoetst. "Binnen ons stylometrische bereik" is niet "ononderscheidbaar". Generieke toepasbaarheid vergt meer empirisch werk (zie `PROTOCOL.md`).

---

## 10. Model-vergelijking (4.8 vs 4.6 vs 4.5 vs Codex; N=4 per model, taak constant)
Zelfde taak (premisse-eerst + dialoog + register-constraints) en dezelfde 4 dieren (eekhoorn/mier/kreeft/mus); alleen het schrijfmodel varieert. Claude 4.7 was hier niet beschikbaar. Codex is toegevoegd als extra arm, maar niet blind/schoon: de agent had de harness en eerdere resultaten in context.

| model | MFW-Delta | char3-Delta (held-out) | komma/100 | TTR |
|---|---|---|---|---|
| **Opus 4.8** | 0,870 | **0,906** | 6,2 | 0,45 |
| Codex | 0,921 | 1,051 | 4,5 | 0,44 |
| Sonnet 4.6 | 0,859 | 1,117 | 5,3 | 0,43 |
| Haiku 4.5 | 1,024 | 1,105 | 5,0 | 0,43 |
| echt (ref) | 0,765 (max 0,945) | ~0,78 (per-verhaal 0,76–0,98) | 5,6 | 0,50 |

**Bevinding:** op de discriminerende held-out char-3-gram ligt **Opus 4.8 het dichtst bij Tellegen** (0,906, grotendeels binnen het echte bereik). Codex komt daarna (1,051): buiten het echte max-bereik, maar dichterbij dan Sonnet 4.6 (1,117) en Haiku 4.5 (1,105). Op MFW zijn 4.8 en 4.6 het sterkst; Codex zit daarachter maar vóór Haiku. Eerste *meetbare* indicatie van een modelbijdrage: het nieuwere/grotere Claude-model schrijft dichter bij de doelstijl op de scherpst onderscheidende vingerafdruk; Codex levert in deze niet-blinde arm geen verbetering op t.o.v. Opus 4.8.

**Voorbehoud:** N=4/model, één taak, één auteur, twee families, onze eigen harness; de register-constraints zijn deels afgeleid van 4.8-output (mogelijk mild in 4.8's voordeel). De Codex-arm is extra besmet: dezelfde sessie kende de meetopzet en de eerdere uitkomsten, dus dit is hooguit een praktische Codex-proef, geen eerlijke black-box benchmark. Indruk, geen ranglijst-bewijs; 4.7 ontbreekt. Een schone meting vraagt om meer N, meerdere taken/auteurs, een getrainde detector, menselijke raters en rolscheiding tussen schrijver en analist (PROTOCOL.md §8).

---

## 11. Gold-triad: volledige schrijfagent vs kale variant (n=12, vooraf vastgelegd)

**Datum:** 2026-11-17. **Vraag:** schrijft de volledige `toon-tellegen-schrijver` (429 regels, 27 skills) dichter bij Tellegen dan een kale variant met alleen premisse-eerst, temporeel register en register-constraints?

**Opzet.** 12 echte verhalen als gold (3 per bundel, 354–580 woorden, mechanisch gekozen met `triad/select_gold.py`; uit: wat de agent-prompt citeert of oproept en wat in eerdere blindtests zat). Per gold schreef een aparte agent een inhoudsbrief uit de PDF; alle 12 delen geen reeks van ≥5 woorden met hun gold (`triad/check_brief.py`; 4-gram-overlap ≤0,9%).
Per brief twee concepten met hetzelfde model (`claude-opus-5-5`), elk in een schone context met alleen system prompt + brief: **A** = de volledige agent-body, **B** = regels 15–44 van dezelfde prompt (`triad/arm_B_system.md`). Geen review, geen surgery, geen selectie op kwaliteit.
Rechter: `triad.py` (afstand tot het gold, MFW + char3). Opzet en beslisregel zijn gecommit vóór het eerste concept bestond (`e0c390c`).

**Beslisregel (vooraf).** Alleen een bevinding als één arm op béíde families wint met tweezijdige tekentoets p<0,05 (n=12: ≥10 van 12). Alles daaronder = geen aantoonbaar verschil.

### Gemeten

| # | gold | woorden gold / A / B | MFW A | MFW B | win | char3 A | char3 B | win | gold-echo A / B |
|---|---|---|---|---|---|---|---|---|---|
| 01 | djw p38 | 363 / 398 / 380 | 0,548 | 0,551 | A | 0,634 | 0,635 | A | 13,1% / 12,6% |
| 02 | djw p24 | 416 / 473 / 438 | 0,649 | 0,566 | B | 0,719 | 0,671 | B | 12,7% / 6,8% |
| 03 | djw p35 | 480 / 519 / 524 | 0,474 | 0,452 | B | 0,585 | 0,543 | B | 17,1% / 14,1% |
| 04 | ehodr p34 | 374 / 402 / 402 | 0,595 | 0,557 | B | 0,671 | 0,663 | B | 14,2% / 11,9% |
| 05 | ehodr p13 | 455 / 496 / 498 | 0,655 | 0,565 | B | 0,747 | 0,654 | B | 4,6% / 1,6% |
| 06 | ehodr p24 | 530 / 604 / 588 | 0,458 | 0,461 | A | 0,648 | 0,613 | B | 9,6% / 13,8% |
| 07 | mnuhh p12 | 354 / 395 / 357 | 0,633 | 0,600 | B | 0,745 | 0,727 | B | 3,0% / 9,2% |
| 08 | mnuhh p32 | 436 / 451 / 457 | 0,590 | 0,506 | B | 0,664 | 0,578 | B | 6,7% / 8,3% |
| 09 | mnuhh p14 | 439 / 469 / 461 | 0,620 | 0,620 | A (<0,001) | 0,741 | 0,655 | B | 2,8% / 3,5% |
| 10 | mhez p09 | 430 / 435 / 484 | 0,524 | 0,710 | A | 0,792 | 0,787 | B | 3,0% / 1,9% |
| 11 | mhez p35 | 466 / 530 / 508 | 0,476 | 0,474 | B | 0,558 | 0,520 | B | 7,2% / 18,5% |
| 12 | mhez p13 | 580 / 676 / 651 | 0,565 | 0,531 | B | 0,578 | 0,598 | A | 4,0% / 7,1% |

*Gold-echo = aandeel van de woorden van het concept dat in een letterlijke reeks van ≥8 woorden uit het eigen gold valt (`triad/gold_echo.py`).*

**Winstpercentages.** MFW: A wint 4/12 (33%), B 8/12, p=0,388. char3: A wint 2/12 (17%), B 10/12, **p=0,039**. Beide families eens: A 1, B 7, verdeeld 4. Gemiddelde afstand tot het gold: MFW A 0,566 / B 0,549; char3 A 0,673 / B 0,637. Vier (MFW) en drie (char3) triades zijn beslist met een marge <0,01. De p van 0,039 is fragiel; zie de zelftoets onderaan.

**Afstand tot het corpus-profiel (`measure.py`, gemiddeld over 12):**

| arm | MFW-Delta | char3-Delta | komma/100 | TTR |
|---|---|---|---|---|
| A volledige agent | 0,728 (sd 0,059; 0,66–0,88) | 0,786 (sd 0,078; 0,63–0,91) | 5,2 | 0,52 |
| B kale variant | 0,744 (sd 0,066; 0,63–0,87) | 0,793 (sd 0,091; 0,65–0,95) | 4,0 | 0,51 |
| echt (ref) | 0,765 (max 0,945) | 0,779 (max 0,940) | 5,6 | 0,50 |

A ligt dichter bij het profiel dan B in 6/12 (MFW) en 7/12 (char3) paren. Beide armen liggen op het echte gemiddelde; alleen B_07 (char3 0,946) valt net boven het echte maximum.

**Controles.**
- **Lengte.** Alle 24 concepten zijn langer dan hun gold: A gemiddeld +9,6%, B +7,6%. De lengtepoort (±15%, hooguit 3 pogingen, vooraf vastgelegd) zette 8 concepten ongemeten opzij (A 6, B 2; `triad/generation_log.tsv`). A_12 bleef na drie pogingen op +16,6% en is zo meegenomen: één concept buiten de marge.
- **8-gram-overlap met het corpus: de controle faalt.** Alle 24 concepten delen 8-grams met het corpus (0,2–7,6%; A gem. 2,9%, B 3,5%), vrijwel uitsluitend met het éígen gold (rest van het corpus gemiddeld <0,1%, hoogstens 1,0%). Per concept gemiddeld bijna vier letterlijke reeksen van ≥8 woorden, de langste 19 (A) en 21 (B) woorden; samen 8,2% (A) en 9,1% (B) van de tekst, uitschieters tot 18,5%. In 64 van de 91 reeksen staat minstens één inhoudswoord dat nergens in de brief voorkomt.
- **Positieve controle van de rechter** (vóór de meting gedraaid, `triad/manifest_control.tsv`): een ánder echt Tellegen-verhaal tegenover een oud niet-constrained AI-verhaal uit §8. Het echte verhaal wint op char3 9/12 (p=0,146) en op MFW 4/12 (p=0,388). Volgens de beslisregel hierboven is dus zelfs echt-tegen-oud-AI geen bevinding. Inhoud was hier niet gelijkgetrokken (afstanden 0,84–1,53 tegen 0,45–0,79 in het experiment).
- **`triad.py` zelf.** Draait foutloos op het echte corpus, is herhaalbaar (twee runs identiek) en volgorde-onafhankelijk (armen omgewisseld geeft gespiegeld 8/12 en 10/12 met dezelfde p). Eén afwijking, niet gerepareerd: de MFW-lijst verschilt in 1 van de 100 woorden van `measure.py`. Op rang 100 staan `we` en `mij` gelijk (47×); `measure.py` sorteert alleen op frequentie en houdt `we`, `triad.py` sorteert bij gelijkstand alfabetisch en houdt `mij`. De char3-lijst is identiek.

### Afgeleid

- **Geen aanwijzing dat de volledige agent dichter bij Tellegen schrijft.** De richting wijst eerder naar de kale variant (op beide families gemiddeld dichter bij het gold), maar alleen char3 haalt de drempel. Op het corpus-profiel zijn de armen gelijk.
- **De ruim 380 regels buiten de drie secties leveren op deze twee families niets meetbaars op.** Dat is smaller dan "de gids is overbodig": de brief legt dieren, premisse en verloop vast, dus alles wat de volledige prompt doet aan premisse-keuze, architectuur en slot kan hier niet meetellen. Gemeten is alleen het register op zinsniveau.
- **De triade meet deels reproductie van het origineel.** De letterlijke reeksen staan niet in de briefs en komen in beide armen voor. Ze komen dus óf uit het geheugen van het model, óf uit een brief die zo gedetailleerd is (582–834 woorden, langer dan de verhalen zelf) dat de eenvoudigste Tellegen-zin samenvalt met de echte. Deze opzet kan die twee niet scheiden. De echo is over de armen ongeveer gelijk en de arm met de meeste echo wint char3 in 6/12 triades; hij verklaart de richting dus niet, maar maakt "afstand tot het gold" een onzuivere stijlmaat.
- **Het instrument is bij n=12 zwak.** De positieve controle haalt de regel niet. "Geen aantoonbaar verschil" betekent hier daarom "niet aangetoond", niet "aangetoond gelijk".

**Terughoudendheid.** n=12, één model, één auteur, twee families, eigen harness. Eén concept per cel: de variatie tussen twee runs van dezelfde arm is niet gemeten en kan even groot zijn als het verschil tussen de armen. Het gold zit ook in het referentiecorpus waarop gestandaardiseerd wordt (klein effect, beide armen gelijk). A is gemiddeld iets langer dan B. De agent-prompt ging als system prompt de CLI in (`claude -p --safe-mode`), niet als geregistreerde subagent; de CLI voegt aan beide armen hetzelfde omgevingsblok toe. Het user-bericht schreef voor beide armen enkele aanhalingstekens voor, omdat quote-trigrammen in de char3-top-300 zitten. De 24 concepten bevatten door de gold-echo letterlijke bronfragmenten en staan daarom alleen lokaal (`triad/A_*.txt`, `triad/B_*.txt`), niet in git.

**Uitkomst.** Geen aantoonbaar verschil volgens de vooraf vastgelegde regel: de kale variant won op char3 10/12 (p=0,039) maar op MFW slechts 8/12 (p=0,388), dus de volledige agent schrijft op deze maten niet aantoonbaar dichter bij Tellegen dan de kale.

**Vervolgvoorstel (niet uitgevoerd).** (1) Gold dat het model niet kan kennen, of grovere briefs (premisse plus drie stappen), zodat de echo verdwijnt. (2) Meerdere concepten per cel om de variatie binnen een arm te schatten. (3) Een arm "geen gids" en een tweede model, zoals bij Taylor/Every. (4) Arm B zonder de opmaakregels uit het user-bericht. (5) Dezelfde A/B-vergelijking op een taak met eigen premisse, beoordeeld door lezers. (6) Meer triades (n≥30) of een toets op de marges in plaats van alleen het teken. (7) De tie-break in `triad.py` en `measure.py` gelijktrekken.

### Zelftoets: is "de volledige agent helpt niet" een artefact van onze eigen opzet?

*Post hoc en verkennend, op bestaande teksten (`triad/selfcheck.py`). Verandert de beslisregel en de uitkomst niet.*

**Wat het cijfer opblies (eigen toedoen).** De enige p onder 0,05 in deze sectie hangt aan de lengtepoort, die ik zelf heb toegevoegd. Met de eerste poging van elke cel wint B op char3 9/12 (p=0,146) in plaats van 10/12; triade 04 slaat om op een marge van 0,008. Met de gold-echo gemaskeerd is het ook 9/12. Lees de char3-uitslag dus als "9 à 10 van 12", niet als p=0,039.

**Wat het resultaat níét verklaart.**

| mogelijke vertekening | toets | uitkomst |
|---|---|---|
| lengte (A is langer) | verband lengteverschil ↔ afstandsverschil; alleen lengte-gelijke triades | geen stabiel verband (MFW r=+0,63, zonder triade 10 −0,17); in 9 lengte-gelijke triades wint B char3 7–2, MFW 6–3 |
| gold-echo | letterlijke reeksen uit beide concepten geknipt | richting gelijk: char3 B 9–3, MFW B 8–4; gem. afstand A 0,625/0,731, B 0,609/0,699 |
| de prompt verbiedt woorden die in het gold staan | tellingen gold / A / B | verwaarloosbaar: `thee` 2/2/2, `drempel` 1/2/4, `verdween` 3/0/2 |
| typografie | aandeel leesteken-trigrammen in het char3-verschil | 18% (0,006 van 0,036); de rest is verspreid over 272 letter-trigrammen |

**Ruis.** Acht afgekeurde pogingen geven een tweede concept van dezelfde arm op dezelfde brief (6×A, 2×B, alle >15% te lang). Op MFW is het verschil binnen een arm (mediaan 0,039) even groot als tussen de armen (0,034): de MFW-uitslag draagt geen informatie. Op char3 is het verschil tussen de armen (mediaan 0,037) ruwweg vier keer zo groot als binnen een arm (0,009; gem. 0,017); van de 9 triades met een marge boven die ruisvloer wint B er 8. De char3-richting is dus waarschijnlijk geen toeval, al rust de ruisschatting op acht paren.

**Wat de opzet niet kán zien (het werkelijke risico).**
- *De maatlat is die van arm B.* De register-constraints zijn in §9 afgeleid van precies deze twee families. De overige regels van de prompt zijn afgesteld op leesindruk in de blindtests. Dat ze MFW en char3 niet verder bewegen, is bijna per constructie zo.
- *De brief schakelt de rest van de prompt uit.* Premisse, verloop en slot liggen vast, en de briefs zijn door mijn instructie uitputtend. Waar de volledige agent voor bedoeld is, kan niet meedoen.
- *"Dichter bij het gold" is niet "dichter bij Tellegen".* Op het corpus-profiel zijn de armen gelijk. B hergebruikt iets meer van het gold-vocabulaire (56,5% tegen 53,7% van de inhoudswoorden; A hoger in 4/12). De maat straft dus afwijken van het origineel, en daar stuurt de volledige prompt juist op.
- *Het user-bericht gaf B een deel van de gids cadeau:* geen titel, geen opmaak, enkele aanhalingstekens, doellengte. Dat verkleint het gat tussen de armen; hoeveel is niet getoetst.
- *Ander model dan waarop de prompt is afgesteld* (Opus 5.5 in plaats van 4.8).

**Oordeel.** "De volledige agent schrijft slechter" is niet gedekt: dat zou een vals signaal zijn, gebouwd op een fragiele p en op een maat die origineel-trouw beloont. "De volledige agent schrijft op deze maten niet dichterbij" blijft staan; geen enkele toets zette A voor. Verder reikt het niet: over de verbetering waarvoor de gids is gemaakt (premisse, opbouw, leesindruk) zegt deze meting niets.
