# toonandtell

*Een meertraps agent-pipeline die Toon Tellegens dierenverhalen analyseert en synthetisch reproduceert — en, eerlijker geformuleerd, vooral in kaart brengt hoe moeilijk het is om "ononderscheidbaarheid" überhaupt betrouwbaar te meten.*

---

## Over dit project

Experimenteel, **educatief** onderzoeksproject naar stilistische AI-imitatie van Toon Tellegens werk, opgezet als pipeline van vijf gespecialiseerde Claude-agents (linguïst, neerlandicus, redacteur, fan, schrijver). Negen blindtests en meerdere tuningrondes in drie fasen.

> **Belangrijk methodologisch voorbehoud vooraf.** Alle "beoordelaars" in dit project zijn LLM-agents (Claude), géén menselijke experts. De schrijfagent is hetzelfde modelfamilie als de jury. Detectie gebeurt door *lezen en gokken*, niet stylometrisch. De getallen hieronder zijn dáárom indicatief, niet bewijzend — zie sectie 10 voor de volledige lijst confounds. Lees "0/3 herkend" als "dit specifieke, aantoonbaar onbetrouwbare LLM-panel flagde het niet", niet als "ononderscheidbaar voor mensen of voor stylometrie".

De uitkomst kent drie lagen:
1. Een werkende methodische opzet voor stilistische analyse via meervoudige agents (fase 1-2).
2. Bij prozagerichte prompt-tuning bleef het LLM-panel alle AI-verhalen herkennen, met scores rond **6-8/10** (fase 1-2) — destijds geïnterpreteerd als een structureel plafond.
3. **Fase 3:** een andere *generatieve aanpak* — **premisse-eerst** in plaats van thema-eerst — leverde binnen deze opzet een groot effect op (panel-scores ~9-10/10, 0/3 geflagd, over drie verhalen incl. klassieke dieren). MAAR datzelfde experiment toonde dat het panel een **onbetrouwbaar meetinstrument** is: het bestempelde meerdere échte Tellegen-verhalen als AI, en gaf hetzelfde echte verhaal in verschillende runs tegengestelde oordelen. Het grote effect is dus suggestief, niet bewijzend; het "plafond" is niet aantoonbaar doorbroken in stylometrische of menselijke zin.

### Repo-structuur

- **[CLAUDE.md](CLAUDE.md)** — de gevalideerde werkwijze, stapsgewijs (lees dit eerst bij vervolgwerk)
- **`.claude/agents/`** — vijf agent-definities (YAML-frontmatter + Markdown systeemprompt)
- **[LEARNINGS.md](analyses/refinement/LEARNINGS.md)** — zo wetenschappelijk mogelijke samenvatting (wat wel/niet werkte, kerntabel, false-positive-bevinding)
- **[PIPELINE.md](analyses/refinement/PIPELINE.md)** — operationele stappen + `normalize.py`
- **`analyses/`** — onderzoeksoutput per bundel, cross-boek synthese, blindtest-rapporten (1-9), literatuurscan
- **`README.md`** — dit document; volledig sessieverslag

### Snel naar de kern

- Wil je **het premisse-eerst-effect** en waarom we het niet als doorbraak mogen lezen? Secties 9 en 10.
- Wil je **wat wel/niet werkte** + de confounds, beknopt? [LEARNINGS.md](analyses/refinement/LEARNINGS.md).
- Wil je de **methodologie**? Secties 2-3 (analyse) en [CLAUDE.md](CLAUDE.md) (de gevalideerde pijplijn).
- Wil je de **blindtest-resultaten** fase 1-2? Secties 4 en 8.

---

## 1. Oorspronkelijke opdracht

De gebruiker, taalanalyticus, formuleerde achtereenvolgens vier opdrachten die samen een experimenteel project vormden:

