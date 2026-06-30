"""Section 10: Roadmap MVP"""

from reportlab.platypus import Spacer


def build_section_10(story, ctx):
    h = ctx['heading']; so = ctx['section_opener']
    body = ctx['body']; bl = ctx['bullet_list']; cb = ctx['callout_box']
    dt = ctx['data_table']; cap = ctx['caption']
    P = ctx['Paragraph']; HR = ctx['HRFlowable']; KT = ctx['KeepTogether']
    
    story.extend(so('Capitolo 10 · Roadmap', 'Roadmap MVP', chapter_num=10))
    
    story.append(body(
        "Questa roadmap definisce le milestone di sviluppo di [Mod Name] "
        "in ordine di priorità e dipendenza. Ogni milestone ha una "
        "<b>definizione di done</b> chiara e un <b>set di task</b> "
        "ordinato. La roadmap è strutturata per permettere release "
        "incrementali: dopo M0 c'è già qualcosa di giocabile, anche se "
        "minimale."
    , ctx['styles']['BodyLead']))
    
    # ── 10.1 Milestones overview ──
    story.append(P('<b>10.1 — Panoramica milestone</b>', ctx['styles']['H2']))
    
    headers = ['ID', 'Nome', 'Stima ore', 'Dipendenze',
               'Definizione di done']
    rows = [
        ['M0', 'Hello World Mech', '8-12', '—',
         'PawnKindDef custom spawna in gioco, è un mech vanilla funzionante'],
        ['M1', 'Subcore Install', '12-18', 'M0',
         'CompSubcorePilot installato, HP tracking, SubcoreInfo bridge'],
        ['M2', 'Death & Relic', '16-24', 'M1',
         'Drop relitto su morte, smontaggio, recupero subcore deterministico'],
        ['M3', 'Bay Ibrida', '20-30', 'M2',
         'Edificio + ITab + 4 funzioni integrate'],
        ['M4', 'Batteria & Bandwidth', '10-15', 'M3',
         'Batteria scarsa, low power mode, bandwidth cost, patch charger'],
        ['M5', 'SubcoreInfo Integration', '6-10', 'M3',
         'Bridge via reflection testato in tutti i 4 punti (Tabella 7.1)'],
        ['M6', 'CE Compat', '8-12', 'M3',
         'Patch CE dedicata, testing con CE caricata'],
        ['M7', 'Polish & Bilanciamento', '20-40', 'M4, M5, M6',
         'Playtesting, tweak valori, documentazione, pubblicazione'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.06, 0.20, 0.10, 0.14, 0.50]))
    story.append(cap('Tabella 10.1 — Milestone ordinate per dipendenza. '
                      'Stima totale: 100-161 ore (~3-4 settimane full-time).'))
    
    # ── 10.2 M0 ──
    story.append(P('<b>10.2 — M0: Hello World Mech</b>', ctx['styles']['H2']))
    story.append(body(
        "Obiettivo: avere un mech custom spawna in gioco usando le Defs "
        "minime. Questo valida l'ambiente di sviluppo (riferimenti DLL, "
        "compilazione, caricamento mod) e crea la base su cui costruire."
    ))
    
    story.append(P('<b>Task M0</b>', ctx['styles']['H3']))
    story.append(bl([
        "Setup progetto Visual Studio / Rider con riferimenti a Assembly-CSharp.dll, UnityEngine.dll, Exosuit.dll, 0MultiplayerAPI.dll",
        "About.xml minimo (packageId, name, supportedVersions, modDependencies per Exosuit Framework + Harmony)",
        "LoadFolders.xml per 1.6 (e opzionalmente 1.5)",
        "ThingDef race custom (ParentName=\"BaseMechanoid\") con grafica placeholder",
        "PawnKindDef custom (ParentName=\"BaseMechanoidKind\")",
        "Test: spawn via dev mode, verifica che il mech appaia e sia selezionabile",
    ]))
    
    story.append(P('<b>Done M0</b>', ctx['styles']['H3']))
    story.append(body(
        "Il mech custom spawna in gioco, ha grafica visibile (anche solo "
        "un rettangolo colorato), può essere selezionato e mostra la "
        "scheda info vanilla. Non ha behavior custom, è solo un mech "
        "vanilla con grafica diversa."
    ))
    
    # ── 10.3 M1 ──
    story.append(P('<b>10.3 — M1: Subcore Install</b>', ctx['styles']['H2']))
    story.append(body(
        "Obiettivo: implementare il <code>CompSubcorePilot</code> in modo "
        "che un mech-exosuit possa 'ospitare' un subcore, tracciarne "
        "l'HP, e propagare l'identità via SubcoreInfoBridge."
    ))
    
    story.append(P('<b>Task M1</b>', ctx['styles']['H3']))
    story.append(bl([
        "Implementare CompSubcorePilot.cs + CompProperties_SubcorePilot.cs (Sezione 2.2.1)",
        "Aggiungere il Comp al ThingDef della race (Sezione 3.2)",
        "Implementare BodyDef custom con subcore come body part (Sezione 3.3)",
        "Implementare SubcoreInfoBridge.cs (Sezione 2.3) — solo stub per ora",
        "Implementare Harmony patch Patch_TakeDamage.cs per reindirizzare danno al subcore (Sezione 4.2.1)",
        "Test: spawnare mech-exosuit, installare subcore via dev mode, verificare HP tracking",
        "Test: SubcoreInfo installato, verificare che l'identità venga propagata",
    ]))
    
    story.append(P('<b>Done M1</b>', ctx['styles']['H3']))
    story.append(body(
        "Un mech-exosuit può essere generato con un subcore installato "
        "(via dev mode per ora), il subcore ha HP separati visibili nella "
        "scheda info, e quando il mech viene colpito alla body part "
        "'Subcore', l'HP del subcore si riduce invece di quello del mech."
    ))
    
    # ── 10.4 M2 ──
    story.append(P('<b>10.4 — M2: Death & Relic</b>', ctx['styles']['H2']))
    story.append(body(
        "Obiettivo: implementare il sistema di morte e drop del relitto, "
        "con smontaggio e recupero deterministico del subcore."
    ))
    
    story.append(P('<b>Task M2</b>', ctx['styles']['H3']))
    story.append(bl([
        "Definire ThingDef del Relitto Sigillato (Sezione 3.4) per la Patriot",
        "Definire ThingDef del Destroyed Subcore Standard e High (Sezione 3.5)",
        "Implementare CompRelic con logica CalculateSurvival() e CalculateRecoveredHP()",
        "Implementare JobDriver_DismantleRelic.cs (Sezione 2.2.5)",
        "Definire RecipeDef per smontaggio (Sezione 3.6)",
        "Implementare Harmony patch Patch_MechDeath.cs per intercettare la morte del mech e spawnare il relitto",
        "Aggiornare CompSubcorePilot con OnSubcoreDestroyed() e OnMechDeath()",
        "Test: uccidere mech-exosuit, verificare drop relitto, smontare, verificare esito deterministico",
        "Test: uccidere mech-exosuit con subcore a HP basso, verificare Destroyed Subcore",
    ]))
    
    story.append(P('<b>Done M2</b>', ctx['styles']['H3']))
    story.append(body(
        "Quando un mech-exosuit muore, droppa un Relitto Sigillato. Un "
        "pawn può smontare il relitto (200 ticks di lavoro) e ottenere: "
        "subcore recuperato con HP ridotti (se era sopra soglia) o "
        "Destroyed Subcore (se sotto soglia). SubcoreInfo propaga "
        "l'identità in entrambi i casi in cui il subcore sopravvive."
    ))
    
    # ── 10.5 M3 ──
    story.append(P('<b>10.5 — M3: Bay Ibrida</b>', ctx['styles']['H2']))
    story.append(body(
        "Obiettivo: implementare la Building_HybridGestator con le 4 "
        "funzioni integrate (loadout, gestation, charging, subcore "
        "install/extract)."
    ))
    
    story.append(P('<b>Task M3</b>', ctx['styles']['H3']))
    story.append(bl([
        "Definire ThingDef della Building_HybridGestator (Sezione 3.1)",
        "Implementare Building_HybridGestator.cs (Sezione 2.2.3)",
        "Implementare ITab_HybridBay.cs con le 5 sezioni UI (Sezione 5.2)",
        "Implementare HybridGestatorExt per le ricette supportate",
        "Definire RecipeDef per la gestazione della Patriot (Sezione 3.6)",
        "Implementare TryStartGestation() e CompleteGestation()",
        "Implementare charging tick (F3, Sezione 5.5)",
        "Implementare GetFloatMenuOptions per install/extract subcore (F4, Sezione 5.6)",
        "Patch XML per disabilitare i charger vanilla sui mech-exosuit (Sezione 5.5)",
        "Test: costruire bay, avviare gestazione, verificare spawn mech-exosuit",
        "Test: dockare mech-exosuit scarico, verificare ricarica",
        "Test: estrarre subcore, reinstallare, verificare HP preservati",
    ]))
    
    story.append(P('<b>Done M3</b>', ctx['styles']['H3']))
    story.append(body(
        "La bay ibrida è costruibile in gioco. Il giocatore può: "
        "costruire la bay, avviare la gestazione di un Patriot Mech-Exosuit "
        "(con Subcore Standard + materiali), ricaricare il mech-exosuit "
        "quando dockato, estrarre il subcore, reinstallarlo. L'ITab "
        "mostra tutte le 5 sezioni e funziona correttamente."
    ))
    
    # ── 10.6 M4 ──
    story.append(P('<b>10.6 — M4: Batteria & Bandwidth</b>', ctx['styles']['H2']))
    story.append(body(
        "Obiettivo: implementare il sistema di batteria scarsa con low "
        "power mode, e l'integrazione con bandwidth del mechanitor."
    ))
    
    story.append(P('<b>Task M4</b>', ctx['styles']['H3']))
    story.append(bl([
        "Implementare CompMechExosuitBattery.cs (Sezione 2.2.2)",
        "Aggiungere il Comp al ThingDef della race",
        "Implementare CompTick con consumo energia",
        "Implementare Notify_LowPower() con downed state",
        "Implementare Recharge() e integrazione con la bay (Sezione 6.3)",
        "Verificare che il mech-exosuit entri in control group del mechanitor (vanilla CompOverseerSubject)",
        "Verificare che il mech-exosuit vada dormant quando il mechanitor muore",
        "Definire bandwidthCost nel MechExosuitExt (default 3 per Patriot)",
        "Test: fieldare mech-exosuit per 12 ore, verificare low power mode",
        "Test: ricaricare nella bay, verificare ripristino",
    ]))
    
    # ── 10.7 M5-M7 ──
    story.append(P('<b>10.7 — M5, M6, M7: integrazioni e polish</b>',
                   ctx['styles']['H2']))
    
    story.append(P('<b>M5 — SubcoreInfo Integration</b>', ctx['styles']['H3']))
    story.append(bl([
        "Implementare tutti i 4 punti di chiamata al bridge (Tabella 7.1)",
        "Testare ciascun punto con SubcoreInfo caricata",
        "Testare ciascun punto senza SubcoreInfo (verifica no-op)",
    ]))
    
    story.append(P('<b>M6 — CE Compat</b>', ctx['styles']['H3']))
    story.append(bl([
        "Creare directory 1.6/CE/Patches/",
        "Scrivere Patch_MechExosuitCE.xml (Sezione 7.2.1)",
        "Definire BodyPartHealth CE per il subcore",
        "Testare con CE caricata: danno al subcore funziona con AP",
        "Testare senza CE: nessun regression",
    ]))
    
    story.append(P('<b>M7 — Polish & Bilanciamento</b>', ctx['styles']['H3']))
    story.append(bl([
        "Playtesting esteso: 3+ run di gioco complete con la mod",
        "Tweak valori di bilanciamento in base ai feedback (Sezione 8)",
        "Aggiungere texture custom per mech-exosuit, relitto, subcore distrutto",
        "Aggiungere supporto per altre suit (AMP Suit, Mobile Dragon) se richieste",
        "Scrivere Steam Workshop page (descrizione, screenshots, video)",
        "Pubblicazione v1.0",
    ]))
    
    # ── 10.8 Risk register ──
    story.append(P('<b>10.8 — Risk register (nota)</b>', ctx['styles']['H2']))
    story.append(body(
        "I principali rischi tecnici durante lo sviluppo, in ordine di "
        "probabilità:"
    ))
    
    story.append(bl([
        "<b>R1 — BodyDef custom non interagisce bene con CE</b>: mitigazione = testare con CE fin da M1, non aspettare M6",
        "<b>R2 — Harmony patch su TakeDamage conflitto con altre mod</b>: mitigazione = usare prefix patch non invasive, priorità bassa",
        "<b>R3 — SubcoreInfoBridge reflection fallisce in versioni future di SubcoreInfo</b>: mitigazione = catch eccezioni, fallback a no-op con log warning",
        "<b>R4 — ITab custom conflitto con ITab_Exosuit di Exosuit Framework</b>: mitigazione = usare tab name unico, evitare di subclassare ITab_Exosuit",
        "<b>R5 — Performance: troppi mech-exosuit causano lag</b>: mitigazione = testare con 10+ mech-exosuit in late game, ottimizzare CompTick se necessario",
    ]))
    
    story.append(Spacer(1, 18))
