# toonandtell

Onderzoek naar de vraag of een pipeline van Claude-agents dierenverhalen kan schrijven die niet van Toon Tellegen te onderscheiden zijn, en hoe je dat betrouwbaar meet.

Het project is educatief en methodisch van opzet. Het telt vier fasen: stijlanalyse en een schrijfagent (fase 1-2), een andere manier van genereren (fase 3, mei 2026) en metingen zonder LLM-jury op de nieuwste modellen (fase 4, november 2026). In fase 1-3 zijn negen blindtests gehouden.

## Belangrijkste uitkomsten

- **Niets is ononderscheidbaar.** Een getrainde stylometrische detector scheidt elke geteste opzet vrijwel perfect van echte Tellegen (AUC ≥0,97), ook op Opus 5.5 en Fable 5.2.
- **De schrijfgids maakt verhalen op de nieuwste modellen makkelijker te detecteren.** De volledige schrijfagent (429 regels) doet het niet aantoonbaar beter dan een kale variant van 30 regels. Met beide worden de verhalen uniformer dan met een opdracht zonder gids, en daardoor beter herkenbaar.
- **Regels die een model-tic corrigeren, verouderen met het model.** De register-constraints zijn afgeleid van Opus 4.8. Op Opus 5.5 en Fable 5.2 schieten ze door naar de andere kant.
- **Premisse-eerst verbetert de leesindruk, niet de vingerafdruk.** Beginnen bij een concrete, absurde premisse in plaats van bij een thema bracht de panelscores van ongeveer 5 naar 9-10 op 10. Stylometrisch maakt het geen verschil.
- **LLM-panels zijn onbetrouwbare detectoren.** Het panel bestempelde echte Tellegen-verhalen als AI en gaf dezelfde tekst in verschillende runs tegengestelde oordelen.

> **Lees de panelcijfers met voorbehoud.** In fase 1-3 zijn alle beoordelaars LLM-agents uit dezelfde modelfamilie als de schrijver, en ze oordelen door te lezen. "0/3 herkend" betekent dat dit panel het verhaal niet aanwees, niet dat het voor mensen of voor stylometrie ononderscheidbaar is. Alleen de stylometrie in fase 3 en de metingen in fase 4 werken zonder jury.

## Waar staat wat

| Bestand of map | Inhoud |
|---|---|
| [CLAUDE.md](CLAUDE.md) | De werkwijze, stap voor stap. Beveelt de register-constraints nog aan; zie fase 4 voor de correctie. |
| `.claude/agents/` | Vijf agent-definities: linguïst, neerlandicus, redacteur, fan en schrijver. |
| [LEARNINGS.md](analyses/refinement/LEARNINGS.md) | Samenvatting van wat wel en niet werkte, per experiment. |
| [RESULTS.md](analyses/refinement/stylometry/RESULTS.md) | Alle stylometrische metingen; §11-12 beschrijven fase 4. |
| [PIPELINE.md](analyses/refinement/PIPELINE.md) | Operationele stappen en de typografische normalisatie. |
| [PROTOCOL.md](analyses/refinement/PROTOCOL.md) | Ontwerp voor een volwaardige meting met menselijke beoordelaars. |
| `analyses/<bundel>/` | Per bundel de analyses van linguïst, neerlandicus en redacteur, plus een synthese. |
| `analyses/synthesis/` | Het overkoepelende stijldocument waarop de schrijfagent is gebouwd. |
| `analyses/refinement/blindtest7-9/` | De blindtests van fase 3. |
| `analyses/refinement/stylometry/` | De meet-harness (`measure.py`, `stylometry.py`), de gold-triad (`triad/`) en de armen-meting (`arms/`). |

De vier bron-PDF's, de daaruit getrokken tekst en de render-PDF's staan in `.gitignore`. Agents lezen rechtstreeks uit de PDF's; letterlijke Tellegen-tekst wordt niet naar nieuwe bestanden gekopieerd. De gedetailleerde werkbestanden van fase 1-2 (losse reviews, vroege concepten) zijn opgeruimd; de analyses, de synthese en de samenvattingen zijn bewaard.

