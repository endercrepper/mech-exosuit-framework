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
        "<code>1/maxEnergyTicks</code> per tick. La <code>maxEnergyTicks</code> "
        "dipende da <b>due fattori</b>: la suit (ogni suit ha un consumo "
        "diverso in base a MoveSpeed, armor e sistemi attivi) e il tier "
        "del subcore installato. <b>Tre tier di subcore</b> sono supportati, "
        "ciascuno con un impatto diverso sulla batteria:"
    ))
    
    headers = ['Tier subcore', 'Effetto sulla batteria', 'Razionale lore']
    rows = [
        ['Standard', 'Base (100%)',
         'Processore standard, consumo normale'],
        ['High', '−25% durata',
         'Processore più potente, più assorbimento energetico'],
        ['Persona AI', '+25% durata',
         'AI senziente ottimizza dinamicamente il consumo'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.20, 0.25, 0.55]))
    story.append(cap('Tabella 6.1 — Effetto del tier subcore sulla durata della batteria. '
                      'Il Persona AI è l\'unico tier che migliora la batteria rispetto al Standard.'))
    
    story.append(body(
        "In termini numerici, le suit hanno valori di <code>maxEnergyTicks</code> "
        "configurati via XML nel <code>MechExosuitExt</code> (vedi Sezione 8.4 "
        "per i valori concreti di ciascuna suit × tier). Il trade-off del "
        "Persona AI è che costa <b>+2 BW</b> (vs +1 del High) — il mechanitor "
        "deve gestire un'entità senziente, non un semplice processore."
    ))
    
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
        "Il costo in bandwidth dipende da <b>due fattori</b>: la suit "
        "(definisce il valore base via XML in <code>MechExosuitExt</code>) "
        "e il tier del subcore installato. <b>High aggiunge +1</b> al "
        "valore base; <b>Persona AI aggiunge +2</b>. Il Persona AI costa "
        "più bandwidth perché il mechanitor deve gestire un'entità "
        "senziente, non un semplice processore pre-programmato — "
        "richiede attenzione continua per evitare che l'AI sviluppi "
        "comportamenti imprevisti."
    ))
    
    headers = ['Tipo mech', 'BW (Std)', 'BW (High)', 'BW (Persona AI)', 'Note']
    rows = [
        ['Vanilla Lifter', '1', '—', '—', 'Mini-mech, solo hauling'],
        ['Vanilla Constructoid', '2', '—', '—', 'Mini-mech, solo construction'],
        ['Vanilla Pikeman', '3', '—', '—', 'Combat mech'],
        ['Vanilla Centipede', '5', '—', '—', 'Heavy combat mech'],
        ['ModName Patriot', '3', '4', '5', 'Configurabile via XML; vedi Sezione 8'],
        ['ModName AMP', '3', '4', '5', 'Equivalente a Pikeman'],
        ['ModName Mobile Dragon', '3', '4', '5', 'Scout veloce, compensa con armor bassa'],
        ['ModName Pirate Brawnson', '4', '5', '6', 'Tank puro melee; con AI supera Centipede'],
        ['ModName Powered Work Loader', '2', '3', '4', 'Utility, equivalente a Constructoid'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.28, 0.10, 0.12, 0.16, 0.34]))
    story.append(cap('Tabella 6.3 — Costo in bandwidth per suit × tier subcore. '
                      'High = +1 BW; Persona AI = +2 BW (entità senziente richiede più attenzione del mechanitor).'))
    
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
