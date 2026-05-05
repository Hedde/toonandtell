# Literatuurscan — wat de pipeline gemist heeft

Mei 2026. Vijf zoekopdrachten, drie diepteleesopdrachten. De relevante literatuur staat heel dichtbij ons probleem en biedt vier concrete aanknopingspunten die we nog niet benutten.

## Wat de literatuur empirisch bevestigt

Onze plafond-bevinding (6-8/10, AI altijd herkend) is geen idiosyncratische uitkomst van deze pipeline maar een algemeen patroon:

- **Oxford DSH 2025 (GPT-4o stylometrisch):** GPT-4o vangt oppervlakte-eigenschappen (zinslengte, woordlengte) goed, maar mist *Author Multilevel N-gram Profile*-features en lexicale diversiteit. Bij Hemingway-imitaties keerde GPT zelfs de oorspronkelijke diversiteitsvolgorde *om*. Conclusie: surface yes, signature no.

- **Catch Me If You Can — EMNLP 2025 findings:** few-shot prompting plateauert. *"Including more writing examples in the prompt affects the four metrics very little"*. Modellen defaulten naar generieke toon, blijven readily detectable. Hybrid prompting + finetuning is de aanbevolen route.

- **Burrows' Delta studies 2025:** AI-teksten clusteren *tight together*; menselijke teksten hebben veel grotere spreiding. >80% accuratesse om AI van mens te onderscheiden via z-scores van meest-frequente woorden, ook bij teksten van 100 woorden. **Dit verklaart waarom onze drie iteraties allemaal stuk gaan op vergelijkbare manieren — uniformiteit is de tell, niet een specifieke fout.**

- **EQ-Bench Creative Writing 2026:** Claude Opus 4.7 leidt. *"Voice consistency means a model needs to sustain that register across the whole piece, not just the first paragraph"*. Onze openingen zijn vaak goed; de middenstukken gaan zwabberen.

## Vier dingen die wij niet doen — die we wél kunnen doen

### 1. Antislop-style banned-list (ICLR 2026, sterkste vondst)

**Bron:** *Antislop: A Comprehensive Framework for Identifying and Eliminating Repetitive Patterns in Language Models* (ICLR 2026).

**Kerninzicht:** sommige LLM-fraseringen verschijnen >1000× zo vaak als in mensentekst. Voor Gemma-3-12b: de naam "Elara" 85.513× oververtegenwoordigd; trigram "heart hammered ribs" 1.192×. Antislop bouwt een sampler die deze patronen *bij inferentietijd* terugrolt zonder de vocabulaire te slopen.

**Wat wij kunnen doen, zonder fine-tuning:**
- Onze drie iter-verhalen + de vier eerdere blindtest-verhalen mijnen op hun eigen oververtegenwoordigde fraseringen ("hij dacht: misschien", "het was stil", "schelp op een kier", "drie vleugelslagen", "drempel", "thee", "zoethout"). Dat wordt een **expliciete blacklist** in de schrijfagent. Geen techniek, geen regel — alleen een lijst woorden/fraseringen die de agent moet vermijden.
- Concreet: corpus-vergelijking (AI-output vs echte Tellegen-corpus) per trigram. Frasen met >5× oververtegenwoordiging in AI-output → banned.
- Dit is een **structurele** aanpak die niet meer regels toevoegt maar concrete tells weghaalt. Aansluitend op de codex-conclusie ("geen nieuwe technieken meer toevoegen").

### 2. Stylometrische self-check als laatste pipeline-stap

**Bron:** *Detecting LLM-Generated Text with Trigram-Cosine Stylometric Delta* (Journal of Language and Education 2025) + Burrows' Delta studies.

**Kerninzicht:** AI-detectie werkt op meest-frequente-woorden z-scores. Een agent kan dezelfde test op zichzelf uitvoeren.

**Wat wij kunnen doen:**
- Een dunne *stylometric-checker*-agent toevoegen na de schrijfagent. Die berekent voor het concept: type-token ratio, zinslengte-variantie, en relatieve frequenties van een corpus van ~50 functiewoorden (de, het, en, maar, toen, niet, wel, ook, soms, eigenlijk, misschien). Vergelijkt met het Tellegen-baseline.
- Bij delta < threshold → *gewoon weergeven als signaal*, niet automatisch herzien (want revisie verergert het zoals codex aantoonde). Het signaal helpt de gebruiker beoordelen of een output gepubliceerd kan worden.
- Belangrijk: déze meting is *descriptief*, niet *prescriptief*. We meten alleen, we tunen er niet op terug — dat zou Goodhart's law triggeren.

### 3. Premise-first multi-step generatie (LessWrong creative-writing guide)

**Bron:** Practical guide *Creative writing with LLMs, part 1* (LessWrong).

**Kerninzicht:** *"An LLM defaults to the kind of prose the average reader might like — relatively simple characters and trope-heavy stories. Spend multiple messages brainstorming character dynamics, psychological contradictions, and thematic stakes BEFORE requesting scenes."*

