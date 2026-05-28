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

- **`CLAUDE.md`** — de gevalideerde werkwijze, stapsgewijs (lees dit eerst bij vervolgwerk)
- **`.claude/agents/`** — vijf agent-definities (YAML-frontmatter + Markdown systeemprompt)
- **`analyses/refinement/LEARNINGS.md`** — zo wetenschappelijk mogelijke samenvatting (wat wel/niet werkte, kerntabel, false-positive-bevinding)
- **`analyses/refinement/PIPELINE.md`** — operationele stappen + `normalize.py`
- **`analyses/`** — onderzoeksoutput per bundel, cross-boek synthese, blindtest-rapporten (1-9), literatuurscan
- **`codex-review.md`** — interne audit van de review-revisie-cyclus
- **`README.md`** — dit document; volledig sessieverslag

### Snel naar de kern

- Wil je **het premisse-eerst-effect** en waarom we het niet als doorbraak mogen lezen? Secties 9 en 10.
- Wil je **wat wel/niet werkte** + de confounds, beknopt? `analyses/refinement/LEARNINGS.md`.
- Wil je de **methodologie**? Secties 2-3 (analyse) en `CLAUDE.md` (de gevalideerde pijplijn).
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

## 2. Aanpak

### 2.1 Definitie van de persona-agents

Voor elke agent werd online gezocht naar het profiel:
- *Linguistiek vs. neerlandistiek*: onderscheid tussen taalkundige (taalstructuur) en literair-cultureel afgestudeerde (BA Nederlandse taal en cultuur — UvA, Leiden, UU).
- *Curriculum*: 180 EC, modules in moderne en oudere letterkunde, taalkunde, taalbeheersing, media; namen van theoretici (Bal, Anbeek, Vaessens) opgenomen in de prompt.
- *Redacteur-profiel*: 25 jaar ervaring, fonds van het kaliber De Bezige Bij / Querido / Atlas Contact / Van Oorschot; beoordelingsdimensies: authenticiteit, literaire kwaliteit, uitgeefwaardigheid.
- *Tellegen-fan*: warme, persoonlijke stem; mossel als persoonlijke maatstaf ("De Mossel-Maatstaf").

De vier agents werden gedefinieerd als YAML-frontmatter + Markdown systeemprompt.

### 2.2 Parallelle analyse — 12 specialisten over 4 boeken

De vier PDFs (*Dank je wel*, *Een hart onder de riem*, *Maar niet uit het hart*, *Met hart en ziel*) werden in fase 1 door **12 specialisten parallel** gelezen — drie agents (linguïst, neerlandicus, redacteur) per boek. Output: 12 markdown-analyses, gemiddeld 250-500 regels per stuk.

Hierbij werd één content-filter-trigger geraakt (verbatim verkenning van een specifiek boek) en opnieuw gelanceerd met beknoptere citatie-instructies. Dit leidde tot een blijvende werkwijze: agents lezen voortaan **direct uit de bron-PDF via page-ranges**, niet uit door de hoofdsessie geknipte kopieën — ter voorkoming van auteursrechtelijke verbatim-reproductie. Dit werd vastgelegd in het persistent memory-systeem.

### 2.3 Twee niveaus synthese

- **Per-boek synthese** (fase 2): 4 parallelle neerlandicus-agents integreerden de drie perspectieven per boek tot één coherente teamanalyse (~300 regels per boek).
- **Cross-boek refinement** (fase 3): één meta-document (~550 regels) identificeerde 15 vier-uit-vier handtekeningen, 5 drie-uit-vier handtekeningen, boek-specifieke kleuringen, een grammatica op micro-/meso-/macro-/metaniveau, 7 doodzondes, een 20-skill-inventaris en model-openingen/sloten/dialogen.

Een eerste poging om dit master-document door één agent te laten schrijven liep op een idle timeout vast; de synthese werd daarna in de hoofdsessie zelf gemaakt op basis van de vier teamsyntheses.

### 2.4 Bouw van de schrijfagent

