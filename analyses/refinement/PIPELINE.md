# Gevalideerde pijplijn — een Tellegen-verhaal genereren en blind toetsen

Dit is de werkwijze zoals die zich in blindtest7-8 heeft uitgekristalliseerd. Zie `LEARNINGS.md` voor de onderbouwing.

## Generatie
1. **Premisse-eerst.** Laat `toon-tellegen-schrijver` starten bij een concrete, absurde, letterlijk-genomen premisse — niet bij een thema. Deadpan logistiek, geen benoembaar thema, geen psychologisering.
2. **Temporeel register.** Binnen Tellegens venster (ca. 1984-2004); geen post-2005 register-glijders, anglicismen of geforceerd archaïsme.
3. **Titel.** Geen. Tellegen titelt losse dierenverhalen niet; ze openen met een kleinkapitaal-incipit (de openingswoorden zíjn de "titel"). Een verklarende titel is on-Tellegeniaans én een blindtest-tell.

## Review-loop (niet-blind, ter verbetering)
4. **Parallel panel** (linguïst, neerlandicus, redacteur — *ex* toon-fan): vraag CHIRURGISCHE suggesties, geen cijfers; in latere rondes expliciet kaderen tegen over-sturing (twee lijsten: noodzakelijke ingrepen vs. *handen af / productieve ruwheid*).
5. **Regie door de orchestrator.** Neem suggesties NIET klakkeloos over. Beoordeel elke aanbeveling; verwerp over-deterministische adviezen die ruwheid wegpoetsen. Documenteer per ingreep je besluit.
6. **Verificatie.** Een laatste panelronde: nog harde tells? Of juist over-gecorrigeerd? Drie niet-overlappende nitpicks = bodem van de smaak bereikt → stoppen.
7. **Temporele check** als aparte stap (diachroon, linguïst/neerlandicus).

## Toetsing (blind)
8. **"De schoner".** Normaliseer alle teksten identiek via `blindtest7/round3/normalize.py` (rechte aanhalingstekens, uniforme spatiëring, herstelde alinea's, hoofdletter-begin) en render via dezelfde `cupsfilter`-pijplijn. Zo kan typografie/leestekens niets verklappen.
   - Echte verhalen worden mechanisch uit de bron-PDF's gehaald (`pdftotext`), nooit door mij/agent verbatim overgetypt (content-filter + auteursrecht).
9. **Hardened blindtest.** Vier teksten in een geïsoleerde map met OPAKE namen, geen sleutel of sprekende buurbestanden ernaast. Drie verse panel-instanties, posities gerandomiseerd. Vraag per verhaal cijfer + verdict (welk is AI) + zekerheid + tells + ranglijst.
10. **Verifieer de mapping zelf** (lees de bestanden) voordat je conclusies trekt — reviewers wisselen opake labels weleens om; inhoud is leidend.

## normalize.py
Twee modi: `real` (ontwrapt pdftotext-output via eindleesteken + niet-volle-regel + dialoog-aanhalingsteken-heuristiek) en `canonical` (respecteert bestaande witregel-alinea's). Beide leveren dezelfde canonieke vorm.