**Wat wij kunnen doen:**
- Schrijfworkflow uitbreiden met een **pre-schrijf-stap**: agent genereert eerst 5-7 zinnen *premise-uitwerking* — wat dit dier vandaag ergens anders al heeft meegemaakt, een herinnering die wel in de tekst kan opduiken maar niet hoeft, een irrelevant detail uit gisteren. *Niet* in het verhaal opnemen — alleen als interne staat.
- Dan pas: het verhaal schrijven, met die premise als achtergrondgeheugen.
- Dit is geen extra techniek (codex-conform vermeden), maar een procedure-aanpassing die precies het door de literatuur gediagnosticeerde "default-to-average"-probleem aanpakt. De agent heeft *meer dan ze schrijft*, dus krijgt het verhaal surplus dat niet in de tekst zelf gegenereerd is.

### 4. Multi-temperatuur sampling met selectie

**Bron:** Antislop + algemene literatuur over diversiteitsverlies bij low-temp.

**Kerninzicht:** uniformiteit van AI-output is deels samplingproduct. Hogere temperatuur introduceert lexicale variabiliteit, lagere temperatuur breekt grammatica. **Drie drafts bij verschillende temperaturen, dan menselijke selectie of stylometric-checker-selectie**, vangt de spread die Burrows' Delta meet.

**Wat wij kunnen doen:**
- De volgende iteratie genereren als 3 parallelle drafts (bijv. T=0.7, 0.9, 1.1). De stylometric-checker (of jij als reviewer) kiest welke draft het dichtst bij Tellegen-spreiding zit.
- Dit kost driemaal de generatietijd maar geeft ons echte sampling-spread, niet kunstmatige.

## Wat we NIET moeten doen volgens literatuur (en eerder onderzoek)

- **Nóg meer technieken/regels toevoegen.** Bevestigd door codex én EMNLP 2025: prompt-uitbreiding plateauert.
- **Few-shot exemplars uitbreiden.** *"Including more writing examples affects the metrics very little"*.
- **Iteratieve revisie zonder onafhankelijke meting.** De codex-bevinding (revisie verergert detecteerbaarheid) is consistent met alle literatuur die zegt dat AI-output onder oogtoezicht *uniformer* wordt, niet diverser.

## De principiële begrenzing — door literatuur bevestigd

*"While LLMs have demonstrated remarkable proficiency in mimicking surface-level stylistic attributes, challenges remain in capturing subtler qualities of human writing, including innovation, deep causal reasoning, and authentic authorial voice"* (DSH 2025).

Dit dekt precies de drie convergerende reviewer-diagnoses uit `result.md` (linguïst: onregelmatigheden; neerlandicus: surplus dat niet in dienst staat; redacteur: een verhaal dat werkelijk niet weet hoe het eindigt). De plafond-diagnose van onze pipeline is dezelfde diagnose als die van het bredere veld.

**De enige route die de literatuur ziet om hieraan te ontkomen** — `hybrid prompting + finetuning` — is voor deze pipeline niet aangewezen: fine-tuning op Tellegen-corpus is auteursrechtelijk grijs en past niet bij het educatieve doel van het project.

## Aanbevolen volgende stap

Als je verder wil tunen, zou ik in deze volgorde gaan:

1. **Asterisk-verbod toevoegen aan agent.** *Klaar.*
2. **Antislop-mining op onze 7 AI-outputs.** Concrete blacklist genereren. Schat: 30-50 fraseringen die bovengemiddeld voorkomen.
3. **Stylometric-checker als descriptieve meting.** Eén nieuwe agent, één meting, geen feedback-loop.
4. **Premise-first procedure** in de schrijfworkflow.
5. **Pas dán** een nieuwe blindtest. Niet eerder — anders meten we ruis.

## Bronnen

- [Beyond the surface: stylometric analysis of GPT-4o's capacity for literary style imitation — Oxford Academic DSH](https://academic.oup.com/dsh/article/40/2/587/8118784)
- [Catch Me If You Can? Not Yet: LLMs Still Struggle to Imitate the Implicit Writing Styles of Everyday Authors — arXiv 2509.14543](https://arxiv.org/html/2509.14543v1)
- [Antislop: A Comprehensive Framework for Identifying and Eliminating Repetitive Patterns in Language Models — arXiv 2510.15061 (ICLR 2026)](https://arxiv.org/abs/2510.15061)
- [Stylometric comparisons of human versus AI-generated creative writing — Nature Humanities and Social Sciences Communications](https://www.nature.com/articles/s41599-025-05986-3)
- [Detecting authorship between generative AI models and humans: a Burrows's Delta approach — Oxford Academic DSH](https://academic.oup.com/dsh/article-abstract/40/3/1064/8161203)
- [Detecting LLM-Generated Text with Trigram-Cosine Stylometric Delta — Journal of Language and Education](https://jle.hse.ru/article/view/22211)
- [EQ-Bench Creative Writing Leaderboard 2026](https://awesomeagents.ai/leaderboards/creative-writing-llm-leaderboard/)
- [Creative writing with LLMs, part 1: Prompting for fiction — LessWrong](https://www.lesswrong.com/posts/D9MHrR8GrgSbXMqtB/creative-writing-with-llms-part-1-prompting-for-fiction)
