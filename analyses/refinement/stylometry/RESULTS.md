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