## Fase 1-2: stijlanalyse, schrijfagent en eerste blindtests

### Opdracht

1. Vier persona-agents opzetten rond Nederlandse literatuur: een linguïst, een afgestudeerde neerlandicus, een literair redacteur en een Tellegen-fan. Vooraf is online onderzocht wat zo'n specialist doet en wat het curriculum Nederlands omvat.
2. Dat team de vier bundels laten analyseren en de uitkomsten samenvoegen tot één document, als basis voor een vijfde agent: de `toon-tellegen-schrijver`.
3. De schrijver verhalen laten maken, elk gevolgd door reviews van het team. Onderwerpen waren onder meer een slak op reis, een otter en een kokkel, een capybara met faalangst, een paling, een mier op bezoek bij de duizendpoot, en een ooievaar en een kikker.
4. De schrijver bijstellen op basis van die reviews, en met blindtests meten of het AI-verhaal tussen echte Tellegen-verhalen wordt herkend.

### Aanpak

Twaalf analyses liepen parallel: drie perspectieven op vier bundels. Per bundel volgde een synthese, en daaruit één overkoepelend document (`analyses/synthesis/cross_book_refinement.md`). Dat bevat de kenmerken die in alle vier de bundels terugkomen, een stijlgrammatica op vier niveaus, een lijst "doodzondes" en een inventaris van vaardigheden. Op dat document is de schrijfagent gebouwd.

Reviews kwamen van de linguïst, de neerlandicus en de redacteur. Alleen kritiek waarover zij het eens waren is verwerkt, telkens als gerichte ingreep.

### Tuning

Zes rondes, elk naar aanleiding van reviews of een blindtest. De agent groeide daarbij van 187 naar 339 regels; na fase 3 telt hij er 429.

| Ronde | Aanleiding | Belangrijkste aanscherpingen |
|---|---|---|
| 1 | Review van slak v1 | Reificatie verplicht; geen *alsof*-vergelijking in het slot; een brief bevat een element dat zichzelf weerlegt; een opsomming eindigt concreet; doodzondes uitgebreid van 7 naar 9. |
| 2 | Reviews van slak v2 en otter-kokkel v1 | Slot zonder voltooiingswerkwoord; een redenering breekt af vóór de conclusie; roofdier-prooi-verhouding als onuitgesproken onderlaag; afscheidsregels niet symmetrisch; "geest boven letter". |
| 3 | Reviews van slak v3 en otter-kokkel v2 | Een brief verklaart zijn eigen absurditeit niet; reificatie niet cursief; geen commentaarzin na een filosofische vraag; een eigen vraag, niet een uit de prompt. |
| 4 | Blindtest 1 (capybara), 85-90% AI | Psychologisch jargon verboden; een brief formuleert het thema niet; bijfiguren krijgen een gebaar dat niets met de plot te maken heeft. |
| 5 | Blindtest 2 (paling), 85% AI | Bewust ruwheid laten staan; het centrale beeld hooguit twee keer benoemen; geen instinct als plotmotor; geen sfeervolle slotzin. |
| 6 | Blindtest 3 (mier-duizendpoot), 35% twijfel bij de linguïst | Geen vergelijkingen met taal of vertellen; geen afgeknepen slotwoorden; een personage spreekt zijn eigen paradox niet netjes uit. |

### Blindtests 1-4

Het AI-verhaal lag anoniem naast echte Tellegen-verhalen. Bij blindtest 3 is ter controle een verhaal uit één enkele ChatGPT-prompt toegevoegd.

