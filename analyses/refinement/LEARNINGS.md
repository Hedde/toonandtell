# Learnings — wat een Tellegen-imitatie wel en niet ononderscheidbaar maakt

*Geconsolideerde, zo wetenschappelijk mogelijke uitkomsten van de blindtest-experimenten (blindtest1-8). Elke blindtest: één AI-verhaal + drie echte Tellegens, blind voorgelegd aan een 3-koppig analytisch panel (linguïst, neerlandicus, redacteur — bewust zónder de toon-fan, die te bevooroordeeld is). Cijfers 0-10, plus AI-detectie en zekerheid.*

## 1. Meetresultaten (kerntabel)

| Test | AI-verhaal | Aanpak | AI-score (gem.) | Detectie | Zekerheid |
|------|-----------|--------|-----------------|----------|-----------|
| 7-R1 | karper & snoek | one-shot, prozagericht | 4,3 | 3/3 | 79% |
| 7-R2 | karper & snoek | +1 chirurgische revisie | 5,7 | 3/3 | 74% |
| 7-R3 | karper & snoek | +2e revisie, typografie genivelleerd | 4,7 | 3/3 | 81% |
| 8    | spitsmuis & pad | volledige review-loop + regie-restraint | 5,2 | 3/3 | 81% |
| **8-bewijs** | **zeekomkommer** | **premisse-eerste motor** | **9,5** | **0/3** | n.v.t. |
| **8-replicatie** | **zeekomkommer** | idem, tegen 3 *sterke* reals + verse panel | **10,0** | **0/3** | n.v.t. |

