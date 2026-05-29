# CLAUDE.md — Tellegen-imitatie & blindtest-pijplijn

Dit project onderzoekt wat een dierenverhaal *ononderscheidbaar van Toon Tellegen* maakt, via een meervoudige-agent-workflow: genereren → reviewen → reviseren → blind toetsen. Doel is educatief/methodisch (stijlonderzoek + agent-orchestratie), niet commercieel. Zie `analyses/refinement/LEARNINGS.md` voor de empirische uitkomsten en `analyses/refinement/PIPELINE.md` voor de operationele stappen.

## Agents (`.claude/agents/`)
- **toon-tellegen-schrijver** — schrijft de verhalen (premisse-eerste motor + temporeel register, zie hieronder).
- **linguist-nederlands** — fonologisch/syntactisch + diachrone register-check.
- **neerlandicus-afgestudeerd** — letterkundig + premisse-/themalegbaarheidstest.
- **redacteur-uitgeverij** — redactioneel + waakt tegen over-correctie.
- **toon-tellegen-fan** — bewust BUITEN het blindtest-panel (te bevooroordeeld).

## Bronnen & content-filter
De vier bron-PDF's staan één directory hoger (`../Toon_Tellegen-*.pdf`), legaal in bezit, educatief gebruik. **Kopieer geen verbatim Tellegen-tekst naar nieuwe bestanden via Write/Edit** (content-filter blokkeert dat). Echte verhalen extraheer je mechanisch met `pdftotext`; agents lezen rechtstreeks uit de PDF met `Read(pages=...)`.

## De gevalideerde stappen

### 1. Genereren — premisse-eerst (belangrijkste les)
Laat de schrijfagent NIET bij een thema beginnen maar bij een **concrete, absurde, letterlijk-genomen premisse**, deadpan uitgewerkt. Eisen: geen benoembaar thema (niet samen te vatten als "dit gaat over X"), niet psychologiseren, niet optimaliseren (één rare zaak vasthouden, niet-functionele ruwheid, open niet-circulair slot). Titelloos, incipit-dragend (Tellegen titelt losse verhalen niet). Temporeel register binnen ca. 1984-2004 (geen post-2005 register-glijders, anglicismen of archaïsme).

### 2. Review-loop (niet-blind)
Parallel panel (linguïst, neerlandicus, redacteur — ex toon-fan): vraag **chirurgische** suggesties, geen cijfers. Vanaf ronde 2 expliciet kaderen tegen oversturing: twee lijsten — noodzakelijke ingrepen vs. *handen af / productieve ruwheid*.

### 3. Regie (orchestrator beslist)
Neem suggesties NIET klakkeloos over. De orchestrator is regisseur: beoordeel elke aanbeveling, verwerp over-deterministische adviezen die ruwheid wegpoetsen, documenteer per ingreep je besluit. Over-correctie is zelf een AI-tell.

### 4. Verificatie + temporele check
Laatste panelronde (harde tells? over-gecorrigeerd?) plus een aparte diachrone register-controle. Drie niet-overlappende nitpicks = bodem bereikt → stoppen.

### 5. "De schoner" (normaliseren)
Normaliseer álle teksten identiek via `analyses/refinement/blindtest7/round3/normalize.py` (rechte aanhalingstekens, uniforme spatiëring, herstelde alinea's, hoofdletter-begin) en render via dezelfde `cupsfilter`-pijplijn. Zo kan typografie/leestekens niets verklappen — bewezen: dat was nooit de tell.

### 6. Blind toetsen
Vier teksten in een geïsoleerde map met OPAKE namen, geen sleutel/sprekende buurbestanden ernaast; verse panel-instanties; posities gerandomiseerd; verifieer zelf de bestandsinhoud vóór de test (lees ze). Laat beoordelaars de **openingszin** van elk verdacht verhaal citeren (voorkomt label-verwarring).
**Verbeterd protocol (aanbevolen, zie LEARNINGS §7):** vervang de forced-choice "precies één is AI" door onafhankelijke **absolute** per-item-oordelen (echt/AI + waarschijnlijkheid, aantal AI onbekend) + controle-items, met een optionele coöperatieve consensusronde als aparte tweede stap. Forced-choice veroorzaakt false positives op echte Tellegen.

## Kernbevindingen (samengevat)
- Prozapoetswerk en typografie-normalisatie verhogen de score nauwelijks (AI bleef ~5/10, detectie 3/3).
- **Premisse-eerst** brak het plafond: gerepliceerd 9,5-10/10, detectie 0/3, tegen sterke én canonieke echte verhalen.
- De detector heeft een hoge **false-positive-rate** op Tellegens discursieve/psychologische verhalen — lees detectiecijfers met dat voorbehoud.

## Meet-gedreven verbetering: constraints vs surgery (gevalideerd, RESULTS §9)
Na meting met de stylometrie-harness (MFW-Delta + held-out char-3-gram-Delta), splits afwijkingen:
- **Systematisch** (keert consistent terug over teksten: te veel was/niet/dan/nu, te weinig in/zijn/uit, komma-overmaat, lage variatie) → vastleggen als **register-constraints in `toon-tellegen-schrijver`** (generatie-tijd). Dit bracht in de test de baseline op béíde vingerafdruk-families binnen het Tellegen-bereik (incl. de held-out char3), confound-gecontroleerd.
- **Idiosyncratisch** (per tekst wisselend: zei/het/daar/naar) → hooguit **één** data-gedreven surgical pass; itereren plateaut (Goodhart).
Valideer op een held-out maat. Voorbehoud: gevalideerd op 2 families/onze harness/één auteur — geen ononderscheidbaarheids-claim voor neurale detectoren of mensen (zie PROTOCOL.md).
