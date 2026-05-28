# Rigoureuzer protocol — gegronde cijfers over AI-replicatie van Tellegen (zonder plagiaat)

Dit document beschrijft hoe de bevindingen uit `LEARNINGS.md` van *suggestief* naar *gegrond* gebracht kunnen worden. Het corrigeert de confounds die de huidige blindtests (1-9) onbetrouwbaar maken.

## 0. Zwaktes van de huidige opzet (te repareren)
- **Circulaire jury:** schrijver én beoordelaars zijn hetzelfde modelfamilie (Claude) → waarschijnlijke bias naar het authentiek-achten van eigen-model-output.
- **Onbetrouwbaar instrument:** het LLM-panel flagde echte Tellegens als AI en gaf identieke tekst tegengestelde oordelen tussen runs.
- **Geen stylometrie:** detectie was "lezen en gokken"; de literatuur-meetlat (Burrows' Delta, AMNP) is nooit gedraaid.
- **Zwakke opzet:** n=3 AI-verhalen, niet-geblindeerde experimentator, LLM-persona's i.p.v. mensen, reals uit boekcontext gehaald.
- **Geen plagiaat-audit:** nooit gemeten of "stijlimitatie" niet stiekem tekstovername is.

## 1. Definieer vier aparte constructen (meet ze los)
- **D — onderscheidbaarheid:** kunnen lezers AI van echt scheiden? (Turing/2AFC)
- **S — stylometrische afstand:** hoe dicht ligt de forensische vingerafdruk?
- **Q — kwaliteit:** hoe goed/mooi, los van auteurschap?
- **P — plagiaat/originaliteit:** hoeveel verbatim overlap met de bron?

"AI repliceert Tellegen" = hoge D-ononderscheidbaarheid **én** lage S-afstand **én** lage P-overlap (**én** acceptabele Q). Eén getal volstaat niet.

## 2. Steekproef & generatie
- Genereer **N ≥ 30-50** workflow-AI-verhalen met een vooraf vastgelegde, bevroren werkwijze/prompt.
- Trek **N ≥ 30-50** echte Tellegen-verhalen *at random* (pre-gespecificeerd; geen cherry-pick).
- Controle-arm: N naïef-prompt-AI (één-shot, geen werkwijze) als ondergrens.
- Identieke normalisatie/typografie op álle items (`normalize.py`).

## 3. Beoordelaars — fix de circulariteit
- **Primair: menselijke raters**, gespreid (naïef / Tellegen-bekend / experts-neerlandici). Power-analyse vooraf voor het aantal raters.
- LLM-juries enkel als **secundaire proxy** en dan **cross-model** (andere modelfamilie dan de schrijver), als ensemble, expliciet als ruis gerapporteerd — nooit als grondwaarheid.

## 4. Meetontwerp — signal detection, geen forced-choice
- **2AFC:** paar (1 echt, 1 AI), "welke is AI?" → % correct (kans = 50%) + d′.
- Of **per-item** ja/nee + confidence → ROC/AUC, sensitiviteit én specificiteit.
- **Controle/catch-items:** echt-vs-echt-paren en bekend-AI om false-positive-rate en raterbetrouwbaarheid te meten (dit ving onze gebroken detector niet).
- Inter-rater reliability (Krippendorff's α). Rapporteer effect sizes + 95% CI.
- "Ononderscheidbaar" = D **niet significant boven kans**, met CI — niet "0/3".

## 5. Stylometrische batterij (objectief, geen mens, copyright-veilig)
- Burrows' Delta op functiewoord-frequenties; char-n-gram-profielen; POS-n-grams; zinslengte-distributie & burstiness; perplexiteit onder een referentie-LM.
- Classifier (SVM/logistische regressie) AI-vs-echt met cross-validatie → **AUC**. Toets of premisse-eerst de "tight clustering" van AI (literatuurbevinding) verlaagt.
- **Copyright-veilig:** features lokaal berekenen; alleen geaggregeerde statistieken/AUC publiceren; tekst nooit herdistribueren; max. korte fair-use-citaten.

## 6. Plagiaat-/originaliteitsaudit (de kern van "zonder plagiaatschending")
Stijl is niet auteursrechtelijk beschermd; expressie wel. Maak het onderscheid meetbaar:
- Verbatim-overlap van elk gegenereerd verhaal met het hele corpus: **langste gemeenschappelijke substring**, **gedeelde 5-/8-gram-overlap (%)**, near-duplicate/semantische gelijkenis (embeddings).
- Check op Tellegens unieke neologismen (watertaart, beukennotensap, ...).
- **Acceptatiecriterium vooraf:** stijl-gelijkenis hoog **én** tekstoverlap onder drempel (bv. geen gedeelde 8-gram buiten functiewoorden) ⇒ stijlimitatie, geen plagiaat.
- Bij eventuele fine-tuning: test op memorisatie/regurgitatie (overlap met trainingsdata) en rapporteer; distribueer geen model dat de bron kan reproduceren.

## 7. Blindering & pre-registratie
- Rolscheiding: ontwerper ≠ prompt-auteur ≠ analist.
- Pre-registreer hypotheses, n, exclusiecriteria en analyseplan vóór dataverzameling.
- Geblindeerde, gerandomiseerde, gebalanceerde itempresentatie.

## 8. Model-arm — "komt Claude 4.8 dichterbij?" (en wat draait het bij)
- **Gecontroleerde vergelijking:** zelfde werkwijze/prompts/seeds; varieer **alleen** het schrijfmodel (bv. 4.6 vs 4.7 vs 4.8, plus één niet-Claude-model). Matched samples. **Zelfde (bij voorkeur niet-Claude) jury** en **zelfde stylometrische batterij**.
- Uitkomst per model: D (AUC mens), S (Delta-afstand tot Tellegen), slop-rate, burstiness. "Dichterbij" = lagere S-afstand en/of lagere D-AUC, met CI.
- **Wat het model "bijdraait" — eerlijk geoperationaliseerd.** Geen weights-/interpretability-toegang ⇒ géén mechanistische claim. Wél meetbaar wat in de *output-distributie* verschilt, en daaraan de verbetering toeschrijven:
  - zinslengte-variantie & burstiness (mensachtiger = grilliger),
  - lexicale diversiteit (type-token-ratio, hapax-ratio),
  - slop-/cliché-rate (Antislop n-gram-oververtegenwoordiging),
  - perplexiteit/entropie (minder "vlak"),
  - instructievolg-kwaliteit (volgt het de premisse-eerste motor beter?).
  Claim dan: "4.8 ligt op dimensies X/Y dichter bij Tellegens distributie" — behavioral/correlationeel.
- **Confound-bewaking:** jury NIET hetzelfde model als de schrijver, anders meet je modelaffiniteit i.p.v. kwaliteit.

## 9. Rapportage
Pre-registratielink; D (AUC + CI); S (afstanden + classifier-AUC); Q (rubric + α); P (overlap-tabel). Geen losse "9/10"-getallen zonder instrument-validatie.

## Wat hiervan nu al haalbaar is in deze repo
De stylometrische batterij (§5) en de plagiaat-audit (§6) zijn **lokaal te bouwen** (Python op de PDF-teksten), copyright-veilig, en leveren meteen objectieve, instrument-onafhankelijke cijfers — zonder mensen of LLM-jury. Dat is de snelste route naar gegronde getallen en kan de premisse-eerste verhalen (blindtest 8-9) als eerste casus nemen.