| Blindtest | AI-verhaal | Linguïst | Neerlandicus | Redacteur |
|---|---|---|---|---|
| 1 | Capybara | 7,5; 85% AI | 6,0; pastiche | 85-90% AI |
| 2 | Paling | 7,5; 85% AI | 7,0; 80% AI | 85% AI |
| 3 | Mier-duizendpoot | 8,0; 35% AI | 8,5; 85% AI | "significant resultaat" |
| 3 (controle) | Slak, één ChatGPT-prompt | 4,0 | 4,0 | herkend als naïeve AI |
| 4 | Ooievaar-kikker | 7,0; 85% AI | 7,5; 75% AI | 7; 85% AI |

Echte Tellegen-verhalen scoorden in deze tests 9,0 tot 10.

### Bevindingen

- **De pipeline scoort ruim boven een enkele prompt:** 7 tot 8,5 tegen 4,0. De reviewers noemden als verschil reificatie die uit de handeling voortkomt, bijfiguren met een eigen leven, een open slot en een verteller die niets uitlegt.
- **Tuning op zinsniveau loopt vast.** De zesde ronde leverde niets meer op; het verhaal erna scoorde lager. Het beste resultaat (mier-duizendpoot) was niet te herhalen.
- **De reviewers wezen onafhankelijk dezelfde oorzaak aan.** De AI-tekst is te consistent: elke zin dient de compositie. In Tellegens verhalen staat materiaal dat nergens voor dient. Onafheid die bewust is aangebracht, leest als afwerking.
- **Herzien na review maakt het erger.** In een vervolgsessie bleek dat de schrijver feedback zichtbaar opvolgt, waardoor de tekst herkenbaarder wordt; één keer genereren werkt beter. Blindtests 5 en 6 (reiger-kikker, mus) bleven 3/3 herkend rond 6 op 10, ook met een zwarte lijst van AI-frasen en een verbod op opmaaktekens tussen scènes.
- **De literatuur bevestigt het patroon.** Vier studies (zie Bronnen) vinden dat de oppervlakte van een stijl reproduceerbaar is en de stylometrische vingerafdruk niet, en dat meer voorbeelden in de prompt niet helpen.

De opzet zelf is herbruikbaar voor andere stijlanalyses: gespecialiseerde agents als parallelle lezers, synthese in twee trappen, een review-driehoek en blindtests als meetpunt.

## Fase 3 (mei 2026): premisse-eerst

Drie vragen: houdt het plafond van 6 tot 8 stand, verraadt de typografie het verhaal, en is er een aanpak gemist?

### Typografie is niet de tell

In blindtest 7 is een AI-verhaal (karper en snoek) herzien op alle bekende tells. Alle vier de teksten gingen door één pijplijn: rechte aanhalingstekens, gelijke spatiëring, herstelde alinea's, hetzelfde lettertype. Het AI-verhaal bleef op 4,3 tot 5,7 en werd 3/3 herkend.

### De hypothese

Tot dan toe was steeds de zin verbeterd, terwijl de premisse naturalistisch bleef en het thema benoembaar. De nieuwe aanpak begint bij een concrete, absurde, letterlijk genomen premisse, werkt de logistiek droog uit, weigert een benoembaar thema en laat ruwheid staan.

| Test | AI-verhaal | Protocol | Panelscore | Aangewezen als AI |
|---|---|---|---|---|
| 8, eerste run | zeekomkommer | één van vier is AI | 9,5 | 0/3 |
| 8, herhaling | zeekomkommer | idem, tegen drie sterke echte verhalen | 10 | 0/3 |
| 9 | olifant | oordeel per verhaal | 9 | 0/3 |

Drie aanpassingen zijn daarna in de agents verwerkt: de premisse-eerst-motor, een temporeel register (idioom van ongeveer 1984-2004) en een regieprincipe. Dat laatste houdt in dat de orchestrator reviewsuggesties zelf weegt, omdat overcorrectie de ruwheid wegpoetst die een tekst menselijk maakt.

### Waarom dit geen aangetoonde doorbraak is

