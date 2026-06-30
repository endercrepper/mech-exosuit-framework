"""Section 8: Bilanciamento — Caso Pilota Patriot"""

from reportlab.platypus import Spacer


def build_section_08(story, ctx):
    h = ctx['heading']; so = ctx['section_opener']
    body = ctx['body']; bl = ctx['bullet_list']; cb = ctx['callout_box']
    dt = ctx['data_table']; cap = ctx['caption']
    P = ctx['Paragraph']; HR = ctx['HRFlowable']; KT = ctx['KeepTogether']
    
    story.extend(so('Capitolo 08 · Bilanciamento',
                    'Bilanciamento — Caso Pilota Patriot',
                    chapter_num=8))
    
    story.append(body(
        "Questa sezione presenta i valori di bilanciamento <b>completi</b> "
        "per la Patriot Exosuit come caso pilota. Gli stessi valori "
        "(con adattamenti) si applicheranno alle altre suit quando "
        "verranno aggiunte (AMP Suit, Mobile Dragon, ecc.). I numeri sono "
        "<b>valori di partenza</b>, pronti per essere tweakati durante il "
        "playtesting."
    , ctx['styles']['BodyLead']))
    
    # ── 8.1 Mech-exosuit stats ──
    story.append(P('<b>8.1 — Stat del mech-exosuit (Patriot)</b>',
                   ctx['styles']['H2']))
    
    story.append(body(
        "Le stat del mech-exosuit sono derivate direttamente dalla Patriot "
        "Exosuit originale di Aqued.Exosuits, con alcune modifiche per "
        "tener conto del fatto che non c'è un pawn umano a bordo (niente "
        "stat offset che dipendono dal pawn)."
    ))
    
    headers = ['Stat', 'Patriot originale', 'Patriot Mech-Exosuit',
               'Razionale']
    rows = [
        ['MaxHitPoints (mech)', '100 (apparel)',
         '300 (pawn)', 'Pawn ha HP propio + armor; +200 per durabilità'],
        ['ArmorRating_Sharp', '1.70', '1.70',
         'Invariato'],
        ['ArmorRating_Blunt', '1.80', '1.80',
         'Invariato'],
        ['ArmorRating_Heat', '1.50', '1.50',
         'Invariato'],
        ['MoveSpeed', '3.5 (offset)',
         '3.5 (base)', 'Non dipende più da pawn Moving capacity'],
        ['Mass', '100', '120',
         '+20 per il frame di supporto mech'],
        ['Insulation_Cold', '60', '60',
         'Invariato'],
        ['Insulation_Heat', '40', '40',
         'Invariato'],
        ['MarketValue', '~1500 (apparel)',
         '3500 (pawn)', 'Compreso subcore + materiali'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.25, 0.20, 0.20, 0.35]))
    story.append(cap('Tabella 8.1 — Stat del Patriot Mech-Exosuit rispetto alla Patriot Exosuit originale.'))
    
    # ── 8.2 Subcore HP per tier ──
    story.append(P('<b>8.2 — HP del subcore per tier</b>', ctx['styles']['H2']))
    
    story.append(body(
        "L'HP del subcore è <b>separato dall'HP del mech</b> ed è determinato "
        "dal tier del subcore installato. Standard ha 100 HP, High ha 175 "
        "HP. Questo valore è il 'punto di partenza' del subcore quando "
        "viene installato in un nuovo mech-exosuit."
    ))
    
    headers = ['Tier subcore', 'HP massimi', 'Soglia sopravvivenza (30%)',
               'HP dopo 1° recupero (es.)', 'HP dopo 2° recupero (es.)']
    rows = [
        ['Standard (SubcoreRegular)', '100', '30',
         '70 (da 100 residui × 0.7)', '49 (da 70 residui × 0.7)'],
        ['High (SubcoreHigh)', '175', '52',
         '122 (da 175 residui × 0.7)', '85 (da 122 residui × 0.7)'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.20, 0.15, 0.20, 0.25, 0.20]))
    story.append(cap('Tabella 8.2 — HP del subcore per tier e progressione di degrado. '
                      'Dopo 2-3 recuperi, il subcore diventa troppo fragile per uso combat.'))
    
    # ── 8.3 Battery capacity ──
    story.append(P('<b>8.3 — Capacità della batteria</b>',
                   ctx['styles']['H2']))
    
    story.append(body(
        "La capacità della batteria dipende dal tier del subcore: i "
        "subcore High forniscono più energia grazie alla migliore "
        "efficienza computazionale (lore: il subcore High gestisce meglio "
        "il power management)."
    ))
    
    headers = ['Tier subcore', 'maxEnergyTicks', '~Durata gioco',
               'Ricarica completa', 'Consumo power bay']
    rows = [
        ['Standard', '36.000', '12 ore', '~3 ore gioco (5 W/tick)',
         '350 W'],
        ['High', '54.000', '18 ore', '~4.5 ore gioco (5 W/tick)',
         '350 W'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.18, 0.18, 0.20, 0.27, 0.17]))
    story.append(cap('Tabella 8.3 — Capacità della batteria per tier. '
                      'Il tempo di ricarica è lo stesso in entrambi i tier (5 W/tick).'))
    
    # ── 8.4 Crafting costs ──
    story.append(P('<b>8.4 — Costi di crafting</b>', ctx['styles']['H2']))
    
    story.append(body(
        "I costi di crafting del mech-exosuit includono i materiali del "
        "frame (identici alla Patriot originale) più il subcore (consumato) "
        "più componenti extra per il sistema di controllo mech."
    ))
    
    headers = ['Voce', 'Quantità', 'Note']
    rows = [
        ['SubcoreRegular (oppure SubcoreHigh)', '1',
         'Consumato alla gestazione, integrato come pilota'],
        ['Steel', '150',
         'Struttura del frame (come Patriot originale)'],
        ['Plasteel', '250',
         'Corazza del frame (come Patriot originale)'],
        ['Uranium', '50',
         'Contropesi per gambe (come Patriot originale)'],
        ['ComponentIndustrial', '10 (+8 originali = 18 totali)',
         '+2 per il sistema di controllo mech'],
        ['ComponentSpacer', '5',
         'Per il sistema di controllo mech (come Patriot originale)'],
        ['Work to make', '60.000 ticks (~8h gioco)',
         'Con 1 pawn crafter Crafting 8+'],
        ['Skill requirements', 'Crafting 8',
         'Come Patriot originale'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.30, 0.25, 0.45]))
    story.append(cap('Tabella 8.4 — Costo di gestazione del Patriot Mech-Exosuit. '
                      'Il subcore è il componente più costoso (deve essere prodotto a parte).'))
    
    # ── 8.5 Jobs supported ──
    story.append(P('<b>8.5 — Lavori sbloccati per suit</b>',
                   ctx['styles']['H2']))
    
    story.append(body(
        "I mech-exosuit <b>non possono fare qualsiasi lavoro</b>: per "
        "bilanciamento, ogni suit ha una lista definita di "
        "<code>supportedJobs</code> nel <code>MechExosuitExt</code>. La "
        "Patriot, essendo una suit da combat, supporta solo lavori "
        "violenti e di emergenza."
    ))
    
    headers = ['Job', 'Patriot Mech-Exosuit', 'Razionale']
    rows = [
        ['Violent (combat, hunting)', 'Sì',
         'La Patriot è una suit da combat'],
        ['Firefighter', 'Sì',
         'Le suit meccaniche possono trasportare estintori'],
        ['Construction', 'Sì (limitato)',
         'Solo costruzioni base (muri, pavimenti); niente craft fine'],
        ['Hauling', 'No',
         'La Patriot non ha slot per cargo; usare mini-mech per hauling'],
        ['Cleaning', 'No',
         'Troppo grande per pulire interni'],
        ['Growing', 'No',
         'Calpesta le colture'],
        ['Mining', 'No',
         'Non ha slot per drill'],
        ['Doctoring', 'No',
         'Non ha manipolatori fini'],
        ['Research', 'No',
         'Non ha slot per computer'],
        ['Art/Craft', 'No',
         'Manipolatori troppo rozzi'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.30, 0.25, 0.45]))
    story.append(cap('Tabella 8.5 — Lavori supportati dalla Patriot Mech-Exosuit. '
                      'Altre suit avranno liste diverse (es. Constructor Frame supporterà Construction e Hauling).'))
    
    # ── 8.6 Skill bonus ──
    story.append(P('<b>8.6 — Skill: sommatoria suit + subcore</b>',
                   ctx['styles']['H2']))
    
    story.append(body(
        "Le skill del mech-exosuit sono calcolate come <b>sommatoria "
        "della skill base della suit + bonus del subcore</b>. La skill "
        "base della suit è definita nel <code>MechExosuitExt</code> "
        "(valori predefiniti per la Patriot: Combat 12, Construction 6). "
        "Il bonus del subcore è 0 per Standard, +4 per High."
    ))
    
    headers = ['Skill', 'Patriot base', 'Con Subcore Standard',
               'Con Subcore High', 'Cap vanilla mech']
    rows = [
        ['Shooting', '12', '12', '16 (cap 20)',
         '8 (Pikeman)'],
        ['Melee', '8', '8', '12 (cap 20)',
         '10 (Centipede)'],
        ['Construction', '6', '6', '10 (cap 20)',
         '12 (Constructoid)'],
        ['Mining', '0', '0', '0',
         '15 (Tunneler)'],
        ['Cooking', '0', '0', '0',
         '0 (nessuno)'],
        ['Crafting', '0', '0', '0',
         '0 (nessuno)'],
        ['Animals', '0', '0', '0',
         '0 (nessuno)'],
        ['Medicine', '0', '0', '0',
         '0 (nessuno)'],
        ['Intellectual', '0', '0', '0',
         '0 (nessuno)'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.20, 0.18, 0.20, 0.22, 0.20]))
    story.append(cap('Tabella 8.6 — Skill del mech-exosuit. Con Subcore High, la Patriot '
                      'supera il Pikeman vanilla in Shooting (16 vs 8). Bilanciato dal costo subcore High.'))
    
    # ── 8.7 Survival formula in practice ──
    story.append(P('<b>8.7 — Formula di recupero in pratica</b>',
                   ctx['styles']['H2']))
    
    story.append(body(
        "La formula (HP_recuperati = HP_residui × 0.70, soglia 30%) "
        "genera i seguenti scenari pratici per un subcore Standard (max 100):"
    ))
    
    headers = ['Scenario', 'HP residui morte', 'Esito',
               'HP dopo recupero', 'Cicli riusciti cumulativi']
    rows = [
        ['Subcore nuovo, mech muore subito', '100', 'Sopravvive',
         '70', '1'],
        ['Subcore 70 HP, mech muore', '70', 'Sopravvive',
         '49', '2'],
        ['Subcore 49 HP, mech muore', '49', 'Sopravvive',
         '34', '3'],
        ['Subcore 34 HP, mech muore', '34', 'Sopravvive (sopra soglia 30)',
         '24', '4'],
        ['Subcore 24 HP, mech muore', '24', 'Distrutto (sotto soglia 30)',
         '—', '—'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.35, 0.15, 0.25, 0.13, 0.12]))
    story.append(cap('Tabella 8.7 — Progressione di degrado del subcore. '
                      'Un subcore Standard può sopravvivere a ~4 cicli di morte-recupero prima di essere distrutto.'))
    
    story.append(body(
        "Per il subcore High (max 175), la progressione è simile ma "
        "estesa: il subcore sopravvive a ~5-6 cicli prima di essere "
        "distrutto. Questo rende i subcore High significativamente più "
        "valuable, giustificando il costo superiore di crafting."
    ))
    
    # ── 8.8 Other suits ──
    story.append(P('<b>8.8 — Altre suit: template di bilanciamento</b>',
                   ctx['styles']['H2']))
    
    story.append(body(
        "Per le altre suit che verranno aggiunte (AMP Suit, Mobile Dragon, "
        "ecc.), applicare il seguente template:"
    ))
    
    story.append(bl([
        "<b>Stat meccaniche</b>: partire dai valori della suit originale (armor, move speed, HP) e moltiplicare l'HP ×3 per il passaggio da apparel a pawn",
        "<b>Costi crafting</b>: stessi materiali della suit originale + subcore + 2 ComponentIndustrial extra per il sistema di controllo mech",
        "<b>Skill base</b>: assegnare in base al ruolo (combat suit: Shooting/Melee alti; constructor suit: Construction alto; scout suit: MoveSpeed alto)",
        "<b>Jobs supportati</b>: in base al ruolo (combat: Violent+Firefighter; constructor: Construction+Hauling; scout: Violent+Cleaning)",
        "<b>Bandwidth cost</b>: 2-5 in base alla potenza (combat suit: 3-5; utility suit: 2-3)",
        "<b>Battery capacity</b>: 36.000 ticks per Standard, 54.000 per High (uniforme tra suit)",
    ]))
    
    story.append(cb(
        'Bilanciamento iterativo',
        'I valori in questa sezione sono <b>valori di partenza</b>, non finali. '
        'Playtesting continuo è essenziale: tenere traccia di quante volte '
        'un subcore viene distrutto, quanto dura un mech-exosuit in media, '
        'quanto spesso il giocatore usa l\'estrazione volontaria vs '
        'smontaggio. Aggiornare i valori nel file XML '
        '<code>MechExosuitExt</code> della suit e ricompilare.',
        color=ctx['colors']['accent']
    ))
    
    story.append(Spacer(1, 18))