1. **Vier persona-agents opzetten** rond Nederlandse literatuur:
   - een linguïst (Nederlandse taalkundige)
   - een afgestudeerde neerlandicus (BA Nederlandse taal en cultuur)
   - een literair redacteur van een gerenommeerde uitgeverij
   - een fan van Toon Tellegen (favoriet: de mossel uit *Met hart en ziel*)

   Met de instructie eerst online te onderzoeken wat zo'n linguïst doet en wat het Nederlands-curriculum behelst, voor de prompts werden geschreven.

2. **Met dat team vier Tellegen-bundels parallel laten lezen en analyseren**, vervolgens via cross-boek refinement een meta-document opstellen waarop een **vijfde agent** gebouwd kon worden: de *toon-tellegen-schrijver*, die nieuwe verhalen kan produceren in herkenbaar Tellegen-idioom.

3. **De schrijver verhalen laten produceren** (slak op reis, otter en kokkel, capybara met faalangst, paling, mier op visite bij duizendpoot, ooievaar en kikker), telkens gevolgd door reviews van het oorspronkelijke team.

4. **Iteratieve tuning** van de schrijver op basis van de reviews, en **blindtests** waarin het AI-werk anoniem naast echte Tellegen werd gelegd om de detecteerbaarheid te meten.

---

## 2. Aanpak (fase 1-2, beknopt)

Vijf persona-agents (linguïst, neerlandicus, redacteur, fan, schrijver), gedefinieerd na online profielonderzoek. De vier bundels werden door 12 specialisten parallel geanalyseerd (3 perspectieven x 4 boeken), per boek gesynthetiseerd en samengevoegd tot één cross-boek-document (`analyses/synthesis/cross_book_refinement.md`: vier-uit-vier-handtekeningen, een grammatica op micro/meso/macro/meta-niveau, doodzondes, skill-inventaris). Daarop is de schrijfagent gebouwd. Reviews liepen via de driehoek linguïst+neerlandicus+redacteur; convergerende kritiek werd als chirurgische edit verwerkt, niet-convergerende terzijde gelegd. Content-filter-werkwijze: agents lezen direct uit de bron-PDF's, geen verbatim kopieën naar nieuwe bestanden. Op piek draaiden 12 agents parallel.

## 3. Tuning-rondes — chronologie

| Ronde | Trigger | Belangrijkste aanscherpingen |
|---|---|---|
| **1** | Eerste review op slak v1 | Reificatie verplicht; *alsof*-vergelijking in slot verboden; brief moet zelf-weerleggend element bevatten; catalogus eindigt concreet; doodzonden uitgebreid van 7 naar 9 (architectuur-moraal, ingeburgerd idioom). |
| **2** | Reviews op slak v2 + otter-kokkel v1 | Slot zonder voltooiingswerkwoord; conditionaal-keten breekt af vóór conclusie; predator-prooi-onderlaag (ingegeven door observatie van gebruiker); afscheidsregels niet symmetrisch; "geest boven letter" als skill 21. |
| **3** | Reviews op slak v3 + otter-kokkel v2 | Brief mag niet vermeden; geen verklaring van eigen absurditeit in brief; reificatie niet cursief; geen commentaar-zin na filosofische vraag; eigen filosofische vraag (geen letterlijke ontlening uit prompt). |
| **4** | Blindtest 1 (capybara) — herkend met 85-90% | Anti-jargon (*faalangst*, *trauma*, *eenzaamheid* verboden); brief mag thema niet formuleren; reificatie keert niet thuis; bijfiguren leiden eigen leven (irrelevant gebaar verplicht). |
| **5** | Blindtest 2 (paling) — herkend met 85% | Anti-perfectie (skill 22): bewust ruwheid; centraal beeld max twee keer expliciet (skill 23); geen biologische instincten als plot-motor (skill 24); slot niet sfeerig. |
| **6** | Blindtest 3 (mier-duizendpoot) — 35% twijfel bij linguist | Anti-meta-vergelijkingen (skill 25); anti-geclipte-effect-afsluiters (skill 26); paradox van personage niet netjes uitspreken (skill 27). |