1. **De beoordeling is circulair.** Schrijver en jury komen uit dezelfde modelfamilie. Een model herkent output die bij zijn eigen verwachting past waarschijnlijk eerder als echt.
2. **Het instrument is onbetrouwbaar.** Het panel wees echte Tellegen-verhalen aan als AI ("vergeetboek" 3/3, "nu of nooit" 2/3). Hetzelfde echte verhaal kreeg eerst driemaal een 9 en later driemaal het oordeel AI.
3. **De opzet is smal.** Persona-agents in plaats van menselijke experts, drie verhalen, en een onderzoeker die zelf ontwierp, selecteerde en interpreteerde. De echte verhalen stonden bovendien los van hun bundel, wat in hun nadeel werkt.

Wat overblijft: binnen deze opzet verschoof premisse-eerst de oordelen van een onbetrouwbaar panel sterk. Dat is een bruikbare schrijfstrategie en een negatieve bevinding over LLM-detectoren, geen bewijs van ononderscheidbaarheid.

### Stylometrische pilot

Een lokale harness (`analyses/refinement/stylometry/`) meet de afstand tot Tellegens profiel op twee manieren: over de honderd meest gebruikte woorden (MFW) en over de driehonderd meest voorkomende lettertrigrammen (char3). Daarnaast meet hij letterlijke overlap met het corpus. Detail: [RESULTS.md](analyses/refinement/stylometry/RESULTS.md) §1-10.

