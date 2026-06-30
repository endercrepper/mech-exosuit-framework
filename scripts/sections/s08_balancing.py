"""Section 8: Bilanciamento — 5 Exosuit Pilota"""

from reportlab.platypus import Spacer


def build_section_08(story, ctx):
    h = ctx['heading']; so = ctx['section_opener']
    body = ctx['body']; bl = ctx['bullet_list']; cb = ctx['callout_box']
    dt = ctx['data_table']; cap = ctx['caption']
    P = ctx['Paragraph']; HR = ctx['HRFlowable']; KT = ctx['KeepTogether']
    
    story.extend(so('Capitolo 08 · Bilanciamento',
                    'Bilanciamento — 5 Exosuit Pilota',
                    chapter_num=8))
    
    story.append(body(
        "Questa sezione presenta i valori di bilanciamento per le "
        "<b>cinque exosuit</b> analizzate come casi pilota: Helldivers "
        "Patriot, AMP Suit, Mobile Dragon (frame PV-8 Zyklop), Pirate "
        "Brawnson e P-5000 Powered Work Loader. Per ciascuna suit sono "
        "definiti: stat meccaniche derivate dalla suit originale, costi "
        "di crafting, jobs supportati, skill base e bandwidth cost. I "
        "numeri sono <b>valori di partenza</b>, pronti per essere "
        "tweakati durante il playtesting."
    , ctx['styles']['BodyLead']))
    
    # ── 8.1 Overview suits ──
    story.append(P('<b>8.1 — Panoramica delle 5 exosuit supportate</b>',
                   ctx['styles']['H2']))
    
    story.append(cb(
        'Filosofia di bilanciamento',
        'Le stat meccaniche delle suit (armor, MoveSpeed, HP, slot di equipaggiamento) '
        'sono <b>identiche alle suit originali</b> — non vengono modificate da '
        '[Mod Name]. Questo garantisce che il flavor e il bilanciamento interno '
        'di ciascuna suit siano preservati. Le uniche tre variabili che '
        '[Mod Name] calibra sono: <b>(1) la durata della batteria</b> (Tabella 8.4), '
        '<b>(2) il costo in bandwidth</b> (Tabella 8.1 e 8.9), e <b>(3) il bonus skill</b> '
        'del subcore (Standard: +0, High: +4). '
        '<b>Il subcore High è uno trade-off</b>: fornisce più skill (+4) e più HP '
        '(175 vs 100), ma consuma più batteria (−25% durata) e più bandwidth '
        '(+1 rispetto a Standard). Questo riflette il fatto che un processore più '
        'potente è più abile ma anche più esigente — assorbe più energia e '
        'richiede più "attenzione" dal mechanitor.',
        color=ctx['colors']['accent']
    ))
    
    story.append(body(
        "Le 5 suit sono state scelte per coprire l'intero spettro di ruoli: "
        "combat pesante (Patriot), combat bilanciato (AMP), combat "
        "specializzato/veloce (Mobile Dragon), combat pesante alternativo "
        "(Pirate Brawnson) e utility (Powered Work Loader). Per ciascuna "
        "è indicato il mod di origine, il ruolo tematico e il tier di "
        "bilanciamento."
    ))
    
    headers = ['Suit', 'Mod di origine', 'Ruolo',
               'BW (Std)', 'BW (High)', 'Tier']
    rows = [
        ['EXO-45 Patriot', 'Aqued.Exosuits (Helldivers)',
         'Combat pesante (ranged)', '3', '4', 'Medio'],
        ['AMP Suit', 'Aoba.Exosuit.AMP',
         'Combat bilanciato (ranged + melee)', '3', '4', 'Medio'],
        ['PV-8 Zyklop (Mobile Dragon)', 'Aoba.DeadManSwitch.MobileDragoon',
         'Combat veloce (scout)', '3', '4', 'Avanzato'],
        ['PV-8R0N Brawnson (Pirate)', 'amiti.pirateexosuit',
         'Combat pesante alternativo (tank)', '4', '5', 'Alto'],
        ['P-5000 Powered Work Loader', 'Aoba.Exosuit.PowerLoader',
         'Utility (hauling + construction)', '2', '3', 'Base'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.20, 0.24, 0.26, 0.10, 0.10, 0.10]))
    story.append(cap('Tabella 8.1 — Panoramica delle 5 exosuit supportate. '
                      'Il bandwidth cost dipende dal tier del subcore installato: '
                      'High consuma +1 bandwidth rispetto a Standard ma fornisce +4 a tutte le skill.'))
    
    # ── 8.2 Confronto stat meccaniche ──
    story.append(P('<b>8.2 — Confronto stat meccaniche (tutte le suit)</b>',
                   ctx['styles']['H2']))
    
    story.append(body(
        "Le stat del mech-exosuit sono derivate dalla suit originale con "
        "queste regole: (1) HP moltiplicato ×3 per il passaggio da apparel "
        "a pawn, (2) armor e move speed invariati, (3) Mass +20 per il "
        "frame di supporto mech. La tabella sottostante confronta le stat "
        "di tutte e 5 le suit."
    ))
    
    headers = ['Suit', 'Mech HP', 'Armor Sharp', 'Armor Blunt', 'Armor Heat', 'MoveSpeed']
    rows = [
        ['Patriot', '300', '1.70', '1.80', '1.50', '3.5'],
        ['AMP', '320', '1.50', '1.40', '1.20', '3.8'],
        ['Mobile Dragon (PV-8)', '260', '1.20', '0.90', '0.90', '6.2'],
        ['Pirate Brawnson', '280', '1.60', '1.30', '0.70', '5.2'],
        ['Powered Work Loader', '400', '0.80', '0.70', '0.50', '2.8'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.28, 0.13, 0.14, 0.15, 0.13, 0.17]))
    story.append(cap('Tabella 8.2 — Stat meccaniche delle 5 mech-exosuit. '
                      'Il Powered Work Loader ha HP più alti per compensare l\'armor bassa (utility suit).'))
    
    # ── 8.3 Subcore HP per tier ──
    story.append(P('<b>8.3 — HP del subcore per tier (uniforme tra suit)</b>',
                   ctx['styles']['H2']))
    
    story.append(body(
        "L'HP del subcore è <b>separato dall'HP del mech</b> ed è determinato "
        "esclusivamente dal tier del subcore installato. È uniforme tra "
        "tutte le suit — il subcore è un componente standard vanilla, "
        "non dipende dalla suit che lo ospita."
    ))
    
    headers = ['Tier subcore', 'HP massimi', 'Soglia sopravvivenza (30%)',
               'HP dopo 1° recupero', 'HP dopo 2° recupero']
    rows = [
        ['Standard (SubcoreRegular)', '100', '30',
         '70 (da 100 residui × 0.7)', '49 (da 70 residui × 0.7)'],
        ['High (SubcoreHigh)', '175', '52',
         '122 (da 175 residui × 0.7)', '85 (da 122 residui × 0.7)'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.20, 0.15, 0.20, 0.25, 0.20]))
    story.append(cap('Tabella 8.3 — HP del subcore per tier. Indipendente dalla suit ospitante.'))
    
    # ── 8.4 Battery capacity per suit ──
    story.append(P('<b>8.4 — Capacità della batteria per suit × tier</b>',
                   ctx['styles']['H2']))
    
    story.append(body(
        "La capacità della batteria è <b>l'unico bilanciamento attivo</b> "
        "insieme al bandwidth cost e al bonus skill. Le stat meccaniche "
        "delle suit (armor, MoveSpeed, HP) sono <b>identiche alle suit "
        "originali</b> — non vengono modificate. La durata della batteria "
        "è calibrata in base a due fattori: <b>consumo energetico della "
        "suit</b> (MoveSpeed × massa × sistemi attivi) e <b>tier del "
        "subcore</b> (il subcore High assorbe più energia del Standard)."
    ))
    
    story.append(body(
        "Le suit da tank (armor alta + servomotori pesanti per melee) "
        "hanno il consumo più alto; le suit utility (lente, no combat "
        "systems) hanno il consumo più basso. Le suit scout veloci "
        "consumano molto per via dei motori ad alta potenza necessari "
        "per MoveSpeed elevata, anche se l'armor è bassa. <b>Il subcore "
        "High riduce la durata della batteria del ~25%</b> rispetto al "
        "Standard — il processore più potente assorbe più energia."
    ))
    
    headers = ['Suit', 'Standard (h gioco)', 'High (h gioco)',
               'Consumo power', 'Razionale consumo']
    rows = [
        ['Powered Work Loader', '18', '14', '300 W',
         'Basso: armor 0.80, MoveSpeed 2.8, niente combat systems'],
        ['Mobile Dragon (PV-8)', '10', '8', '400 W',
         'Medio-basso: armor bassa MA MoveSpeed 6.2 (motore potente)'],
        ['Patriot', '12', '9', '350 W',
         'Medio: armor alta 1.70, sistemi weapon pesanti (minigun/rocket)'],
        ['AMP', '12', '9', '350 W',
         'Medio: armor media 1.50, 4 slot weapon (ranged + melee)'],
        ['Pirate Brawnson', '9', '7', '400 W',
         'Alto: armor 1.60, tank puro con servomotori pesanti per melee'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.22, 0.12, 0.12, 0.14, 0.40]))
    story.append(cap('Tabella 8.4 — Durata batteria per combinazione suit × tier. '
                      'Il subcore High riduce la durata del ~25% (consumo energetico maggiore). '
                      'Il Powered Work Loader ha la durata maggiore (utility); '
                      'il Pirate Brawnson + High subcore la minore (7h).'))
    
    story.append(body(
        "Il <b>trade-off del subcore High</b> è quindi triplo: fornisce "
        "+4 a tutte le skill e +75 HP (175 vs 100), ma costa 1 bandwidth "
        "in più e riduce la durata della batteria del 25%. Il giocatore "
        "deve decidere se vale la pena per ogni singolo mech-exosuit "
        "che fielda — non è una scelta automatica."
    ))
    
    # ── 8.5 Crafting costs ──
    story.append(P('<b>8.5 — Costi di crafting per suit</b>',
                   ctx['styles']['H2']))
    
    story.append(body(
        "I costi di crafting includono: il subcore (consumato, Standard o "
        "High), i materiali del frame (identici alla suit originale), più "
        "2 ComponentIndustrial extra per il sistema di controllo mech. "
        "Il costo in lavoro è ~60.000 ticks (~8 ore gioco) per tutte le "
        "suit, con skill Crafting 8+ richiesta."
    ))
    
    headers = ['Suit', 'Steel', 'Plasteel', 'Uranium', 'Comp. Ind.', 'Comp. Sp.', 'Subcore']
    rows = [
        ['Patriot', '150', '250', '50', '18', '5', '1 Std/High'],
        ['AMP', '200', '300', '40', '15', '3', '1 Std/High'],
        ['Mobile Dragon (PV-8)', '180', '220', '80', '20', '4', '1 Std/High'],
        ['Pirate Brawnson', '220', '280', '60', '18', '4', '1 Std/High'],
        ['Powered Work Loader', '300', '100', '20', '15', '2', '1 Std/High'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.22, 0.10, 0.12, 0.12, 0.14, 0.12, 0.18]))
    story.append(cap('Tabella 8.5 — Costi crafting per suit. '
                      'Il Powered Work Loader ha meno plasteel/uranium ma più steel (utility, non combat).'))
    
    # ── 8.6 Jobs supported per suit ──
    story.append(P('<b>8.6 — Lavori supportati per suit</b>',
                   ctx['styles']['H2']))
    
    story.append(body(
        "I mech-exosuit <b>non possono fare qualsiasi lavoro</b>: per "
        "bilanciamento, ogni suit ha una lista definita di "
        "<code>supportedJobs</code>. Le suit da combat supportano solo "
        "lavori violenti e di emergenza; le utility supportano hauling e "
        "construction ma non combat avanzato."
    ))
    
    headers = ['Suit', 'Violent', 'Firefighter', 'Construction', 'Hauling', 'Mining']
    rows = [
        ['Patriot', 'Sì', 'Sì', 'Limitato', 'No', 'No'],
        ['AMP', 'Sì', 'Sì', 'Sì', 'No', 'No'],
        ['Mobile Dragon', 'Sì', 'Sì', 'No', 'No', 'No'],
        ['Pirate Brawnson', 'Sì', 'Sì', 'No', 'No', 'No'],
        ['Powered Work Loader', 'Limitato', 'Sì', 'Sì', 'Sì', 'Sì'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.26, 0.12, 0.14, 0.16, 0.14, 0.18]))
    story.append(cap('Tabella 8.6 — Jobs supportati per suit. '
                      'Il Powered Work Loader è l\'unica suit che supporta mining e hauling pieno.'))
    
    # ── 8.7 Skill matrix ──
    story.append(P('<b>8.7 — Skill: matrice suit × subcore</b>',
                   ctx['styles']['H2']))
    
    story.append(body(
        "Le skill del mech-exosuit sono calcolate come <b>sommatoria "
        "della skill base della suit + bonus del subcore</b>. Il bonus "
        "del subcore è 0 per Standard, +4 per High. La tabella mostra "
        "le 2 skill più rilevanti per ogni suit (con entrambi i tier "
        "di subcore)."
    ))
    
    headers = ['Suit', 'Skill principale', 'Con Std', 'Con High', 'Skill secondaria', 'Con Std', 'Con High']
    rows = [
        ['Patriot', 'Shooting', '12', '16', 'Melee', '8', '12'],
        ['AMP', 'Shooting', '10', '14', 'Melee', '10', '14'],
        ['Mobile Dragon', 'Shooting', '14', '18', 'Melee', '6', '10'],
        ['Pirate Brawnson', 'Melee', '14', '18', 'Shooting', '8', '12'],
        ['Powered Work Loader', 'Construction', '10', '14', 'Mining', '8', '12'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.20, 0.16, 0.08, 0.08, 0.16, 0.08, 0.08]))
    story.append(cap('Tabella 8.7 — Matrice skill: base suit + bonus subcore. '
                      'Il Pirate Brawnson è l\'unica suit con Melee come skill principale (tank role).'))
    
    # ── 8.8 Survival formula ──
    story.append(P('<b>8.8 — Formula di recupero (uniforme)</b>',
                   ctx['styles']['H2']))
    
    story.append(cb(
        'Formula di recupero (applicata a tutte le suit)',
        '<b>HP_recuperati = HP_residui_morte × 0.70</b><br/>'
        '<b>Soglia di sopravvivenza = 30% del max HP del subcore</b><br/><br/>'
        'La formula è <b>uniforme tra tutte le suit</b>: il subcore non '
        'sa quale suit lo ospitava, quindi la probabilità di sopravvivenza '
        'dipende solo dai suoi HP residui. Questo è coerente con il design '
        'principio: il subcore è il cervello, il mech è il corpo — la '
        'morte del corpo non influenza la sopravvivenza del cervello.',
        color=ctx['colors']['accent']
    ))
    
    story.append(body(
        "Esempio numerico per un subcore Standard (max 100 HP), applicato "
        "a qualsiasi suit:"
    ))
    
    headers = ['HP residui morte', 'Esito', 'HP dopo recupero', 'Cicli cumulativi']
    rows = [
        ['100 (intatto)', 'Sopravvive', '70', '1'],
        ['70', 'Sopravvive', '49', '2'],
        ['49', 'Sopravvive', '34', '3'],
        ['34 (appena sopra soglia)', 'Sopravvive', '24', '4'],
        ['24 (sotto soglia)', 'Distrutto', '—', '—'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.30, 0.22, 0.28, 0.20]))
    story.append(cap('Tabella 8.8 — Progressione di degrado di un subcore Standard. '
                      'Un subcore sopravvive a ~4 cicli di morte-recupero prima di essere distrutto.'))
    
    # ── 8.9 Bandwidth analysis ──
    story.append(P('<b>8.9 — Analisi bandwidth e bilanciamento</b>',
                   ctx['styles']['H2']))
    
    story.append(body(
        "Il costo in bandwidth dipende da <b>due fattori</b>: la suit "
        "(che definisce il valore base) e il tier del subcore installato "
        "(High aggiunge +1 al valore base). Le 5 suit sono posizionate "
        "rispetto ai mech vanilla in modo da essere alternative valide "
        "senza essere eccessivamente potenti. Confronto diretto:"
    ))
    
    headers = ['Tipo mech', 'BW (Std subcore)', 'BW (High subcore)',
               'Combat power', 'Note']
    rows = [
        ['Vanilla Lifter', '1', '—', 'Basso', 'Mini-mech utility'],
        ['Vanilla Constructoid', '2', '—', 'Basso', 'Mini-mech construction'],
        ['Vanilla Pikeman', '3', '—', 'Medio', 'Combat mech ranged'],
        ['Vanilla Centipede', '5', '—', 'Alto', 'Heavy combat mech'],
        ['ModName Powered Work Loader', '2', '3', 'Basso (utility)',
         'Equivalente a Constructoid; supporta anche hauling e mining'],
        ['ModName Patriot', '3', '4', 'Medio-alto',
         'Equivalente a Pikeman ma con loadout config (minigun/rocket)'],
        ['ModName AMP', '3', '4', 'Medio-alto',
         'Equivalente a Pikeman; versatile ranged + melee'],
        ['ModName Mobile Dragon', '3', '4', 'Medio-alto (scout)',
         'Equivalente a Pikeman; più veloce ma più fragile'],
        ['ModName Pirate Brawnson', '4', '5', 'Alto (tank)',
         'Equivalente a Centipede con subcore High; tank melee puro'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.26, 0.13, 0.13, 0.20, 0.28]))
    story.append(cap('Tabella 8.9 — Confronto bandwidth con mech vanilla. '
                      'Il subcore High aggiunge +1 a tutti i valori (più skill, più potenza, più attenzione del mechanitor).'))
    
    story.append(body(
        "Il Pirate Brawnson è l'unica suit che parte da bandwidth 4 — "
        "riflette il fatto che è un tank puro con armor Sharp 1.60 "
        "(secondo solo al Patriot) e HP helmet dedicato. Con subcore "
        "High arriva a 5, equivalente al Centipede vanilla — ma il "
        "Centipede ha anche ranged heavy, il Brawnson è melee-only. "
        "La Mobile Dragon è a 3 (non 4) perché la sua velocità "
        "(6.2 vs 3.5 Patriot) è bilanciata dall'armor molto più bassa "
        "(1.20 sharp vs 1.70 Patriot)."
    ))
    
    # ── 8.10 Suit-specific notes ──
    story.append(P('<b>8.10 — Note specifiche per suit</b>',
                   ctx['styles']['H2']))
    
    story.append(P('<b>Patriot (Helldivers)</b>', ctx['styles']['H3']))
    story.append(body(
        "Caso pilota principale del documento. Suit da combat ranged con "
        "slot per minigun/autocannon (destra) e rocket launcher (mount "
        "sinistro). Niente slot melee dedicato ma ha l'ability "
        "<code>Exosuit_Stomp</code> (danno 30 blunt, cooldown 400 ticks). "
        "La più bilanciata delle 5 suit — ottimo punto di partenza per "
        "playtesting."
    ))
    
    story.append(P('<b>AMP Suit (Avatar)</b>', ctx['styles']['H3']))
    story.append(body(
        "Suit versatile con 4 armi dedicate: AMP_WeaponRanged_SMG, _LMG, "
        "_FL (flamethrower), _PT (plasma), e AMP_WeaponMelee. Pattern "
        "di Def esemplare (vedi Sezione 3.2 come riferimento per "
        "implementare altre suit). Ha già un <code>Building_Wreckage</code> "
        "nel mod originale — possiamo riusarlo come base per il nostro "
        "Relitto Sigillato, riadattandolo con CompRelic."
    ))
    
    story.append(P('<b>Mobile Dragon (PV-8 Zyklop)</b>', ctx['styles']['H3']))
    story.append(body(
        "Suit veloce (MoveSpeed 6.2 vs 3.5 Patriot) con armor più bassa. "
        "5 frame disponibili nel mod originale (AT34, FA47, PF3, PV4, "
        "PV8) — per la v1.0 di [Mod Name] supportiamo solo PV8 (Zyklop), "
        "gli altri frame possono essere aggiunti in v1.1. PV8 ha helmet "
        "dedicato che riduce MoveSpeed di 0.2 (lore: il casco Zyklop ha "
        "sensori pesanti). Bandwidth 4 per compensare la velocità."
    ))
    
    story.append(P('<b>Pirate Brawnson</b>', ctx['styles']['H3']))
    story.append(body(
        "Tank puro: armor Sharp 1.60 (secondo solo al Patriot), Melee "
        "14 come skill principale (unico caso tra le 5 suit). Helmet "
        "dedicato con 120 HP. 3 frame disponibili (Brawnson, PPV4, "
        "Toothache) — Brawnson è il caso pilota per il ruolo tank. "
        "Bandwidth 5 (come Centipede vanilla) per bilanciare la "
        "tanking ability."
    ))
    
    story.append(P('<b>Powered Work Loader (P-5000)</b>', ctx['styles']['H3']))
    story.append(body(
        "L'unica suit utility del set. Nata per hauling e construction "
        "e mining — non è una suit da combat. Ha 3 tool dedicati: "
        "PWL_Tool_Welder (per construction/repair), PWL_Tool_Drill (per "
        "mining), PWL_Tool_Claw (per hauling e melee difensivo). "
        "Bandwidth 2 (la più bassa) perché il suo ruolo utility non "
        "crea squilibri tattici. HP alti (400) per compensare l'armor "
        "bassa. Perfetta per il giocatore che vuole un mech-exosuit "
        "per lavoro quotidiano, non per combat."
    ))
    
    # ── 8.11 Bilanciamento finale ──
    story.append(P('<b>8.11 — Sintesi di bilanciamento</b>',
                   ctx['styles']['H2']))
    
    story.append(body(
        "Le 5 suit coprono l'intero spettro di ruoli senza sovrapposizioni "
        "eccessive. Il giocatore che vuole fieldare tutti e 5 i tipi "
        "contemporaneamente consuma <b>15 bandwidth con subcore Standard</b> "
        "(3+3+3+4+2) oppure <b>20 bandwidth con subcore High</b> "
        "(4+4+4+5+3) — il doppio costo del High va valutato in base alle "
        "+4 skill e ai +75 HP extra per subcore."
    ))
    
    headers = ['Combinazione (tutti Std subcore)', 'BW tot.',
               'Combinazione (tutti High subcore)', 'BW tot.']
    rows = [
        ['Powered Work Loader da solo', '2',
         'Powered Work Loader (High)', '3'],
        ['Patriot + Powered Work Loader', '5',
         'Patriot (High) + Powered Work Loader (High)', '7'],
        ['2× Patriot + Powered Work Loader', '8',
         '2× Patriot (High) + Powered Work Loader (High)', '11'],
        ['Patriot + AMP + Mobile Dragon', '9',
         'Patriot + AMP + Mobile Dragon (tutti High)', '12'],
        ['Pirate Brawnson + Patriot + Powered Work Loader', '9',
         'Brawnson + Patriot + PWL (tutti High)', '12'],
        ['Tutte e 5 le suit', '15',
         'Tutte e 5 le suit (tutti High subcore)', '20'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.34, 0.10, 0.34, 0.10]))
    story.append(cap('Tabella 8.10 — Combinazioni tattiche e bandwidth totale. '
                      'Con tutti High subcore, il totale saliva da 15 a 20 bandwidth (richiede mechanitor molto avanzato).'))
    
    story.append(cb(
        'Bilanciamento iterativo',
        'I valori in questa sezione sono <b>valori di partenza</b>, non finali. '
        'Playtesting continuo è essenziale: tenere traccia di quante volte '
        'un subcore viene distrutto per suit (le suit veloci come Mobile Dragon '
        'potrebbero essere soggette a più colpi subcore), quanto dura un mech-exosuit '
        'in media per suit, e quanto spesso il giocatore usa l\'estrazione volontaria. '
        'Aggiornare i valori nei file XML MechExosuitExt di ciascuna suit e ricompilare.',
        color=ctx['colors']['accent']
    ))
    
    story.append(Spacer(1, 18))