De agent groeide van 187 → 339 regels.

---

## 4. Blindtests — resultaten

In totaal vier blindtests waarin AI-output anoniem naast echte Tellegen werd geplaatst. Bij blindtest 3 werd ook een single-prompt ChatGPT-respons (zonder pipeline-kennis) als controlepunt toegevoegd.

| Blindtest | AI-verhaal | Linguist | Neerlandicus | Redacteur |
|---|---|---|---|---|
| 1 | Capybara | 7,5 — 85% AI | 6,0 — pastiche | 85-90% AI |
| 2 | Paling | 7,5 — 85% AI | 7,0 — 80% AI | 85% AI |
| 3 | Mier-duizendpoot | **8,0 — 35% AI** | 8,5 — 85% AI | "significant resultaat" |
| 3 (controle) | ChatGPT-naïef slak | 4,0 — naïeve AI | 4,0 — naïeve AI | naïeve AI |
| 4 | Ooievaar-kikker | 7,0 — 85% AI | 7,5 — 75% AI | 7 — 85% AI |

Echte Tellegen scoorde in alle blindtests structureel **9,0-10/10**.

---

## 5. Bevindingen

### 5.1 Pipeline overtreft single-prompt AI dramatisch

De controlebenchmark was helder: een single-prompt ChatGPT-respons scoort gemiddeld **4,0/10**. Onze meervoudige-agent-pipeline scoort **7-8,5/10** — een verdubbeling. Het verschil zit in:
- werkelijke reificatie versus illustratie van een thema
- bijfiguren met eigen leven versus instrumenten
- open slot versus moraliserend slot
- neutrale verteller versus empathisch-verklarende verteller

### 5.2 Plafond rond 7,5-8,5/10

Iteratieve tuning bereikt een plafond. De zesde tuning (anti-meta-vergelijking, anti-clip, anti-articulate-paradox) leverde *geen* progressie meer; het ooievaar-kikker-verhaal scoorde lager dan de mier-duizendpoot. Het beste resultaat (mier-duizendpoot, 35% twijfel bij de linguist) was niet repliceerbaar door verdere instructie.

### 5.3 Convergerende verklaring van het plafond

Alle drie reviewers formuleerden onafhankelijk dezelfde diagnose:
- *"Authentiek Tellegen is ook zijn onregelmatigheden, zijn niet-sierlijke formuleringen op cruciale plekken"* (linguïst)
- *"Echte Tellegen heeft altijd een surplus dat niet in dienst staat van de compositie"* (neerlandicus)
- *"De pipeline schrijft een verhaal dat wil klinken alsof het niet weet hoe het eindigt. Tellegen schrijft een verhaal dat werkelijk niet weet hoe het eindigt"* (redacteur)

Het structurele probleem: **bewust geconstrueerde onafgemaaktheid is een vorm van afgemaaktheid.** AI-output is intrinsiek consistent; iedere zin dient een doel; iedere terugkeer is functioneel. Een schrijver die handelt vanuit een eigen wereld heeft *surplus*: zinnen die voor zichzelf bestaan, niet voor de tekst.

### 5.4 Methodologische opbrengst

Onafhankelijk van het stilistische resultaat heeft het experiment een herbruikbare werkwijze opgeleverd:
- specialistische persona-agents als parallelle lezers
- meertraps synthese (per-boek → cross-boek)
- iteratieve refinement-loop met drie-perspectieven-jury
- blindtests als objectieve meetlat
- chirurgische tunings op basis van convergerende kritiek

Dit patroon is overdraagbaar naar andere stilistische analyse-projecten.

---

## 6. Artefacten

