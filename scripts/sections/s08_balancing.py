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
        'del subcore. '
        '<b>Tre tier di subcore</b> sono supportati, ciascuno con un trade-off diverso: '
        '<b>Standard</b> (base, +0 skill, BW base, battery base), '
        '<b>High</b> (+4 skill, +75 HP, +1 BW, −25% battery), e '
        '<b>Persona AI</b> (+8 skill, +150 HP, +2 BW, +25% battery). '
        'Il Persona AI è l\'unico tier che <b>migliora</b> la durata della batteria '
        'rispetto al Standard — la sua vera intelligenza ottimizza dinamicamente '
        'il consumo energetico. Tuttavia costa più bandwidth di tutti perché '
        'il mechanitor deve gestire un\'entità senziente.',
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
               'BW (Std)', 'BW (High)', 'BW (AI)', 'Tier']
    rows = [
        ['EXO-45 Patriot', 'Aqued.Exosuits (Helldivers)',
         'Combat pesante (ranged)', '3', '4', '5', 'Medio'],
        ['AMP Suit', 'Aoba.Exosuit.AMP',
         'Combat bilanciato (ranged + melee)', '3', '4', '5', 'Medio'],
        ['PV-8 Zyklop (Mobile Dragon)', 'Aoba.DeadManSwitch.MobileDragoon',
         'Combat veloce (scout)', '3', '4', '5', 'Avanzato'],
        ['PV-8R0N Brawnson (Pirate)', 'amiti.pirateexosuit',
         'Combat pesante alternativo (tank)', '4', '5', '6', 'Alto'],
        ['P-5000 Powered Work Loader', 'Aoba.Exosuit.PowerLoader',
         'Utility (hauling + construction)', '2', '3', '4', 'Base'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.20, 0.22, 0.24, 0.09, 0.09, 0.08, 0.08]))
    story.append(cap('Tabella 8.1 — Panoramica delle 5 exosuit supportate. '
                      'Il bandwidth cost dipende dal tier del subcore installato: '
                      'High consuma +1 BW (ma +4 skill, −25% battery); '
                      'Persona AI consuma +2 BW (ma +8 skill, +25% battery).'))
    
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
        "non dipende dalla suit che lo ospita. Il tier Persona AI usa un "
        "<b>nuovo ThingDef custom</b> (<code>ModName_SubcorePersonaAI</code>) "
        "creato dalla mod a partire da un Persona Core vanilla."
    ))
    
    headers = ['Tier subcore', 'HP massimi', 'Soglia sopravvivenza (30%)',
               'HP dopo 1° recupero', 'HP dopo 2° recupero']
    rows = [
        ['Standard (SubcoreRegular)', '100', '30',
         '70 (da 100 residui × 0.7)', '49 (da 70 residui × 0.7)'],
        ['High (SubcoreHigh)', '175', '52',
         '122 (da 175 residui × 0.7)', '85 (da 122 residui × 0.7)'],
        ['Persona AI (ModName_SubcorePersonaAI)', '250', '75',
         '175 (da 250 residui × 0.7)', '122 (da 175 residui × 0.7)'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.28, 0.12, 0.16, 0.22, 0.22]))
    story.append(cap('Tabella 8.3 — HP del subcore per tier. Il Persona AI è il più resistente '
                      'e sopravvive a ~5 cicli di morte-recupero (vs ~4 del High, ~4 dello Standard).'))
    
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
        "subcore</b>."
    ))
    
    story.append(body(
        "Le suit da tank (armor alta + servomotori pesanti per melee) "
        "hanno il consumo più alto; le suit utility (lente, no combat "
        "systems) hanno il consumo più basso. Le suit scout veloci "
        "consumano molto per via dei motori ad alta potenza necessari "
        "per MoveSpeed elevata, anche se l'armor è bassa. <b>Il subcore "
        "High riduce la durata della batteria del ~25%</b> rispetto al "
        "Standard (processore più potente, più assorbimento). <b>Il "
        "Persona AI invece aumenta la durata del ~25%</b> rispetto al "
        "Standard — la sua vera intelligenza ottimizza dinamicamente il "
        "consumo energetico."
    ))
    
    headers = ['Suit', 'Std (h)', 'High (h)', 'Persona AI (h)',
               'Consumo power', 'Razionale consumo suit']
    rows = [
        ['Powered Work Loader', '18', '14', '22', '300 W',
         'Basso: armor 0.80, MoveSpeed 2.8, niente combat systems'],
        ['Mobile Dragon (PV-8)', '10', '8', '12', '400 W',
         'Medio-basso: armor bassa MA MoveSpeed 6.2 (motore potente)'],
        ['Patriot', '12', '9', '15', '350 W',
         'Medio: armor alta 1.70, sistemi weapon pesanti (minigun/rocket)'],
        ['AMP', '12', '9', '15', '350 W',
         'Medio: armor media 1.50, 4 slot weapon (ranged + melee)'],
        ['Pirate Brawnson', '9', '7', '11', '400 W',
         'Alto: armor 1.60, tank puro con servomotori pesanti per melee'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.22, 0.08, 0.09, 0.14, 0.13, 0.34]))
    story.append(cap('Tabella 8.4 — Durata batteria per combinazione suit × tier. '
                      'Persona AI = +25% vs Standard; High = −25% vs Standard. '
                      'Il Pirate Brawnson + High subcore ha la durata minore (7h); '
                      'il Powered Work Loader + Persona AI ha la durata maggiore (22h).'))
    
    story.append(body(
        "Il <b>trade-off dei tre tier</b> è quindi: "
        "<b>Standard</b> = base; "
        "<b>High</b> = +4 skill, +75 HP, +1 BW, −25% battery; "
        "<b>Persona AI</b> = +8 skill, +150 HP, +2 BW, +25% battery. "
        "Il giocatore deve decidere se vale la pena per ogni singolo "
        "mech-exosuit che fielda — non è una scelta automatica."
    ))
    
    # ── 8.4.1 Persona AI subcore crafting ──
    story.append(P('<b>8.4.1 — Crafting del Persona AI Subcore</b>',
                   ctx['styles']['H3']))
    story.append(body(
        "Il <code>ModName_SubcorePersonaAI</code> è un nuovo ThingDef "
        "custom creato dalla mod. Non esiste in vanilla — vanilla ha "
        "solo il <code>Persona Core</code> (usato per le ship AI). "
        "La nostra mod lo trasforma in un subcore mech-pilotable."
    ))
    
    headers = ['Componente', 'Quantità', 'Note']
    rows = [
        ['Persona Core (vanilla)', '1',
         'Item raro, drop da raid late game o quest reward'],
        ['SubcoreRegular (vanilla)', '1',
         'Usato come "contenitore" — fornisce la struttura fisica'],
        ['ComponentSpacer', '4',
         'Per i circuiti di interfaccia AI'],
        ['AI Persona Fragment (ModName)', '1',
         'Nuovo item custom — drop raro da mech-hostile AI'],
        ['Work to make', '120.000 ticks (~16h gioco)',
         'Con 1 pawn crafter Crafting 12+'],
        ['Skill requirements', 'Crafting 12',
         'Più esigente del High (Crafting 8)'],
        ['Recipe user', 'SubcoreEncoder (vanilla)',
         'Riutilizza il building vanilla'],
        ['Research prereq', 'ModName_AIPersonaSubcoreTech',
         'Nuovo nodo research, vedi Sezione 9'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.30, 0.25, 0.45]))
    story.append(cap('Tabella 8.4.1 — Costo crafting del Persona AI Subcore. '
                      'Il Persona Core vanilla è il componente più raro: limita la produzione di questo tier.'))
    
    story.append(body(
        "<b>Lore del Persona AI Subcore</b>: normalmente un Persona Core "
        "è usato per pilotare navi stellari — contiene un'AI senziente. "
        "La mod nostra permette di \"imbottigliare\" questa AI in un "
        "subcore mech-exosuit, ottenendo un pilota con vera intelligenza "
        "tattica (da cui le skill elevate e l'ottimizzazione dinamica "
        "dell'energia). Tuttavia, gestire un'entità senziente richiede "
        "più attenzione da parte del mechanitor (da cui il +2 BW). "
        "L'AI Persona Fragment è un drop raro da mech con AI (es. "
        "Centipede con AI core) — simboleggia il \"materiale di "
        "calibrazione\" necessario per sincronizzare il Persona Core "
        "con il frame mech-exosuit."
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
        "del subcore è +0 per Standard, +4 per High, +8 per Persona AI. "
        "<b>Il cap vanilla è 20</b> — valori che lo superano vengono "
        "troncati a 20. La tabella mostra la skill principale di ogni "
        "suit per tutti e 3 i tier."
    ))
    
    headers = ['Suit', 'Skill principale', 'Std (+0)', 'High (+4)',
               'Persona AI (+8)', 'Note']
    rows = [
        ['Patriot', 'Shooting', '12', '16', '20 (cap hit)',
         'Persona AI raggiunge il cap'],
        ['AMP', 'Shooting', '10', '14', '18',
         ''],
        ['Mobile Dragon', 'Shooting', '14', '18', '20 (capped from 22)',
         'Persona AI supererebbe il cap'],
        ['Pirate Brawnson', 'Melee', '14', '18', '20 (capped from 22)',
         'Persona AI supererebbe il cap'],
        ['Powered Work Loader', 'Construction', '10', '14', '18',
         ''],
    ]
    story.append(dt(headers, rows, col_ratios=[0.18, 0.18, 0.10, 0.10, 0.18, 0.26]))
    story.append(cap('Tabella 8.7 — Matrice skill principale: base suit + bonus subcore. '
                      'Cap vanilla = 20. 3 suit su 5 raggiungono il cap con Persona AI.'))
    
    story.append(P('<b>8.7.1 — Skill secondaria per suit</b>', ctx['styles']['H3']))
    story.append(body(
        "Ogni suit ha anche una skill secondaria rilevante. La tabella "
        "sotto mostra i valori per i 3 tier. Anche in questo caso, il "
        "cap vanilla di 20 viene applicato."
    ))
    
    headers = ['Suit', 'Skill secondaria', 'Std (+0)', 'High (+4)',
               'Persona AI (+8)', 'Note']
    rows = [
        ['Patriot', 'Melee', '8', '12', '16', ''],
        ['AMP', 'Melee', '10', '14', '18', ''],
        ['Mobile Dragon', 'Melee', '6', '10', '14', ''],
        ['Pirate Brawnson', 'Shooting', '8', '12', '16', ''],
        ['Powered Work Loader', 'Mining', '8', '12', '16', ''],
    ]
    story.append(dt(headers, rows, col_ratios=[0.18, 0.18, 0.10, 0.10, 0.18, 0.26]))
    story.append(cap('Tabella 8.7.1 — Matrice skill secondaria. '
                      'Nessuna suit raggiunge il cap di 20 sulla skill secondaria nemmeno con Persona AI.'))
    
    story.append(cb(
        'Implicazione del cap a 20',
        'Tre suit su cinque (Patriot, Mobile Dragon, Pirate Brawnson) raggiungono il cap di 20 '
        'sulla skill principale con Persona AI. Questo significa che il bonus skill del Persona AI '
        '(+8) è <b>parzialmente sprecato</b> per queste suit: il giocatore paga +2 BW e +25% battery '
        'per un bonus effettivo minore del previsto. Il Persona AI è quindi più efficiente per '
        'suit con skill base bassa (AMP, Powered Work Loader), dove il +8 si traduce in un miglioramento '
        'reale. Questo è un bilanciamento emergente: il giocatore deve scegliere con cura quale suit '
        'meriti il Persona AI.',
        color=ctx['colors']['accent2']
    ))
    
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
    
    headers = ['Tipo mech', 'BW (Std)', 'BW (High)', 'BW (AI)',
               'Combat power', 'Note']
    rows = [
        ['Vanilla Lifter', '1', '—', '—', 'Basso', 'Mini-mech utility'],
        ['Vanilla Constructoid', '2', '—', '—', 'Basso', 'Mini-mech construction'],
        ['Vanilla Pikeman', '3', '—', '—', 'Medio', 'Combat mech ranged'],
        ['Vanilla Centipede', '5', '—', '—', 'Alto', 'Heavy combat mech'],
        ['ModName Powered Work Loader', '2', '3', '4', 'Basso (utility)',
         'Equivalente a Constructoid; supporta anche hauling e mining'],
        ['ModName Patriot', '3', '4', '5', 'Medio-alto',
         'Equivalente a Pikeman ma con loadout config (minigun/rocket)'],
        ['ModName AMP', '3', '4', '5', 'Medio-alto',
         'Equivalente a Pikeman; versatile ranged + melee'],
        ['ModName Mobile Dragon', '3', '4', '5', 'Medio-alto (scout)',
         'Equivalente a Pikeman; più veloce ma più fragile'],
        ['ModName Pirate Brawnson', '4', '5', '6', 'Alto (tank)',
         'Con Persona AI = 6 BW (più del Centipede vanilla!)'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.25, 0.10, 0.10, 0.10, 0.18, 0.27]))
    story.append(cap('Tabella 8.9 — Confronto bandwidth con mech vanilla. '
                      'Il subcore High aggiunge +1 BW; il Persona AI aggiunge +2 BW. '
                      'Il Pirate Brawnson con Persona AI arriva a 6 BW, superando il Centipede vanilla.'))
    
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
    
    story.append(body(
        "<b>Il Persona AI è il primo caso in cui una nostra suit supera "
        "il Centipede vanilla in bandwidth cost</b> (Brawnson + Persona AI "
        "= 6 BW vs Centipede 5). Questo è bilanciato dal fatto che il "
        "Brawnson + Persona AI ha +8 skill (Melee 14→20, cap vanilla), "
        "+150 HP subcore, e +25% battery. È una forza tattica che il "
        "giocatore può fieldare solo se ha un mechanitor estremamente "
        "avanzato (richiede molti bandwidth boost)."
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
        "contemporaneamente consuma: <b>15 BW con subcore Standard</b> "
        "(3+3+3+4+2), <b>20 BW con subcore High</b> (4+4+4+5+3), oppure "
        "<b>25 BW con Persona AI</b> (5+5+5+6+4). L'ultimo scenario è "
        "possibile solo con un mechanitor con bandwidth massimizzato "
        "(bandwidth booster + multi-mechanitor setup)."
    ))
    
    headers = ['Combinazione (tutti stesso tier)', 'BW Std',
               'BW High', 'BW Persona AI']
    rows = [
        ['Powered Work Loader da solo', '2', '3', '4'],
        ['Patriot + Powered Work Loader', '5', '7', '9'],
        ['2× Patriot + Powered Work Loader', '8', '11', '14'],
        ['Patriot + AMP + Mobile Dragon', '9', '12', '15'],
        ['Pirate Brawnson + Patriot + Powered Work Loader', '9', '12', '15'],
        ['Tutte e 5 le suit (combo massima)', '15', '20', '25'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.46, 0.14, 0.18, 0.22]))
    story.append(cap('Tabella 8.10 — Combinazioni tattiche e bandwidth totale per tier. '
                      'Con tutti Persona AI, il totale arriva a 25 BW — richiede mechanitor con bandwidth massimizzato.'))
    
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
