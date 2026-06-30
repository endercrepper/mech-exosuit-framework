"""Section 6: Batteria & Bandwidth"""

from reportlab.platypus import Spacer


def build_section_06(story, ctx):
    h = ctx['heading']; so = ctx['section_opener']
    body = ctx['body']; bl = ctx['bullet_list']; cb = ctx['callout_box']
    dt = ctx['data_table']; cap = ctx['caption']
    P = ctx['Paragraph']; HR = ctx['HRFlowable']; KT = ctx['KeepTogether']
    code_block = ctx['code_block']
    
    story.extend(so('Capitolo 06 · Batteria & Bandwidth',
                    'Batteria & Bandwidth', chapter_num=6))
    
    story.append(body(
        "Due sistemi regolano l'<b>operatività</b> dei mech-exosuit: la "
        "<b>batteria</b> (energia temporanea, si scarica con l'uso) e la "
        "<b>bandwidth</b> (risorsa permanente del mechanitor, limita il "
        "numero di mech simultanei). Entrambi sono <b>deliberatamente "
        "scarsi</b>: il giocatore non può spammarli, deve pianificare "
        "quando e dove attivarli."
    , ctx['styles']['BodyLead']))
    
    # ── 6.1 Battery ──
    story.append(P('<b>6.1 — Sistema batteria: design intenzionalmente scarso</b>',
                   ctx['styles']['H2']))
    
    story.append(body(
        "Il <code>CompMechExosuitBattery</code> traccia l'energia del "
        "mech-exosuit come valore normalizzato 0..1, con consumo di "
        "<code>1/maxEnergyTicks</code> per tick. Per default, "
        "<code>maxEnergyTicks = 36.000</code> (~12 ore di gioco a velocità "
        "normale), ma il valore è configurabile per-tier via XML: i "
        "subcore High estendono la batteria a 54.000 ticks (~18 ore)."
    ))
    
    headers = ['Tier subcore', 'maxEnergyTicks', '~Durata gioco',
               '~Durata reale (1x speed)', 'Note']
    rows = [
        ['Standard', '36.000', '12 ore', '20 minuti',
         'Mezza giornata di operatività'],
        ['High', '54.000', '18 ore', '30 minuti',
         'Estensione del 50% rispetto a Standard'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.18, 0.18, 0.18, 0.22, 0.24]))
    story.append(cap('Tabella 6.1 — Capacità della batteria per tier. '
                      'A velocità 3x (comune in late game), 12 ore gioco = ~7 minuti reali.'))
    
    story.append(body(
        "Quando l'energia arriva a 0, il mech va in <b>low power mode</b>: "
        "è downed (non può muoversi né attaccare), ma non è morto. Il "
        "giocatore riceve una notifica e un gizmo auto-attivato 'Ritorna "
        "alla bay' fa sì che il mech, appena diventa operativo (ad esempio "
        "per un pawn che lo ripara con chemfuel temporaneo), si muova "
        "verso la bay ibrida più vicina per ricaricarsi."
    ))
    
    # ── 6.2 Battery degradation ──
    story.append(P('<b>6.2 — Degradazione della batteria (meccanica opzionale)</b>',
                   ctx['styles']['H2']))
    story.append(body(
        "Per aumentare la profondità tattica, la batteria può subire "
        "<b>degradazione cumulativa</b>: ogni ciclo completo di "
        "scarica-ricarica riduce la <code>maxEnergyTicks</code> del 2%. "
        "Dopo 10 cicli, il mech-exosuit ha perso il 20% della capacità "
        "originale. Questo costringe il giocatore a non lasciare il mech "
        "sempre acceso-spento-acceso: l'usura si accumula."
    ))
    
    story.append(body(
        "La degradazione può essere <b>riparata</b> alla bay ibrida con "
        "un'operazione dedicata (costo: 4.000 ticks + 1 ComponentIndustrial "
        "+ 5 Chemfuel). Questo ripristina maxEnergyTicks al valore originale. "
        "La riparazione non ha costo in termini di maxHP del mech — è "
        "puramente una 'manutenzione' come cambiare l'olio."
    ))
    
    # ── 6.3 Power routing ──
    story.append(P('<b>6.3 — Routing della potenza elettrica</b>',
                   ctx['styles']['H2']))
    story.append(body(
        "La bay ibrida ha tre modalità operative con consumi diversi:"
    ))
    
    headers = ['Modalità', 'Consumo', 'Trigger']
    rows = [
        ['Idle', '50 W', 'Bay costruita ma nessun mech dockato, nessuna gestazione in corso'],
        ['Charging', '350 W', 'Mech-exosuit dockato con batteria < 100%'],
        ['Gestating', '200 W', 'Gestazione attiva (indipendente dal charging)'],
        ['Charging + Gestating', '550 W', 'Entrambi in corso contemporaneamente (raro ma possibile)'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.30, 0.20, 0.50]))
    story.append(cap('Tabella 6.2 — Modalità operative della bay e relativi consumi.'))
    
    story.append(body(
        "Se la rete elettrica non riesce a fornire la potenza richiesta, "
        "la bay entra in <b>brownout</b>: la ricarica e la gestazione "
        "vengono messe in pausa (non annullate), e il giocatore riceve "
        "una notifica. Questo rende la bay sensibile alla qualità della "
        "rete elettrica della colonia, specialmente in late game quando "
        "la bay è solo una dei tanti carichi."
    ))
    
    # ── 6.4 Bandwidth ──
    story.append(P('<b>6.4 — Bandwidth del mechanitor</b>', ctx['styles']['H2']))
    
    story.append(body(
        "I mech-exosuit <b>consumano bandwidth del mechanitor</b> come "
        "mech vanilla. Entrano a pieno titolo nel <b>control group</b> "
        "assegnato, e rispondono ai comandi del mechanitor (draft, work, "
        "follow, escort). Se il mechanitor muore o perde bandwidth "
        "(ad esempio per overdose di mechlink), i mech-exosuit assegnati "
        "vanno in <b>dormant mode</b>: sono downed, non possono operare, "
        "ma non muoiono. Quando un nuovo mechanitor viene assegnato (o "
        "viene liberata bandwidth), tornano operativi."
    ))
    
    story.append(P('<b>6.4.1 — Costo in bandwidth</b>', ctx['styles']['H3']))
    story.append(body(
        "Il costo in bandwidth è <b>configurabile per suit</b> via XML "
        "(modExtension <code>bandwidthCost</code>). Per la Patriot, il "
        "valore di default è <b>3 bandwidth</b> — equivalente a un "
        "mini-mech vanilla come il Lifter, nonostante il mech-exosuit sia "
        "molto più potente. Questo è bilanciato dal fatto che il mech-exosuit "
        "ha costi aggiuntivi (batteria, subcore fragile) che i mech vanilla "
        "non hanno."
    ))
    
    headers = ['Tipo mech', 'Bandwidth cost', 'Note']
    rows = [
        ['Vanilla Lifter', '1', 'Mini-mech, solo hauling'],
        ['Vanilla Constructoid', '2', 'Mini-mech, solo construction'],
        ['Vanilla Pikeman', '3', 'Combat mech'],
        ['Vanilla Centipede', '5', 'Heavy combat mech'],
        ['ModName Patriot Mech-Exosuit', '3', 'Configurabile via XML; default uguale a Pikeman'],
        ['ModName [altra suit]', '2-5', 'Da definire per suit; vedi Sezione 8'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.40, 0.20, 0.40]))
    story.append(cap('Tabella 6.3 — Costo in bandwidth rispetto ai mech vanilla. '
                      'Il mech-exosuit è bilanciato per essere un\'alternativa ai combat mech vanilla.'))
    
    # ── 6.5 Control group integration ──
    story.append(P('<b>6.5 — Integrazione con control group</b>',
                   ctx['styles']['H2']))
    story.append(body(
        "I mech-exosuit usano il sistema vanilla di <code>CompOverseerSubject</code> "
        "per l'assegnazione al mechanitor. Quando un mech-exosuit viene "
        "generato dalla bay, viene automaticamente assegnato al control "
        "group del mechanitor più vicino con bandwidth disponibile. Se "
        "nessun mechanitor ha bandwidth, il mech rimane in stato "
        "'unassigned' (downed) finché non viene liberata bandwidth."
    ))
    
    story.append(body(
        "Il giocatore può <b>cambiare control group</b> del mech-exosuit "
        "usando il gizmo standard 'Mech -> Assign to overseer' (vanilla). "
        "Quando il mech viene riassegnato, la bandwidth del vecchio "
        "mechanitor viene liberata e il nuovo mechanitor riceve il carico. "
        "Questo è importante se un mechanitor muore: il giocatore può "
        "riassegnare tutti i mech-exosuit a un altro mechanitor senza "
        "perderli."
    ))
    
    # ── 6.6 Battery + bandwidth synergy ──
    story.append(P('<b>6.6 — Sinergia batteria + bandwidth</b>',
                   ctx['styles']['H2']))
    
    story.append(body(
        "I due sistemi creano <b>doppio costo opportunità</b>: anche "
        "quando un mech-exosuit è in low power mode (batteria scarica), "
        "<b>continua a consumare bandwidth</b>. Questo significa che il "
        "giocatore non può 'mettere in pausa' un mech-exosuit quando è "
        "scarico per liberare bandwidth — il costo bandwidth è fisso "
        "finché il mech esiste."
    ))
    
    story.append(cb(
        'Perché questa sinergia è importante',
        'Senza questa regola, il giocatore potrebbe fieldare 10 mech-exosuit '
        'e tenerli in pausa (scarichi) finché non servono, pagando solo '
        'il costo di crafting. Con la regola, ogni mech-exosuit ha un costo '
        'opportunità permanente in bandwidth: anche scarichi, occupano '
        'slot del mechanitor. Questo costringe il giocatore a smontare '
        '(estrarre subcore) i mech-exosuit che non usa più, invece di '
        'accumularli. È coerente con il Pilastro 2 (tensione operativa) '
        'della Sezione 1.',
        color=ctx['colors']['accent2']
    ))
    
    story.append(body(
        "Il modo corretto di 'messa in pausa' di un mech-exosuit è "
        "<b>estrarre il subcore</b> (Sezione 5.6) e smontare il frame. "
        "Questo libera sia la bandwidth che il costo di mantenimento, "
        "ma costa lavoro e materiali per ricreare il frame in futuro. "
        "È un trade-off intenzionale."
    ))
    
    story.append(Spacer(1, 18))