```
CLAUDE.md                                  de gevalideerde werkwijze, stapsgewijs
.claude/agents/   vijf agents (schrijver: premisse-eerste motor + temporeel register;
                  reviewers: diachrone register-, themalegbaarheid- en over-correctie-checks)
analyses/
├── dank_je_wel/ · een_hart_onder_de_riem/ · maar_niet_uit_het_hart/ · met_hart_en_ziel/
│        (per boek: linguist.md, neerlandicus.md, redacteur.md, team_synthese.md)
├── synthesis/cross_book_refinement.md     (fundament voor de schrijfagent)
└── refinement/
    ├── LEARNINGS.md · PIPELINE.md · PROTOCOL.md   (resultaten / werkwijze / rigoureus meetontwerp)
    ├── blindtest5_summary.md · literatuur_aanknopingspunten.md   (compacte fase 1-2-record)
    ├── blindtest7/  (karper & snoek — proza-tuning + typografie genivelleerd)
    ├── blindtest8/  (zeekomkommer — premisse-eerst: bewijs + replicatie)
    ├── blindtest9/  (olifant — premisse-eerst, klassieke dieren, per-item-protocol)
    └── stylometry/  (measure.py, stylometry.py, extract_corpus.sh, RESULTS.md)
```

De granulaire fase-1-2-werkbestanden (per-reviewer-reviews, vroege story-drafts, per-ronde-blindtests) zijn opgeschoond; de fundamentele analyses, de cross-boek-synthese en de samenvattingen bleven behouden. Verbatim bron-extracten en render-PDF's staan in `.gitignore` (auteursrecht / reproduceerbaar).

---

## 7. Conclusie van de eerste fase

Een goed georkestreerde meervoudige-agent-pipeline produceert substantieel kwalitatievere imitatie dan single-prompt AI (4/10 → 7-8,5/10). Tegelijk werd een principiële grens zichtbaar: synthetische *nonchalance* — het surplus van een schrijver in zijn eigen universum — blijft de scheidslijn tussen hoogwaardige pastiche en oorspronkelijk werk.

---

## 8. Vervolgsessie — plafond zonder review-loop + literatuurscan (beknopt)

Een latere sessie toetste of het plafond standhoudt zónder de review-revisie-loop, en scande recente literatuur. Bevindingen: (a) revisie ná teamreview verergert de detecteerbaarheid (de schrijver volgt feedback te zichtbaar op) — één-shot generatie werkt beter als default; (b) blindtests 5-6 (reiger-kikker, mus-ochtend) bleven 3/3 herkend rond 6/10, ook met een antislop-blacklist en een verbod op markdown-scènescheiders; (c) vier bronnen (zie §11) bevestigen het patroon: surface reproduceerbaar, de diepe stylometrische vingerafdruk niet, en meer few-shot voorbeelden helpen niet. Netto bleef het plafond rond 6-8/10 — wat fase 3 vervolgens herkadert.

## 9. Fase 3 (mei 2026): het premisse-eerst-effect — en de kritische lezing

Een latere fase stelde drie vragen: blijft het 6-8/10-plafond staan; is het de typografie die verraadt; en is er een aanpak die we misten?