Op basis van het cross-boek-document werd een **operationele schrijfagent** opgesteld met:
- grondhouding (filosofische instructie)
- vaste cast met asymmetrie als motor
- vier inhoudelijke kleuringen (dankbaarheid / emoties als objecten / afscheid / het feest)
- skill-inventaris (begon op 20, groeide via tunings naar 27)
- doodzonden (begon op 7, groeide naar 9)
- workflow in 5 stappen met expliciete check-vragen (groeide van 5 naar 29)

### 2.5 Iteratieve refinement-loop

Voor elk geproduceerd verhaal werd de driehoek **linguïst + neerlandicus + redacteur** parallel ingezet om de tekst te beoordelen op:
- de eigen handtekening-criteria
- detectie van pastiche-signalen
- concrete tunings-aanbevelingen

Convergerende kritiek werd vervolgens als **chirurgische edit** in de schrijfagent verwerkt. Niet-convergerende kritiek werd terzijde gelegd.

### 2.6 Parallelisatie

Op piekmoment draaiden 12 agents tegelijk. Voor reviews steevast 3 parallel. Synthese-stappen 4 parallel. Dit werd mogelijk door `run_in_background: true` op de Agent-tool, zodat de hoofdsessie haar eigen context-window ongeschonden hield terwijl agents in eigen subprocessen werkten.

---

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
.claude/agents/
├── linguist-nederlands.md
├── neerlandicus-afgestudeerd.md
├── redacteur-uitgeverij.md
├── toon-tellegen-fan.md
└── toon-tellegen-schrijver.md            (398 regels, 7 tunings)

analyses/
├── dank_je_wel/
│   ├── linguist.md, neerlandicus.md, redacteur.md, team_synthese.md
├── een_hart_onder_de_riem/
│   ├── (idem)
├── maar_niet_uit_het_hart/
│   ├── (idem)
├── met_hart_en_ziel/
│   ├── (idem)
├── synthesis/
│   └── cross_book_refinement.md          (~550 regels)
└── refinement/
    ├── verhaalproducties fase 1-2 (slak, otter-kokkel, capybara, paling, mier-duizendpoot, ooievaar-kikker, reiger-kikker, mus-ochtend)
    ├── blindtest7/ (karper & snoek — proza-tuning + typografie genivelleerd)
    ├── blindtest8/ (zeekomkommer — premisse-eerst, bewijs + replicatie)
    ├── blindtest9/ (olifant — premisse-eerst, klassieke dieren, per-item-protocol)
    ├── LEARNINGS.md (wetenschappelijke samenvatting + confounds)
    ├── PIPELINE.md + normalize.py (operationele stappen + "de schoner")
    └── reviews per ronde + blindtests 1-9