Echte Tellegens scoorden over de meeste tests 8,5-9,5. Twee opvallende uitzonderingen (zie §6): in zowel de bewijs- als de replicatietest wees het hele panel een écht Tellegen-verhaal ten onrechte als AI aan (3,0-5,5), terwijl het AI-verhaal als meest authentiek (#1) werd gerangschikt.

## 2. Wat NIET werkte

- **Prozapoetswerk op zinsniveau.** Tells repareren (over-explicitatie, gladde vergelijkingen, effect-herhaling, "in en uit, in en uit") verhoogde de score hooguit ~1 punt en verlaagde de detectie niet structureel. Reviewers verschoven naar diepere bezwaren.
- **Iteratief reviseren tot "alles klopt".** Elke revisieronde maakte de tekst *correcter* → uniformer → en die gladde consistentie werd zelf de tell ("te netjes", "te symmetrisch", "te afgerond", "geen scheve knik"). Over-optimalisatie is een AI-signaal.
- **Typografie als verklaring.** Toen alle vier teksten door één identieke pijplijn uniform werden getypografeerd (rechte aanhalingstekens, gelijke spatiëring, herstelde alinea's, geen small-caps), bleef de detectie 3/3 bij ~81%. Het waren dus nooit de leestekens; het is de tekst zelf.
- **Symmetrie/spiegeling als compositie.** Slot dat de openingszin echoot ("telde de dingen" → "telde niet meer"; "dunner aan de randen" → "voelde zijn randen") werd consequent als #1 structurele tell aangewezen.

## 3. Wat WEL werkte — de gap

De doorbraak (4-6 → 9,5; detectie 3/3 → 0/3) kwam niet van betere zinnen maar van een andere **generatieve motor**:

- **Premisse-eerst i.p.v. thema-eerst.** Begin bij een concrete, absurde, letterlijk-genomen premisse (de zeekomkommer wil niet óp maar ín de bodem liggen) en werk de logistiek deadpan uit. De gefaalde verhalen begonnen bij een *thema* (bestaansangst, verlies) en kleedden dat aan met dieren — dat is de AI-default en thematisch leesbaar.
- **Geen benoembaar thema.** Als de strekking in één zin navertelbaar is ("dit gaat over X"), is dat zelf de tell. Authentiek werk weigert de samenvatting; de betekenis is residu.
- **Deadpan-letterlijk, niet psychologisch.** Materialiseren, niet diagnosticeren; het dier reflecteert niet op zijn eigen toestand.
- **Bewust niet optimaliseren.** Commitment aan één rare zaak, niet-functionele zijbewegingen (de doornhaai met zijn jeukende schraapje; de garnaal die korrels keurt en niets meeneemt), open niet-circulair slot.

## 4. Twee dimensies die we eerst over het hoofd zagen

- **Temporeel register (diachroon).** Een tekst kan stijl en lexicon perfect treffen en tóch "uit de tijd" vallen op enkele woorden: post-2005 register-glijders ("aan de randen", hedging "wel ongeveer", afsluiter "gewoon"). Dit hoort primair thuis bij de schrijfagent (deel van Toons stem), geborgd door een diachrone reviewer-check, en bewaakt door de orchestrator als processtap. Stond aanvankelijk in geen enkele agent.
- **De rol van de orchestrator/regisseur.** Reviewers zijn analytisch en neigen naar over-correctie — ze poetsen exact de productieve ruwheid weg die menselijk maakt. De orchestrator moet per suggestie zelf oordelen en over-deterministische adviezen verwerpen. In blindtest 8 werden bewust slechts 2 van ~10 ronde-2-suggesties overgenomen; die terughoudendheid ís onderdeel van de kwaliteit. (Tegelijk eerlijk: enkele behouden elementen werden later toch als tell genoemd — de afweging blijft echt, niet mechanisch.)

## 5. Methodische borging van de blindheid

Verse subagents krijgen alleen hun systeemprompt + de taakprompt; ze erven het hoofdgesprek, de sleutel en de mapping niet. Bewijs van zuiverheid: exact 4 tool-aanroepen per reviewer (de 4 Reads), schone PDF-inhoud en -metadata, herhaalde positie-randomisatie, en reële onzekerheid (72-88%) met puur stilistische motivering. Hardste variant: opake bestandsnamen in een geïsoleerde map zonder sleutel of sprekende buurbestanden.

## 6. False positives — een validiteitsprobleem van de test zelf

In zowel de bewijs- als de replicatietest wees het voltallige panel een ECHT Tellegen-verhaal aan als de AI:
- Bewijs: het afscheidsverhaal "Ik moet op reis" (procedureel lezend buiten boekcontext) → 3,0-5,5, unaniem "AI".
- Replicatie: het canonieke "nu of nooit" (eekhoorn, bron van de modelzinnen *"wat is het omgekeerde van niets"*) → 4-5, unaniem "AI", met geciteerde openingszin — dus ondubbelzinnig een echt verhaal.

Dit is geen procesfout (alle bestanden inhoudelijk geverifieerd) maar een eigenschap van het testontwerp. Twee oorzaken:
1. **Forced single-choice.** "Precies één van vier is AI, wijs hem aan" dwingt het panel tot een keuze, óók als het alle vier authentiek acht; het offert dan het relatief zwakste/discursiefste verhaal.
2. **Overgeleerde detectieheuristieken.** De tells die het panel inmiddels hanteert (fysiologische emotie, "talloze gedachten", psychologische glossen als "zijn gedachten die wijzer waren dan hijzelf", aforistische slotgrap) komen werkelijk in Tellegens eigen discursieve verhalen voor. De detector misvuurt daardoor op authentiek werk.

Implicatie: de spectaculaire 0/3-detectie van de zeekomkommer weerspiegelt twee dingen tegelijk — (a) de premisse-eerste motor is echt sterk, reproduceerbaar tegen sterke én canonieke reals, en (b) de detector is te scherp afgesteld en heeft een hoge false-positive-rate op Tellegens psychologische register. Beide zijn waar.

## 7. Beter blindtest-protocol (aanbevolen)

De forced-choice moet vervangen worden door een signal-detection-opzet:
- **Onafhankelijk + absoluut per item.** Elke beoordelaar oordeelt per verhaal "echt of AI + waarschijnlijkheid", zonder te weten hoeveel AI-items er zijn (0-N). Zo komen sensitiviteit én specificiteit eruit.
- **Controle-items.** Neem bekende echte en (waar mogelijk) bekende AI-items mee om de false-positive-rate expliciet te meten.
- **Coöperatieve synthese als aparte tweede ronde.** Na de onafhankelijke oordelen mag een gemodereerde discussie volgen; rapporteer pre- én post-discussie, zodat het effect van overleg zichtbaar blijft. Discussie vervangt de onafhankelijke meting niet (risico van dominantie/groupthink).
- **Laat de beoordelaar de openingszin van elk verdacht item citeren** — voorkomt label-verwarring bij opake bestandsnamen (in run 8-bewijs verwisselden alle drie de labels, al klopte de inhoud).

## 8. Kanttekeningen

De zeekomkommer-uitkomst is gerepliceerd (twee runs, twee vergelijkingssets, twee verse panels) en is dus robuust qua richting. Maar "ononderscheidbaar" is mede-bepaald door de false-positive-neiging van de detector; een zuiverder protocol (§7) zou de echte ondergrens scherper meten. De kernconclusie blijft: de hefboom zit in de premisse-laag en het weigeren van thematische resolutie, niet in prozaverfijning.
