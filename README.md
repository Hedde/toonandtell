# toonandtell

*Een meertraps agent-pipeline die Toon Tellegens dierenverhalen analyseert en synthetisch reproduceert — en zo het huidige plafond van AI-pastiche van een literaire stem in kaart brengt.*

---

## Over dit project

Experimenteel onderzoeksproject naar stilistische AI-imitatie van Toon Tellegens werk, opgezet als pipeline van vijf gespecialiseerde Claude-agents (linguïst, neerlandicus, redacteur, fan, schrijver). Zes blindtests, zeven tuningrondes en een literatuurscan tonen waar AI nu staat in literaire pastiche en — belangrijker — waar het structureel tekortschiet.

Het werk is **educatief** van aard, opgezet vanuit een taalanalytische interesse in wat er gebeurt als je een complexe literaire stem probeert te ontleden in reproduceerbare regels. De uitkomst is dubbel: een werkende methodische opzet voor stilistische analyse via meervoudige agents, én een empirische diagnose van wat in een literaire stem precies *niet* reduceerbaar blijkt.

### Repo-structuur

- **`.claude/agents/`** — vijf agent-definities (YAML-frontmatter + Markdown systeemprompt) die samen de pipeline vormen
- **`analyses/`** — onderzoeksoutput per Tellegen-bundel, cross-boek synthese, blindtest-rapporten en literatuurscan
- **`codex-review.md`** — interne audit van de review-revisie-cyclus
- **`README.md`** — dit document; volledig sessieverslag inclusief TL;DR

### Snel naar de kern

- Wil je weten **wat AI nu wel en niet kan** in literaire pastiche? Sectie 9 (TL;DR).
- Wil je de **methodologie** zien? Secties 2 en 3.
- Wil je de **blindtest-resultaten**? Secties 4 en 8.

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
    ├── verhaalproducties (slak v1/v2/v3, otter v1/v2, capybara, paling, mier-duizendpoot, ooievaar-kikker, reiger-kikker iter 1/2/3, mus-ochtend)
    └── reviews per ronde + 6 blindtests
```

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

---

## 9. TL;DR — waar AI nu staat en waar het tekortschiet

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

## 10. Bronnen

- Beyond the surface: stylometric analysis of GPT-4o's capacity for literary style imitation — *Digital Scholarship in the Humanities* 40(2) 2025 — https://academic.oup.com/dsh/article/40/2/587/8118784
- Catch Me If You Can? Not Yet: LLMs Still Struggle to Imitate the Implicit Writing Styles of Everyday Authors — EMNLP Findings 2025 / arXiv 2509.14543 — https://arxiv.org/html/2509.14543v1
- Antislop: A Comprehensive Framework for Identifying and Eliminating Repetitive Patterns in Language Models — ICLR 2026 / arXiv 2510.15061 — https://arxiv.org/abs/2510.15061
- Detecting authorship between generative AI models and humans: a Burrows's Delta approach — *Digital Scholarship in the Humanities* 40(3) 2025 — https://academic.oup.com/dsh/article-abstract/40/3/1064/8161203
- EQ-Bench Creative Writing Leaderboard 2026 (Claude Opus 4.7 — Elo 2216 / april 2026) — https://awesomeagents.ai/leaderboards/creative-writing-llm-leaderboard/
