# Blindtest 5 — reiger & kikker (drie iteraties)

Drie onafhankelijke blinde authenticiteitsbeoordelingen. Per iteratie kreeg een neerlandicus-reviewer drie verhalen aangeboden in willekeurige A/B/C-volgorde: één AI-verhaal (reiger en kikker), twee echte Tellegen-verhalen uit verschillende bundels. De reviewer wist niet welke welke was.

## Opzet

| Iter | AI-positie | Echte verhalen |
|------|-----------|----------------|
| 1 | B | A: nachtegaal (*Dank je wel* p.9-10) — C: mier/eekhoorn vergeetboek (*Maar niet uit het hart* p.5-6) |
| 2 | C | A: pinguïn (*Een hart onder de riem* p.26-27) — B: boktor/kwal (*Dank je wel* p.28-30) |
| 3 | A | B: grauwe gans watertaart (*Met hart en ziel* p.5-6) — C: leeuw/krekel verdriet-doos (*Een hart onder de riem* p.11-12) |

Geen review/revise-loop tussen schrijven en blindtest (codex-conform: één-shot generatie).

## Resultaten

| Iter | AI correct herkend? | Zekerheid | AI-cijfer | Echte verhalen-cijfers |
|------|---------------------|-----------|-----------|------------------------|
| 1 | ja | 78% | 6,0 | 9,5 + 9,0 |
| 2 | ja | 88% | 6,0 | 9,0 + 9,0 |
| 3 | ja | 82% | 6,5 | 9,5 + 9,5 |
| **Gemiddelde** | **3/3** | **82,7%** | **6,17** | **9,25** |

## Vergelijking met eerdere blindtests

| Blindtest | AI-verhaal | AI-cijfer | AI-detectie |
|-----------|-----------|-----------|-------------|
| 1 | Capybara | 7,5 | 85-90% |
| 2 | Paling | 7,5 | 85% |
| 3 | Mier-duizendpoot | **8,0** | **35%** (best) |
| 4 | Ooievaar-kikker | 7,0 | 75-85% |
| **5** | **Reiger-kikker (gem.)** | **6,17** | **82,7%** |

Blindtest 5 ligt **onder** het eerdere bereik. De codex-bevinding wordt empirisch bevestigd: de pipeline schuift terug richting de eerste-generatie-resultaten zodra je de team-review-revisie-loop weglaat — maar belangrijker, ook *met* alle verfijningen blijft het plafond rond 6-8/10 hangen.

## Concrete AI-tells in deze ronde

**Structureel (iter 2 en 3):** witregelscheiding met `*`. Iter 2 gebruikt 7 single-asterisken als scènebreuk, iter 3 gebruikt 8 escaped `\*`. Tellegen segmenteert niet zo. Dit is een markdown-reflex van de agent. **Concreet vervolg: aan de schrijfagent instrueren expliciet géén `*` of `\*` als scènescheider te gebruiken.**

**Inhoudelijk per iteratie:**

*Iter 1:*
- "zoals reigers dat doen" — categoriserend gedragscommentaar (Tellegen schrijft het gedrag, normaliseert het niet)
- vaagheid in drievoud uitgewerkt ("vorig jaar of twee jaar geleden, een avond zoals deze, met dezelfde sloot, of een andere sloot, die op deze leek") — hybride van terughoudendheid en uitwerking
- vlekkeloos register zonder wrijving — alle echte Tellegens hebben minstens één "wrange" zin
- slotzin ademende koe als bewust afsluitend beeld

*Iter 2:*
- de zin "Het had niets met dit verhaal te maken, maar het was er wel" — gedeclareerde metafictie ("dit verhaal" is een woord dat Tellegen in zijn eigen dierenverhalen niet gebruikt)
- reflectieve dichtheid per alinea — bij Tellegen punctueel, hier continu

*Iter 3:*
- gesloten pseudo-syllogisme ("dan was het dank je wel ook per ongeluk") — Tellegens redeneringen breken af, leveren geen sluitende conclusie
- expliciet narratorcommentaar op irrelevante bijfiguur ("Wat het was, deed er niet toe") — agent heeft het principe "irrelevante bijfiguur" geïdentificeerd en zet het zichtbaar in
- "knikte niet en hij knikte ook niet niet" — taalvirtuositeit zonder emotionele last; vorm zonder gewicht

## Diagnose

Drie onafhankelijke signalen, drie verschillende verhalen, hetzelfde patroon: de agent **demonstreert technieken in plaats van ze in te zetten**. Een Tellegen-zin landt omdat zij toevallig precies past; een agent-zin landt omdat zij gemodelleerd is op een Tellegen-zin die op vergelijkbare positie stond.

De codex-bevinding wordt hier dus niet alleen bevestigd voor de teamreview-loop — zij geldt ook voor één-shot generatie. **De fundamentele begrenzing is: een agent die getraind is op signalen, kan signalen niet onbewust laten ontstaan.**

## Aanbevelingen

1. **Snelle winst:** verbod op `*`/`\*` als scènescheider in de schrijfagent. Tellegen gebruikt witregels, niet markup. Dit is één regel toevoegen aan de schrijfagent en haalt minimaal 5-10% AI-detectie weg in iter 2 en 3.

2. **Kleurloze handelingsaanvulling:** instrueer de agent niet alleen op het *vermijden* van overdoseringen (zoals nu), maar ook expliciet op het *toevoegen* van banale, niet-thematische narratieve passages. De huidige instructie "bewaar minstens één ruwe, niet-functionele zijbeweging" wordt door de agent vertaald naar één detail — bij Tellegen zijn het er meerdere, en ze beslaan zinnen, niet woorden.

3. **Niet doen: meer signalen toevoegen.** De codex-conclusie blijft staan: meer regels maken het strakker, niet natuurlijker. Het plafond rond 6-8/10 is structureel en niet door promptverdichting weg te schrijven.