```

Daarnaast in fase 3 toegevoegd/bijgewerkt: **`CLAUDE.md`** (root, de gevalideerde werkwijze) en de vijf agent-definities (schrijver: premisse-eerste motor + temporeel register; reviewers: diachrone register-, themalegbaarheid- en over-correctie-checks).

---

## 7. Conclusie van de eerste fase

Een goed georkestreerde meervoudige-agent-pipeline produceert substantieel kwalitatievere imitatie dan single-prompt AI (4/10 → 7-8,5/10). Tegelijk werd een principiële grens zichtbaar: synthetische *nonchalance* — het surplus van een schrijver in zijn eigen universum — blijft de scheidslijn tussen hoogwaardige pastiche en oorspronkelijk werk.

---

## 8. Vervolgsessie (mei 2026)

Een latere sessie testte twee aanvullende vragen: (a) blijft het plafond staan zonder de teamreview-revisie-loop, en (b) zijn er literaire/stilometrische methodes uit recent onderzoek die we hebben gemist?

### 8.1 Codex-review (interne pipeline-audit)

Een codex-audit op een eerdere review-revisie-cyclus toonde aan dat **revisie na teamreview de detecteerbaarheid verergert** in plaats van wegneemt: van 6/10 (82% AI) naar 4/10 (85% AI) over twee rondes. De reviewer-feedback wordt door de schrijver te zichtbaar opgevolgd; technische bewustheid stijgt, vanzelfsprekendheid daalt. Aanbeveling: één-shot generatie, geen verplichte review-revisie als default.

### 8.2 Blindtest 5 — reiger & kikker (3 iteraties, één-shot)

Drie onafhankelijke iteraties, drie reviewers, geen review-loop.

| Iter | AI herkend? | Zekerheid | AI-cijfer | Echte verhalen |
|------|-------------|-----------|-----------|----------------|
| 1 | ja | 78% | 6,0 | 9,5 + 9,0 |
| 2 | ja | 88% | 6,0 | 9,0 + 9,0 |
| 3 | ja | 82% | 6,5 | 9,5 + 9,5 |

3 op 3 herkend, gemiddeld 6,17/10. Concrete tells: markdown-asterisken als scènescheiders (iter 2 en 3), gesloten pseudo-syllogismen, gedeclareerde metafictie ("dit verhaal"), narratorcommentaar op irrelevante bijfiguren.

### 8.3 Literatuurscan

Vier recente bronnen bevestigen het pipeline-plafond als algemeen patroon en wijzen op één concrete techniek die we niet benutten:

- *Beyond the surface: stylometric analysis of GPT-4o's capacity for literary style imitation* (Oxford DSH 2025) — surface yes, Author Multilevel N-gram Profile no.
- *Catch Me If You Can? — LLMs Still Struggle to Imitate the Implicit Writing Styles of Everyday Authors* (EMNLP 2025) — meer few-shot voorbeelden helpen niet.
- *Antislop: A Comprehensive Framework for Identifying and Eliminating Repetitive Patterns in Language Models* (ICLR 2026) — model-specifieke fraseringen zijn 1000× oververtegenwoordigd; concrete blacklist-aanpak.
- *Detecting authorship between generative AI models and humans: a Burrows's Delta approach* (Oxford DSH 2025) — AI-teksten clusteren tight; menselijke teksten variëren breed; >80% detectie-accuratesse.

### 8.4 Tuning op basis van literatuur

Drie aanpassingen aan de schrijfagent — geen nieuwe technieken (codex-conform) maar concrete uitsluitingen + procedure:
- **Asterisk-verbod** (geen `*`/`\*`/`---` als scènescheider — alleen witregels);
- **Antislop-blacklist** (concrete fraseringen: *zoals X dat doen*, *dit verhaal*, prompt-voorbeelden zoals *schelp op een kier*, *zoethout*, *watertaart*);
- **Premise-first stap** (interne 2-3 regels achtergrond per personage, niet in tekst — geeft niet-functioneel surplus dat de literatuur als sleutel aanwijst).

### 8.5 Blindtest 6 — mus & ochtend (één-shot, met getunede agent)

| Metric | Waarde |
|--------|--------|
| AI herkend? | ja (positie B) |
| Zekerheid | 82% |
| AI-cijfer | 6,0 |
| Echte verhalen-cijfers | 9 + 9 |

De directe verbatim-tells (asterisken, blacklist-fraseringen) waren weg — bevestigd via grep. **De score verschoof niet.** De reviewer wees op nieuwe tells op syntactisch en compositioneel niveau: zelf-verklaarde vondst, overaccumulatie van stijlmarkers, herhaalde epistemische zinsstructuur, structurele symmetrie tussen opening en slot.

### 8.6 Update van het samenvattende beeld

| Blindtest | AI-verhaal | AI-cijfer | AI-detectie |
|-----------|-----------|-----------|-------------|
| 1 | Capybara | 7,5 | 85-90% |
| 2 | Paling | 7,5 | 85% |
| 3 | Mier-duizendpoot | **8,0** | **35%** (best) |
| 4 | Ooievaar-kikker | 7,0 | 75-85% |
| 5 (gem.) | Reiger-kikker | 6,17 | 82,7% |
| 6 | Mus-ochtend (met blacklist) | 6,0 | 82% |

Het plafond ligt rond 6-8/10. Tunings die binnen prompt-engineering blijven schuiven niet meer.

> **Nuance uit fase 3 (zie §9):** dit gold voor tuning op *zinsniveau*. Een ingreep op de *generatieve startpositie* (premisse-eerst i.p.v. thema-eerst) verschoof de panel-scores wél sterk — al bleek datzelfde panel een onbetrouwbare detector, dus de uitkomst is suggestief, niet bewijzend.

---

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
3. **Geen stylometrie.** Detectie gebeurde door *lezen en gokken*. De literatuur detecteert AI stylometrisch (Burrows' Delta, AMNP) met >80%, ongeacht leeskwaliteit; dat is hier niet getoetst. "Plafond doorbroken" is in stylometrische zin ongefundeerd.
4. **Zwakke opzet.** LLM-persona's i.p.v. menselijke experts; n=3 verhalen; niet-geblindeerde experimentator (dezelfde die ontwierp, koos en interpreteerde, met de hypothese in het hoofd); echte verhalen uit hun boekcontext gehaald en genormaliseerd (nadeel voor de reals).

De verdedigbare conclusie is daarom smal: *binnen deze gebrekkige opzet* gaf premisse-eerst een groot effect op de oordelen van een aantoonbaar onbetrouwbaar LLM-panel. Dat is een bruikbare generatie-strategie-hint en een interessante negatieve bevinding over LLM-detectoren — geen capaciteitsclaim over ononderscheidbaarheid.

### Hoe een zuivere meting eruit zou zien (vervolg)
- Menselijke beoordelaars, niet hetzelfde modelfamilie als de schrijver.
- Controle-items (bekend echt + bekend AI) door elkaar → sensitiviteit én specificiteit (ROC), niet alleen "vond het onze AI?".
- Een stylometrische toets op de premisse-eerste verhalen (Burrows' Delta / n-gram-profiel).
- Een plagiaat-audit (verbatim-overlap met het corpus) om stijlimitatie van tekstovername te scheiden.
- Meer trials, pre-registratie, geblindeerde set-samenstelling.

Het volledige rigoureuze ontwerp — inclusief de model-arm ("komt Claude 4.8 dichterbij, en wat draait het bij?") en de copyright-veilige plagiaat-audit — staat in **`analyses/refinement/PROTOCOL.md`**.

---

## 10. TL;DR — fase 1-2 (herzien door fase 3)

> **Let op:** onderstaande TL;DR vat fase 1-2 samen en stelde een structureel "6-8/10-plafond" vast bij prozagerichte tuning. Fase 3 (sectie 9) nuanceert dit op twee punten: (a) een andere *generatieve aanpak* (premisse-eerst) gaf binnen onze opzet veel hogere panel-scores, en (b) het LLM-panel bleek een onbetrouwbare detector. De claims hieronder over "detectie" en "het plafond" gelden dus alleen voor het zwakke LLM-panel-meetinstrument, niet als algemene capaciteits- of stylometrische uitspraak.

**Wat AI op dit moment kan, anno mei 2026 (Claude Opus 4.7, EQ-Bench Creative Writing leider):**

- *Surface-stijl reproduceerbaar:* zinslengte-distributies, woordlengtes, register, lexicaal veld, microtechnieken (parataxis, diminutief, vrije indirecte rede, reificatie). Dit gaat opvallend goed — een AI-Tellegen scoort 7-8/10 waar een naïef GPT-prompt 4/10 haalt.
- *Mid-level technieken reproduceerbaar:* asymmetrische cast, brief-als-genre, conditionaal-keten, predator-prooi-onderlaag — als procedure leerbaar.
- *Best-case:* in 1 van 4 blindtests werd 35% twijfel bereikt bij een expert-reviewer — ruim onder de 50% die voor "echt onderscheidsbaar" nodig is, maar boven het ruisniveau.

**Waar het structureel tekortschiet:**

1. **Uniformiteit is een sampling-eigenschap, geen regel-eigenschap.** Burrows' Delta detecteert AI-tekst met >80% accuratesse omdat AI-output tight clustert in z-score-ruimte. Geen prompt kan dit opheffen — een prompt kan specifieke patronen verbieden, waarna nieuwe uniforme patronen ontstaan. Dit is in deze sessie empirisch gerepliceerd: blacklist haalde de directe tells weg, score bleef gelijk, nieuwe tells verschenen.

2. **Author Multilevel N-gram Profile faalt.** Oppervlaktewoordkeuze klopt; de diepe sequentie­statistiek waarop literaire vingerafdrukken rusten niet. Stylometrische auteursherkenning blijft AI van mens scheiden ook bij hoog scorende imitaties.

3. **Geen authentiek surplus.** AI-output is intrinsiek consistent — iedere zin dient een functie, iedere terugkeer is gepland. Tellegens *bijna heerlijk*-effect ontstaat doordat de schrijver dingen schrijft die voor zichzelf bestaan, niet voor de tekst. De drie blindtest-reviewers diagnosticeerden onafhankelijk hetzelfde: de pipeline schrijft een verhaal dat *wil klinken alsof het niet weet hoe het eindigt*; Tellegen schrijft een verhaal dat werkelijk niet weet hoe het eindigt.

4. **Bewust geconstrueerde onafgemaaktheid is een vorm van afgemaaktheid.** Toevoegen van "ruwheid" via instructies produceert net zo goed pastiche als gepolijste imitatie. De "ruwheid" wordt zelf systematisch ingezet en daardoor herkenbaar.

5. **Prompt-engineering plateauert.** EMNLP 2025 bevestigt dat meer few-shot voorbeelden de metrics niet verbeteren. Onze zes tuningrondes lopen tegen dezelfde wand. Het plafond zit niet in de schrijver maar in de *output-distributie* van het onderliggende model.

**Wat in principe wél door de wand kan breken (volgens recent onderzoek), maar buiten dit project valt:**

- Fine-tuning op auteurscorpus (FTPO uit het Antislop-paper, 90% slop-reductie). Auteursrechtelijk en ethisch grijs op canonieke literatuur.
- Diffusion-based LLMs (recente vergelijkingen tonen LLaDA-output bijna ononderscheidbaar van mens op perplexity-metrics).
- Multi-temperatuur ensembles met menselijke of stylometrische selectie — introduceert echte sampling-spread.
- Hybride prompting + RL/DPO op auteurspecifieke discriminator-feedback.

**De bredere implicatie voor de taalanalyticus:**

AI-pastiche staat nu op het niveau van *competente literaire imitatie*: bruikbaar voor educatieve analyse, voor stijlverkenning, voor draftwerk. Niet op het niveau van *publiceerbaar onder de naam van de geïmiteerde auteur*. De grens tussen die twee niveaus blijkt geen schaalkwestie maar een eigenschap van wat een literaire stem *is* — een schrijver die in zijn eigen wereld iets meer schrijft dan zijn tekst. Modellen die patronen leren kunnen patronen reproduceren; ze kunnen geen *bewoner* zijn.

Tellegen-stijl is een bijzonder zuivere stresstest hiervoor, omdat zijn werk gebouwd is op minimalisme, stilte en het nalaten — precies de plekken waar AI standaard *opvult*. In die zin is het 6-8/10-plafond geen falen van de pipeline; het is een meting van waar het verschil tussen technisch kennen en literair *bewonen* op dit moment ligt.

---

## 11. Bronnen

- Beyond the surface: stylometric analysis of GPT-4o's capacity for literary style imitation — *Digital Scholarship in the Humanities* 40(2) 2025 — https://academic.oup.com/dsh/article/40/2/587/8118784
- Catch Me If You Can? Not Yet: LLMs Still Struggle to Imitate the Implicit Writing Styles of Everyday Authors — EMNLP Findings 2025 / arXiv 2509.14543 — https://arxiv.org/html/2509.14543v1
- Antislop: A Comprehensive Framework for Identifying and Eliminating Repetitive Patterns in Language Models — ICLR 2026 / arXiv 2510.15061 — https://arxiv.org/abs/2510.15061
- Detecting authorship between generative AI models and humans: a Burrows's Delta approach — *Digital Scholarship in the Humanities* 40(3) 2025 — https://academic.oup.com/dsh/article-abstract/40/3/1064/8161203
- EQ-Bench Creative Writing Leaderboard 2026 (Claude Opus 4.7 — Elo 2216 / april 2026) — https://awesomeagents.ai/leaderboards/creative-writing-llm-leaderboard/