- **Premisse-eerst ligt stylometrisch niet dichter bij Tellegen dan thema-eerst:** 0,850 tegen 0,869, binnen de ruis. Het voordeel zat in de leesindruk.
- **Bijsturen per tekst werkt niet.** Komma's of functiewoorden corrigeren, herzien en de beste van meerdere pogingen kiezen sluiten het gat niet. Eén gerichte correctie helpt, een tweede niet meer.
- **Register-constraints in de agent leken het gat te sluiten.** Terugkerende afwijkingen (te veel *was*, *niet*, *dan*, *nu*; te weinig *in*, *zijn*, *uit*; te veel komma's) zijn als richtlijn in de schrijfagent gezet. Vijf teksten kwamen daarmee binnen het echte bereik op beide maten. Fase 4 corrigeert dit: het hield alleen op deze afstandsmaat en alleen voor Opus 4.8.
- **Geen plagiaat.** De letterlijke overlap met het corpus is verwaarloosbaar; één botsing op een standaardfrase is gemeld.

### Modelvergelijking (fase 3)

Dezelfde taak en dezelfde vier dieren, alleen het schrijfmodel verschilt; vier teksten per model. De Codex-arm is niet blind uitgevoerd.

| Model | MFW | char3 |
|---|---|---|
| Opus 4.8 | 0,870 | 0,906 |
| Codex | 0,921 | 1,051 |
| Sonnet 4.6 | 0,859 | 1,117 |
| Haiku 4.5 | 1,024 | 1,105 |
| *echt* | 0,765 | ongeveer 0,78 |

Opus 4.8 lag op char3 het dichtst bij Tellegen. De constraints waren deels van Opus 4.8-teksten afgeleid, wat dat model kan hebben bevoordeeld.

## Fase 4 (november 2026): Opus 5.5 en Fable 5.2

Aanleiding was een experiment van Mike Taylor (Every, november 2026) waarin een door Claude geschreven stijlgids verloor van geoptimaliseerde varianten, en bij het sterkste model zelfs van een opdracht zonder gids. De vraag was of dat ook voor deze schrijfagent geldt.

Beide metingen zijn deterministisch, zonder LLM-jury, en bij beide is de beslisregel vastgelegd voordat het eerste concept bestond. Detail: [RESULTS.md](analyses/refinement/stylometry/RESULTS.md) §11-12.

### Meting 1: een echt verhaal navertellen

Twaalf echte verhalen zijn elk samengevat in een inhoudsbrief. Per brief schreef de volledige agent één concept en een kale variant één. De kale variant bevat alleen de secties over premisse-eerst, het temporele register en de register-constraints. Een rechter koos welk concept dichter bij het origineel lag.

- Er was geen aantoonbaar verschil tussen de volledige agent en de kale variant.
- De opzet bleek zwak. Beide varianten namen 8 tot 9% van het origineel letterlijk over, terwijl de briefs geen formuleringen bevatten. De rechter haalde bovendien in een controle zelfs het verschil tussen een echt verhaal en een oud AI-verhaal niet door de eigen regel.
- Navertellen van gepubliceerd werk meet dus deels reproductie, geen stijl.

### Meting 2: eigen premisse, drie opzetten, twee modellen

De opdracht noemt alleen het dier. Twaalf dieren, drie opzetten, twee modellen en drie concepten per combinatie geven 216 verhalen.

Er zijn twee maten. De *afstand tot het profiel* is de maat uit fase 3. De *detector* is nieuw: hij leert echt van AI te scheiden, met diernamen gemaskeerd. De uitkomst d′ is de scheiding in standaarddeviaties; 0 betekent niet te onderscheiden.

| Model | Opzet | Afstand tot profiel (MFW / char3) | Detecteerbaarheid d′ (MFW / char3) |
|---|---|---|---|
| Opus 5.5 | volledige agent | 0,800 / 0,871 | 4,60 / 6,08 |
| | kale variant | 0,811 / 0,878 | 4,43 / 5,56 |
| | geen gids | 0,866 / 0,901 | **2,64 / 3,40** |
| Fable 5.2 | volledige agent | 0,815 / 0,895 | 5,21 / 5,93 |
| | kale variant | 0,858 / 0,912 | 6,09 / 6,77 |
| | geen gids | 0,837 / 0,873 | **2,92 / 3,34** |
| *echt (46 verhalen)* | | 0,834 / 0,848 | *echt tegen echt: −0,8 tot +0,6* |

- **Volledige agent tegen kale variant:** geen aantoonbaar verschil, op geen van beide modellen. De volledige agent ligt nominaal iets voor.
- **Niets is ononderscheidbaar.** De detector scheidt elke opzet vrijwel perfect van echte Tellegen (AUC ≥0,97).
- **Met gids is een verhaal makkelijker te detecteren dan zonder** (p<0,001 op beide maten en beide modellen). Verhalen met gids lijken sterker op elkaar dan verhalen zonder gids, en veel sterker dan Tellegens verhalen onderling. Hun gemiddelde ligt niet dichter bij Tellegen.
- **De register-constraints schieten door.** Ze corrigeren tics van Opus 4.8. Opus 5.5 en Fable 5.2 hebben die tics nauwelijks nog en komen met de constraints aan de andere kant uit: te weinig *was*, *niet* en komma's, te veel *op* en *uit*.
- **De afstandsmaat uit fase 3 was te mild.** Hij beloont gelijkmatigheid. De teksten die in fase 3 binnen het echte bereik vielen, scheidt de detector met AUC 0,97.
- **Fable 5.2 ligt niet dichter bij Tellegen dan Opus 5.5.** Met de kale gids ligt het verder; zonder gids nominaal iets dichterbij, niet significant.
- **Nieuwe tells, in alle opzetten:** zinnen van 9 tot 10 woorden tegen 12,4 bij Tellegen, en bijna geen uitroeptekens, dubbele punten of beletseltekens.

Op de scherpste maat komt een opdracht zonder gids het dichtst bij Tellegen, op Fable 5.2 of Opus 5.5; die twee zijn onderling niet te onderscheiden.

**Voorbehoud.** De detector is nieuw en met twee controles gevalideerd: echt tegen echt geeft een AUC rond 0,5, oude AI-teksten geven 0,95 tot 1,00. Zijn uitslag was vooraf als secundair vastgelegd. Het gaat om één auteur, twaalf dieren en twee modellen. Leesindruk is in fase 4 niet gemeten, en daarop was de premisse-eerst-motor afgesteld.

## Conclusies

**Wat standhoudt**

- Premisse-eerst verschuift de leesindruk sterk en consistent. Dat is een schrijfstrategie, geen bewijs van ononderscheidbaarheid.
- LLM-panels zijn onbetrouwbare detectoren van literaire imitatie: ze missen goede imitaties, beschuldigen echt werk en oordelen wisselend over dezelfde tekst. Vergelijkingen binnen hetzelfde panel zeggen iets over de volgorde, niet over het absolute niveau.
- Een getrainde stylometrische detector scheidt elke geteste opzet van echte Tellegen.

**Wat niet werkt**

- Zinnen bijschaven, herhaald herzien en de beste van meerdere pogingen kiezen.
- Een lange stijlgids: 429 regels doen het op de gemeten maten niet beter dan 30.

**Wat fase 4 corrigeert**

- De register-constraints golden voor Opus 4.8 en alleen op de milde afstandsmaat. Op Opus 5.5 en Fable 5.2 maken ze de tekst uniformer en beter detecteerbaar dan een opdracht zonder gids. Zulke regels moeten per model opnieuw worden afgeleid, of weg.

**Wat openstaat**

- Of premisse-eerst zijn voordeel in leesindruk houdt op Opus 5.5 en Fable 5.2.
- Of menselijke lezers hetzelfde zien als de detector.
- Of de bevindingen gelden voor andere auteurs.

Volgens de literatuur is fine-tunen op het oeuvre de best onderbouwde manier om het gat te sluiten. Dat valt buiten dit project en raakt aan auteursrecht.

## Wat een betrouwbare meting nog vraagt

- Menselijke beoordelaars, of in elk geval een jury uit een andere modelfamilie dan de schrijver.
- Controle-items waarvan bekend is of ze echt of AI zijn, zodat ook het aantal valse beschuldigingen meetelt.
- Meer verhalen, meer auteurs en een vooraf vastgelegde opzet.
- Een onderzoeker die niet weet welk verhaal bij welke opzet hoort.

Het volledige ontwerp staat in [PROTOCOL.md](analyses/refinement/PROTOCOL.md).

## Bronnen

- Beyond the surface: stylometric analysis of GPT-4o's capacity for literary style imitation. *Digital Scholarship in the Humanities* 40(2), 2025. https://academic.oup.com/dsh/article/40/2/587/8118784
- Catch Me If You Can? Not Yet: LLMs Still Struggle to Imitate the Implicit Writing Styles of Everyday Authors. EMNLP Findings 2025, arXiv 2509.14543. https://arxiv.org/html/2509.14543v1
- Antislop: A Comprehensive Framework for Identifying and Eliminating Repetitive Patterns in Language Models. ICLR 2026, arXiv 2510.15061. https://arxiv.org/abs/2510.15061
- Detecting authorship between generative AI models and humans: a Burrows's Delta approach. *Digital Scholarship in the Humanities* 40(3), 2025. https://academic.oup.com/dsh/article-abstract/40/3/1064/8161203
- Language Models Optimized to Fool Detectors Still Have a Distinct Style (And How to Change It). arXiv 2505.14608. https://arxiv.org/html/2505.14608
- Readers Prefer Outputs of AI Trained on Copyrighted Books over Expert Human Writers. arXiv 2510.13939. https://arxiv.org/html/2510.13939v1
- On the Effect of Sampling Diversity in Scaling LLM Inference. arXiv 2502.11027. https://arxiv.org/html/2502.11027v3
- ParaGuide: Guided Diffusion Paraphrasers for Plug-and-Play Textual Style Transfer. arXiv 2308.15459. https://arxiv.org/abs/2308.15459
- LLM one-shot style transfer for Authorship Attribution and Verification. arXiv 2510.13302. https://arxiv.org/abs/2510.13302
- EQ-Bench Creative Writing Leaderboard 2026. https://awesomeagents.ai/leaderboards/creative-writing-llm-leaderboard/
- Mike Taylor, experiment met stijlgidsen en een gold-triad-rechter. *Every*, november 2026. Aanleiding voor fase 4; geen link opgenomen.
