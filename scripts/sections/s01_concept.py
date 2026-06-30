"""Section 1: Concept & Vision"""

from reportlab.platypus import Spacer, PageBreak


def build_section_01(story, ctx):
    h = ctx['heading']; so = ctx['section_opener']
    body = ctx['body']; bl = ctx['bullet_list']; cb = ctx['callout_box']
    dt = ctx['data_table']; cap = ctx['caption']
    P = ctx['Paragraph']; HR = ctx['HRFlowable']; KT = ctx['KeepTogether']
    Spacer_ = ctx['Spacer']
    
    # ── Section opener ──
    story.extend(so('Capitolo 01 · Concept', 'Concept & Vision', chapter_num=1))
    
    # ── Lead paragraph ──
    story.append(body(
        "<b>[Mod Name]</b> è una mod per RimWorld 1.6 che introduce exosuit "
        "meccanoid-guidate: entità ibride che combinano l'estetica e l'autonomia "
        "operativa dei mechanoidi vanilla con la modularità e la configurabilità "
        "dell'Exosuit Framework di Aoba. Il cuore del concept è semplice ma "
        "tematicamente potente: invece di un pawn umano a bordo dell'exosuit, "
        "il pilota è un <b>subcore vanilla</b> (Standard o High) installato "
        "fisicamente come body part interna, con health pool separato dal mech."
    , ctx['styles']['BodyLead']))
    
    story.append(body(
        "L'idea nasce dall'osservazione che le exosuit classiche — pur essendo "
        "visivamente e meccanicamente soddisfacenti — soffrono di due limiti: "
        "(1) richiedono un pawn umano dedicato che viene 'bloccato' all'interno, "
        "riducendo la flessibilità della colonia; (2) il flavor tematico è "
        "quello di un'veicolo con pilota' anziché di un'autonomia robotica. "
        "D'altra parte, i mechanoidi vanilla hanno autonomia ma sono monolitici: "
        "niente slot di equipaggiamento, niente loadout configurabile. [Mod Name] "
        "unisce i due mondi: il subcore diventa letteralmente il 'cervello' del "
        "mech-exosuit, con tutti i pro e i contro che questo comporta."
    ))
    
    story.append(body(
        "Il posizionamento della mod è quindi quello di un framework estensibile "
        "che può 'mech-ificare' qualsiasi exosuit esistente (compatibile con "
        "Exosuit Framework) aggiungendo un nuovo ThingComp e una nuova bay di "
        "gestione. La mod è pensata come <b>soft dependency</b>: funziona "
        "standalone ma si arricchisce quando SubcoreInfo è installato "
        "(preserva l'identità del pawn scansionato) e quando Combat Extended "
        "è presente (usa il suo sistema di penetrazione armatura)."
    ))
    
    story.append(Spacer_(1, 18))
    
    # ── Feature table ──
    story.append(P('<b>Tabella 1.1 — Feature chiave della mod</b>',
                   ctx['styles']['H3']))
    story.append(Spacer_(1, 6))
    
    headers = ['Aspetto', 'Decisione', 'Note implementative']
    rows = [
        ['Pilota interno', 'Subcore Standard/High vanilla',
         'BodyDef custom con subcore come body part, HP 100/175'],
        ['Danno al pilota', 'Health pool separato, penetrazione come exosuit vanilla',
         'Coverage 0.10 (10% dei colpi che penetrano l\'armatura colpiscono il subcore)'],
        ['Morte subcore', 'Deterministica',
         'HP subcore = 0 → Destroyed Subcore (smontabile al machining table)'],
        ['Morte mech', 'Drop Relitto Sigillato',
         'Apertura deterministica basata su HP residui del subcore'],
        ['Batteria', 'Scarsa (~mezza giornata)',
         'Solo bay ibrida ricarica; vanilla/Deadmanswitch charger disattivati'],
        ['Bandwidth', 'Come mech vanilla',
         'Entra in control group del mechanitor, va dormant se offline'],
        ['Sblocco tech', 'Standard Mechtech prerequisito',
         'No Basic subcore — solo Standard/High per coerenza lore'],
        ['Skill', 'Suit base + bonus subcore',
         'Standard: +0; High: +4 a tutte le skill della suit'],
        ['Estrazione', 'Comando floating menu',
         'Solo mech dockato in bay → restituisce subcore + frame item'],
        ['SubcoreInfo', 'Soft dependency',
         'CopySubcoreInfo() su installazione e su recupero da relitto'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.22, 0.30, 0.48]))
    story.append(cap('Tabella 1.1 — Riepilogo delle decisioni di design core della mod.'))
    
    # ── Design pillars ──
    story.append(Spacer_(1, 12))
    story.append(P('<b>1.1 — Pilastri di design</b>', ctx['styles']['H2']))
    
    story.append(body(
        "Tre pilastri guidano tutte le decisioni di design e bilanciamento "
        "della mod. Ogni feature proposta deve essere valutata rispetto a "
        "questi pilastri; se una feature li viola, va rivista o scartata."
    ))
    
    story.append(P('<b>Pilastro 1 — Costo reale al fallimento</b>', ctx['styles']['H3']))
    story.append(body(
        "In molte mod di mech/exosuit, la distruzione del mech comporta solo "
        "la perdita di materiali. Questo genera gameplay superficiale: si "
        "spamma mech senza cura perché il costo di una morte è solo 'craft "
        "un altro'. [Mod Name] rompe questo pattern rendendo il subcore un "
        "oggetto <b>persistente e fragile</b>: un subcore può sopravvivere a "
        "più morti del mech, ma ogni volta perde HP e diventa più probabile "
        "che venga distrutto al prossimo blow-through. Questo crea una "
        "progressione naturale di 'subcore storici' nella colonia — alcuni "
        "diventano reliquie da proteggere, altri finiscono per essere "
        "smontati quando troppo danneggiati per essere utili."
    ))
    
    story.append(P('<b>Pilastro 2 — Tensione operativa</b>', ctx['styles']['H3']))
    story.append(body(
        "La batteria scarsa non è un limite arbitrario: è una scelta di game "
        "design per creare tensione. Il giocatore non può lasciare un "
        "mech-exosuit sempre attivo a pattugliare — deve pianificare quando "
        "attivarlo, quando ricaricarlo, e questo crea finestre di vulnerabilità "
        "narrative. La bay ibrida diventa un asset strategico: posizionarla "
        "vicino al perimetro difensivo o al centro della base cambia le "
        "dinamiche di risposta agli raid. Inoltre, il fatto che consumi "
        "bandwidth anche da spento impedisce di avere una scorta di mech-exosuit "
        "pronti all'uso — ogni mech attivo ha un costo opportunità reale."
    ))
    
    story.append(P('<b>Pilastro 3 — Rispetto delle mod esistenti</b>', ctx['styles']['H3']))
    story.append(body(
        "[Mod Name] non riscrive Exosuit Framework né vanilla mechtech: ne "
        "estende il comportamento via ThingComp, ModExtension e Harmony patch "
        "non-invasive. Una suit 'mech-ificata' è, dal punto di vista di "
        "Exosuit Framework, una normale exosuit con un Comp aggiuntivo. Dal "
        "punto di vista di vanilla mechtech, è un mech normale in un control "
        "group del mechanitor. Questo garantisce massima compatibilità con "
        "future versioni delle mod dipendenti e minimizza il rischio di "
        "regressioni."
    ))
    
    # ── Positioning ──
    story.append(P('<b>1.2 — Posizionamento rispetto alle mod esistenti</b>',
                   ctx['styles']['H2']))
    
    story.append(body(
        "Per capire dove si posiziona [Mod Name], è utile mappare lo spazio "
        "delle mod di mech/exosuit esistenti per RimWorld 1.6:"
    ))
    
    headers = ['Mod', 'Pilota', 'Batteria', 'Configurabilità', 'Costo morte']
    rows = [
        ['Vanilla Mechanoids', 'Nessuno (autonomo)', 'Ricarica standard',
         'Bassa (preset)', 'Solo materiali'],
        ['Exosuit Framework', 'Pawn umano', 'Fuel cell opzionale',
         'Alta (slot system)', 'Pawn + materiali'],
        ['TheDeadmanswitch Mech Chargers', 'N/A (framework)',
         'Custom charger', 'N/A', 'N/A'],
        ['Androids / Misc Robots', 'AI core', 'Ricarica standard',
         'Media', 'AI core perso'],
        ['[Mod Name]', 'Subcore vanilla', 'Scarsa (bay ibrida)',
         'Alta (slot system)', 'Subcore persistente con degrado'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.25, 0.18, 0.18, 0.20, 0.19]))
    story.append(cap('Tabella 1.2 — Posizionamento competitivo. [Mod Name] occupa la '
                      'nicchia "mech autonomi con subcore persistente e loadout configurabile".'))
    
    # ── Target experience ──
    story.append(Spacer_(1, 12))
    story.append(P('<b>1.3 — Esperienza target</b>', ctx['styles']['H2']))
    
    story.append(body(
        "Il giocatore tipico a cui ci rivolgiamo è il <b>colonnello "
        "mech-friendly</b>: ha già sbloccato Standard Mechtech, ha un "
        "mechanitor attivo con qualche lifter/constructoid, e sta cercando "
        "un'evoluzione che unisca la potenza difensiva delle exosuit "
        "(armatura, slot di armi pesanti) con l'autonomia dei mech "
        "(non richiedere un pawn dedicato). [Mod Name] dovrebbe dargli:"
    ))
    
    story.append(bl([
        "<b>Una decisione tattica significativa</b> quando attivare il mech-exosuit (battery scarica = mech inutilizzabile per ore)",
        "<b>Un legame emotivo con i subcore</b> — specialmente se SubcoreInfo è installato e mostra il nome del pawn scansionato",
        "<b>Una perdita che fa male</b> quando un subcore storico viene distrutto (ma non così male da scoraggiare il retry)",
        "<b>Una progression lenta ma tangibile</b> — più subcore crafti, più mech-exosuit puoi fieldare, ma bandwidth limita il numero contemporaneo",
        "<b>Compatibilità con il loadout</b> delle sue exosuit preferite (Patriot, AMP, ecc.) — la mod non lo costringe a imparare nuove suit",
    ]))
    
    story.append(Spacer_(1, 8))
    story.append(cb(
        'Nota su sottosistema SubcoreInfo',
        'L\'integrazione con SubcoreInfo è opzionale ma fortemente raccomandata. '
        'Senza di essa, il subcore è "solo un oggetto". Con SubcoreInfo, '
        'diventa il ricordo persistente di un pawn — possibilmente un pawn '
        'morto per produrlo (ripguard). Questo aggiunge peso emotivo al '
        'sistema di degrado: ogni riparazione fallita non è solo una perdita '
        'meccanica, è la perdita dell\'ultimo legame con quel pawn. '
        'Implementare l\'integrazione costa ~20 righe di codice (vedi Sezione 7).',
        color=ctx['colors']['accent2'], bg=ctx['colors']['card_bg']
    ))
    
    story.append(Spacer_(1, 18))