**Blindtest 7 — proza-tuning + typografie genivelleerd.** Een AI-verhaal (karper & snoek) werd chirurgisch herzien op alle bekende tells, en alle vier teksten gingen door één identieke pijplijn (rechte aanhalingstekens, gelijke spatiëring, herstelde alinea's, monospace render). AI bleef ~4,3-5,7/10, 3/3 geflagd. Conclusie: het waren niet de leestekens, en zinsniveau-tuning plateaut — consistent met fase 1-2.

**De gap-hypothese.** We optimaliseerden steeds de *prozalaag*, terwijl de premisse naturalistisch bleef en het thema benoembaar. Hypothese: de hefboom is de *generatieve startpositie*, niet de zin — begin bij een concrete, absurde, letterlijk-genomen premisse (à la Tellegens nijlpaard-in-de-lucht), werk de logistiek deadpan uit, weiger een benoembaar thema, en optimaliseer niet (laat ruwheid staan).

**Blindtest 8 & 9 — premisse-eerst (binnen-opzet-resultaat).**

| Test | AI-verhaal | Protocol | Panel-score | Geflagd als AI |
|---|---|---|---|---|
| 8-bewijs | zeekomkommer | forced-choice | 9,5/10 | 0/3 |
| 8-replicatie | zeekomkommer | forced-choice, 3 sterke reals | 10/10 | 0/3 |
| 9 | olifant (klassieke dieren) | per-item (geen forced-choice) | 9/10 | 0/3 |

Drie refinements zijn in de agents verwerkt: de premisse-eerste motor, een temporeel register (idioom ca. 1984-2004), en een regie-principe — de orchestrator neemt reviewersuggesties *niet klakkeloos* over, want over-correctie poetst productieve ruwheid weg en is zelf een tell.

### Waarom dit GEEN aangetoonde doorbraak is

Hetzelfde experiment ondermijnt zijn eigen sterke lezing. Vier confounds, van zwaar naar licht:

1. **Circulaire beoordeling.** Schrijver én jury zijn hetzelfde modelfamilie (Claude). Een LLM die LLM-output op authenticiteit beoordeelt is vermoedelijk geneigd output die past bij zijn eigen prior als echt te zien. De 0/3 kan grotendeels dáárvan komen.
2. **Onbetrouwbaar instrument.** Het panel flagde meerdere ECHTE Tellegens als AI (vergeetboek 3/3, "nu of nooit" 2/3) en gaf hetzelfde echte verhaal in verschillende runs tegengestelde oordelen (vergeetboek: eerst 9/9/9 "echt", later 3/3 "AI"). Als het instrument echt-van-echt niet scheidt, is non-detectie van onze AI zwak bewijs.
3. **Geen stylometrie.** Detectie gebeurde door *lezen en gokken*. De literatuur detecteert AI stylometrisch (Burrows' Delta, AMNP) met >80%, ongeacht leeskwaliteit; dat is hier niet getoetst. "Plafond doorbroken" is in stylometrische zin ongefundeerd. (Inmiddels wél in een pilot gemeten — zie de stylometrie-subsectie hieronder; uitkomst: premisse-eerst komt stylometrisch níét dichterbij.)
4. **Zwakke opzet.** LLM-persona's i.p.v. menselijke experts; n=3 verhalen; niet-geblindeerde experimentator (dezelfde die ontwierp, koos en interpreteerde, met de hypothese in het hoofd); echte verhalen uit hun boekcontext gehaald en genormaliseerd (nadeel voor de reals).

De verdedigbare conclusie is daarom smal: *binnen deze gebrekkige opzet* gaf premisse-eerst een groot effect op de oordelen van een aantoonbaar onbetrouwbaar LLM-panel. Dat is een bruikbare generatie-strategie-hint en een interessante negatieve bevinding over LLM-detectoren — geen capaciteitsclaim over ononderscheidbaarheid.

### Hoe een zuivere meting eruit zou zien (vervolg)
- Menselijke beoordelaars, niet hetzelfde modelfamilie als de schrijver.
- Controle-items (bekend echt + bekend AI) door elkaar → sensitiviteit én specificiteit (ROC), niet alleen "vond het onze AI?".
- Een stylometrische toets op de premisse-eerste verhalen (Burrows' Delta / n-gram-profiel).
- Een plagiaat-audit (verbatim-overlap met het corpus) om stijlimitatie van tekstovername te scheiden.
- Meer trials, pre-registratie, geblindeerde set-samenstelling.

Het volledige rigoureuze ontwerp — inclusief de model-arm ("komt Claude 4.8 dichterbij, en wat draait het bij?") en de copyright-veilige plagiaat-audit — staat in **[PROTOCOL.md](analyses/refinement/PROTOCOL.md)**.

### Stylometrische pilot + fingerprint-in-de-loop (de objectieve maatlat)

Daarna is de eerste twee punten hierboven deels uitgevoerd met een lokale, niet-circulaire harness (`analyses/refinement/stylometry/`): een Burrows'-achtige MFW-Delta + een **held-out** karakter-3-gram-Delta + verbatim-overlap. Vier bevindingen (pilot, kleine n; [RESULTS.md](analyses/refinement/stylometry/RESULTS.md)):

- **Premisse-eerst ≈ thema-eerst stylometrisch.** MFW-Delta tot Tellegen: 0,850 vs 0,869 (verschil binnen de ruis). Het premisse-eerst-voordeel zat dus in de *leesindruk*, niet in de forensische vingerafdruk.
- **Blijvende, modus-onafhankelijke tells:** AI gebruikt ~34% meer komma's dan Tellegen en heeft lagere lexicale diversiteit; premisse-eerst repareert dat niet. Een getrainde classifier zou AI vermoedelijk nog steeds scheiden.
- **Fingerprint-in-de-loop — wat wél/niet werkt (na verificatie).** Oppervlakte-chirurgie (komma's/functiewoorden) én best-of-N-selectie sluiten de gap NIET (de held-out char3 volgt niet; r=0,40); per-tekst surgery helpt één pas en plateaut dan (Goodhart). **Wat wél sloot:** de *systematische* afwijkingen verplaatsen naar **register-constraints ín de agent** (generatie-tijd, voor terugkerende biases: minder was/niet/dan/nu, meer in/zijn/uit, komma's laag, tags variëren). Dat bracht de baseline op béíde families binnen het Tellegen-bereik, **inclusief de held-out char-3-gram** (5 teksten char3 0,82–0,91 vs 1,05–1,30; animal-confound uitgesloten via identieke dieren: reiger char3 1,30→0,90, kreeft 1,09→0,83), en de verhalen lezen goed. **De balans (bewezen): systematisch → constraint; idiosyncratisch → hooguit één surgical pass.** Voorbehoud: 2 families / onze harness / n klein / één auteur — geen bewijs van ononderscheidbaarheid voor neurale detectoren of mensen. Detail: [RESULTS.md](analyses/refinement/stylometry/RESULTS.md) §7-9.
- **Geen plagiaat:** verbatim-overlap verwaarloosbaar (8-gram ≈ 0%; één eerlijk gemelde stockfrase-collisie).

Dit alles **strookt met** de geciteerde literatuur en weerlegt die niet.

### Model-vergelijking (4.8 vs 4.6 vs 4.5 vs Codex; N=4 per model, taak constant)

Zelfde taak (premisse-eerst + dialoog + register-constraints) en dezelfde 4 dieren; alleen het schrijfmodel varieert. Claude 4.7 was niet beschikbaar; de **Codex-arm is niet blind** (de agent kende de meetopzet en eerdere uitkomsten).

| model | MFW-Delta | char3-Delta (held-out) |
|---|---|---|
| **Opus 4.8** | 0,870 | **0,906** |
| Codex | 0,921 | 1,051 |
| Sonnet 4.6 | 0,859 | 1,117 |
| Haiku 4.5 | 1,024 | 1,105 |
| *echt (ref)* | 0,765 | ~0,78 (per-verhaal 0,76–0,98) |

Op de discriminerende held-out char-3-gram ligt **Opus 4.8 het dichtst bij Tellegen** (binnen het echte bereik), gevolgd door Codex, dan Haiku 4.5 en Sonnet 4.6. Eerste *meetbare* indicatie van een modelbijdrage — met de caveats (klein, één auteur, eigen harness, constraints deels van 4.8-data afgeleid; Codex-arm niet blind). Detail: [RESULTS.md](analyses/refinement/stylometry/RESULTS.md) §10.

---

## 10. TL;DR — geïntegreerde, objectieve conclusie (alle fases samen)

Bekijk je niet elke fase apart maar het geheel, dan verschuift de eerlijke conclusie weg van een rapportcijfer.

**Eén instrument, twee tegengestelde cijferreeksen.** Fase 1-2 gaf 6-8/10 met 3/3-detectie; fase 3 (premisse-eerst) gaf 9-10/10 met 0/3. Beide reeksen komen van hetzelfde meetinstrument: een panel van LLM-agents uit dezelfde modelfamilie als de schrijver. In fase 3 is aangetoond dat dat instrument onbetrouwbaar is — het bestempelt echte Tellegens als AI en geeft identieke tekst tussen runs tegengestelde oordelen.

**Wat dat met de cijfers doet.** Een *absolute* uitspraak ("AI komt tot 9/10" of "ononderscheidbaar van Tellegen") is niet houdbaar: ze rust op een instrument dat echt-van-echt niet betrouwbaar scheidt, plus een circulaire jury (schrijver = jury-modelfamilie). Wél houdbaar zijn *relatieve, ordinale* vergelijkingen binnen hetzelfde instrument:
- de pipeline > een naïef één-shot-prompt (≈7-8 vs ≈4) — relatief robuust, want beide zijn AI;
- premisse-eerst > thema-eerst — verschoof de *panel-oordelen* sterk en consistent (exotische én klassieke dieren), maar **stylometrisch geen verschil** (zie pilot).

Die *ordening* is informatief; de bijbehorende *absolute getallen* niet.

**De twee uitspraken die het hele traject overleven:**

1. **Methodisch/generatief (positief, bescheiden).** Een meertraps analyse→generatie→review→blindtest-opzet werkt als onderzoeksinstrument, en één generatieve hefboom bleek robuust: *begin bij een concrete, absurde premisse, niet bij een thema, en optimaliseer niet.* Bruikbaar als schrijfstrategie — geen capaciteitsbewijs.
2. **Meet-technisch (negatief — wellicht het stevigste resultaat).** LLM-panels zijn onbetrouwbare detectoren van literaire AI-imitatie: ze missen goede imitaties én beschuldigen authentiek werk, en hun oordeel is contextafhankelijk en instabiel. Wie "ononderscheidbaarheid" of "AI-detectie" claimt op basis van LLM-jury's, meet het instrument, niet de tekst.

**Wat een stylometrische pilot daarna toevoegde.** Een lokale harness (MFW-Delta + held-out char-3-gram-Delta) gaf het antwoord op de open vraag: premisse-eerst verkleint de stilistische afstand tot Tellegen **niet** (0,850 vs 0,869 voor thema-eerst); het voordeel zat alleen in de leesindruk. Modus-onafhankelijke tells blijven, en per-tekst-surgery/best-of-N sluiten de gap niet. **Wat de gap (op onze twee families) wél sloot:** de systematische tells als **constraints in de agent** zetten — dat bracht de baseline binnen het Tellegen-bereik, inclusief de held-out char-3-gram (RESULTS §9). De balans: systematisch → constraint, idiosyncratisch → hooguit één surgical pass. Dit blijft een pilot (2 families, kleine n, geen getrainde classifier, geen menselijke raters) — geen vervanging van het volledige ontwerp in [PROTOCOL.md](analyses/refinement/PROTOCOL.md).

**De zuivere bottom line (met balans optimisme/terughoudendheid).**
- *Wat werkt (gefundeerd, behouden in het proces):* (1) **premisse-eerst** generatie verbetert de *leesindruk* sterk; (2) **systematische tells als constraints in de agent** brengen de *stylometrische* afstand (MFW + held-out char-3-gram) binnen het Tellegen-bereik — reproduceerbaar en confound-gecontroleerd; (3) één **data-gedreven surgical pass** ruimt het idiosyncratische residu op. Samen: constraints doen het zware werk, premisse-eerst de toon, surgery de rest.
- *Wat niet werkt (geschrapt):* oppervlakte-woordchirurgie, iteratief doorpoetsen, en best-of-N-selectie — die gamen één metriek zonder transfer.
- *Terughoudendheid (meer empirisch werk nodig):* dit is gemeten op twee feature-families met onze eigen harness, kleine n, één auteur, en met een LLM-jury die aantoonbaar onbetrouwbaar is. "Binnen ons stylometrische bereik én overtuigend voor een LLM-panel" is **niet** hetzelfde als "ononderscheidbaar voor een getrainde stylometrische classifier of voor menselijke experts". Die generieke claim vergt het ontwerp in [PROTOCOL.md](analyses/refinement/PROTOCOL.md) (menselijke raters, niet-circulaire/getrainde detector, controle-items, meer auteurs, pre-registratie). De wetenschappelijk best onderbouwde gap-sluiter blijft **fine-tunen op het oeuvre** (modelniveau, auteursrechtelijk gated) — buiten dit proces.

---

## 11. Bronnen

- Beyond the surface: stylometric analysis of GPT-4o's capacity for literary style imitation — *Digital Scholarship in the Humanities* 40(2) 2025 — https://academic.oup.com/dsh/article/40/2/587/8118784
- Catch Me If You Can? Not Yet: LLMs Still Struggle to Imitate the Implicit Writing Styles of Everyday Authors — EMNLP Findings 2025 / arXiv 2509.14543 — https://arxiv.org/html/2509.14543v1
- Antislop: A Comprehensive Framework for Identifying and Eliminating Repetitive Patterns in Language Models — ICLR 2026 / arXiv 2510.15061 — https://arxiv.org/abs/2510.15061
- Detecting authorship between generative AI models and humans: a Burrows's Delta approach — *Digital Scholarship in the Humanities* 40(3) 2025 — https://academic.oup.com/dsh/article-abstract/40/3/1064/8161203
- EQ-Bench Creative Writing Leaderboard 2026 (Claude Opus 4.7 — Elo 2216 / april 2026) — https://awesomeagents.ai/leaderboards/creative-writing-llm-leaderboard/

**Aanvullende literatuurscan (fase 3):**
- Language Models Optimized to Fool Detectors Still Have a Distinct Style (And How to Change It) — arXiv 2505.14608 — https://arxiv.org/html/2505.14608 *(bevestigt onafhankelijk: surface/DPO-optimalisatie laat een residu-stijl staan)*
- Readers Prefer Outputs of AI Trained on Copyrighted Books over Expert Human Writers — arXiv 2510.13939 — https://arxiv.org/html/2510.13939v1 *(fine-tunen op oeuvre sluit de gap; auteursrechtelijk gated)*
- On the Effect of Sampling Diversity in Scaling LLM Inference — arXiv 2502.11027 — https://arxiv.org/html/2502.11027v3 *(LLM-samples "trapped in a cluster" = de tight-clustering; best-of-N + diversiteit)*
- ParaGuide: Guided Diffusion Paraphrasers for Plug-and-Play Textual Style Transfer — arXiv 2308.15459 — https://arxiv.org/abs/2308.15459
- LLM one-shot style transfer for Authorship Attribution and Verification — arXiv 2510.13302 — https://arxiv.org/abs/2510.13302

**Praktijk-referenties (dit project, eigen metingen):** blindtests 1-9 (`analyses/refinement/`), stylometrie + plagiaat-audit + constraints-vs-surgery ([RESULTS.md](analyses/refinement/stylometry/RESULTS.md)), gevalideerde werkwijze ([CLAUDE.md](CLAUDE.md), [PIPELINE.md](analyses/refinement/PIPELINE.md)), rigoureus vervolgontwerp ([PROTOCOL.md](analyses/refinement/PROTOCOL.md)).
