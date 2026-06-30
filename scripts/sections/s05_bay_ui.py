"""Section 5: Bay Ibrida & UI"""

from reportlab.platypus import Spacer


def build_section_05(story, ctx):
    h = ctx['heading']; so = ctx['section_opener']
    body = ctx['body']; bl = ctx['bullet_list']; cb = ctx['callout_box']
    dt = ctx['data_table']; cap = ctx['caption']; img = ctx['fit_image']
    P = ctx['Paragraph']; HR = ctx['HRFlowable']; KT = ctx['KeepTogether']
    code_block = ctx['code_block']
    
    story.extend(so('Capitolo 05 · Bay & UI', 'Bay Ibrida & UI',
                    chapter_num=5))
    
    story.append(body(
        "La <b>Building_HybridGestator</b> è il cuore operativo della mod. "
        "È un edificio 3×3 che combina quattro funzioni precedentemente "
        "separate in RimWorld: il loadout editor di Exosuit Framework, "
        "la gestazione di mech vanilla, la stazione di ricarica per mech, "
        "e un'interfaccia per installazione/estrazione del subcore. Il "
        "risultato è un 'centro operativo mech-exosuit' che diventa il "
        "focal point della base del giocatore."
    , ctx['styles']['BodyLead']))
    
    # ── 5.1 Schema bay ──
    story.append(P('<b>5.1 — Schema delle 4 funzioni integrate</b>',
                   ctx['styles']['H2']))
    
    story.append(body(
        "Il diagramma sottostante illustra le quattro funzioni della bay "
        "ibrida, gli input che richiede (subcore + materiali + pawn crafter) "
        "e gli output che produce (mech-exosuit operativo, subcore recuperato "
        "su estrazione, frame item su estrazione)."
    ))
    
    story.append(Spacer(1, 8))
    story.append(img(f"{ctx['diagrams_dir']}/bay_schema.png",
                     max_width=ctx['available_w'], max_height=380))
    story.append(cap('Figura 5.1 — Schema della Building_HybridGestator. '
                      'Le 4 funzioni condividono lo stesso edificio 3×3 e lo stesso ITab.'))
    
    # ── 5.2 ITab custom ──
    story.append(P('<b>5.2 — ITab_HybridBay: struttura della UI</b>',
                   ctx['styles']['H2']))
    
    story.append(body(
        "L'ITab custom è il principale punto di interazione del giocatore "
        "con la bay. È diviso in <b>cinque sezioni verticali</b>, ciascuna "
        "dedicata a un aspetto operativo. La UI è ispirata a "
        "<code>Exosuit.ITab_Exosuit</code> ma è stata riscritta da zero "
        "(invece di subclassare) per evitare hard dependency sui membri "
        "internal della classe base."
    ))
    
    headers = ['Sezione UI', 'Funzione', 'Stati visualizzati']
    rows = [
        ['1. Header',
         'Nome bay + stato operativo',
         'Idle · Gestating · Charging · Subcore install pending'],
        ['2. Loadout selector',
         'Selezione frame + armi + moduli (replica ITab_Exosuit)',
         'Lista slot supportati (Core, Head, Arms, Mounts); per slot: lista moduli disponibili'],
        ['3. Subcore panel',
         'Mostra subcore installato + HP + identità (se SubcoreInfo)',
         'Nessun subcore · Subcore installato (Standard/High, HP/maxHP, nome pawn scansionato)'],
        ['4. Battery status',
         'Barra energia del mech dockato + tempo stimato alla carica',
         'Nessun mech dockato · Charging (X%) · Fully charged'],
        ['5. Gestation progress',
         'Barra progressione della gestazione in corso',
         'Nessuna gestazione · In corso (X%) · Completata'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.22, 0.40, 0.38]))
    story.append(cap('Tabella 5.1 — Le 5 sezioni dell\'ITab_HybridBay. '
                      'Scrollable se lo spazio non basta (440×540 pt di default).'))
    
    # ── 5.3 Loadout selector ──
    story.append(P('<b>5.3 — Loadout selector (replica ITab_Exosuit)</b>',
                   ctx['styles']['H2']))
    story.append(body(
        "La sezione 2 (Loadout selector) replica il comportamento di "
        "<code>Exosuit.ITab_Exosuit</code>: per ogni slot supportato dal "
        "frame (definito nel <code>SlotDef</code> di Exosuit Framework), "
        "mostra il modulo attualmente installato e permette di cambiarlo "
        "con uno dei moduli disponibili nell'inventario della colonia. "
        "La differenza chiave: mentre ITab_Exosuit opera su un apparel "
        "indossato da un pawn, ITab_HybridBay opera sul mech-exosuit "
        "dockato."
    ))
    
    story.append(body(
        "I moduli supportati sono gli stessi di Exosuit Framework: per la "
        "Patriot, ad esempio, lo slot <code>ArmRight</code> supporta "
        "minigun o autocannon, lo slot <code>MountLeft</code> supporta "
        "rocket launcher. Quando il giocatore seleziona un modulo, "
        "l'ITab chiama <code>Building_HybridGestator.TryInstallModule()</code> "
        "che spawna un job per il pawn crafter di installarlo fisicamente."
    ))
    
    # ── 5.4 Gestation workflow ──
    story.append(P('<b>5.4 — Workflow di gestazione</b>', ctx['styles']['H2']))
    
    story.append(body(
        "Il workflow di gestazione è il cuore della funzione F2:"
    ))
    
    story.append(bl([
        "<b>Step 1</b> — Il giocatore clicca 'Avvia gestazione' nell'ITab. Appare un dialog con la lista dei mech-exosuit craftabili (in base alle ricette caricate dalla bay)",
        "<b>Step 2</b> — Selezione del mech-exosuit (es. Patriot). La bay verifica: subcore disponibile (in storage), materiali sufficienti, pawn crafter con Crafting ≥ 8 disponibile",
        "<b>Step 3</b> — Selezione del subcore da usare (se più di uno disponibile). La bay mostra il subcore e, se SubcoreInfo è attivo, il nome del pawn scansionato",
        "<b>Step 4</b> — Avvio. La bay consuma istantaneamente i materiali e il subcore (che viene 'installato' in una forma temporanea), e avvia la gestazione",
        "<b>Step 5</b> — Pawn crafter lavora alla bay per ~8 ore game (60.000 ticks di lavoro). La barra di progressione è visibile nell'ITab",
        "<b>Step 6</b> — Completamento. Spawn del mech-exosuit (Pawn) accanto alla bay. SubcoreInfoBridge.CopySubcoreInfo() trasferisce l'identità dal subcore al mech",
        "<b>Step 7</b> — Assegnazione al control group del mechanitor (se presente). Se nessun mechanitor con bandwidth disponibile, il mech rimane in stato 'unassigned' (downed, in attesa)",
    ]))
    
    # ── 5.5 Charging ──
    story.append(P('<b>5.5 — Stazione di ricarica (F3)</b>', ctx['styles']['H2']))
    story.append(body(
        "Quando un mech-exosuit è dockato alla bay (cioè in piedi sulla "
        "cella di interazione della bay), la bay lo ricarica "
        "automaticamente. La ricarica richiede 350 W di potenza elettrica "
        "(consumo della bay in fase di charging) e procede a ~5 W/tick, "
        "il che significa che un mech-exosuit completamente scarico "
        "(0% energia) richiede ~3 ore di gioco per ricaricarsi al 100%."
    ))
    
    story.append(body(
        "<b>Importante:</b> i charger vanilla (MechCharger) e i charger "
        "di TheDeadmanswitch Mech Chargers <b>non funzionano</b> sui "
        "mech-exosuit. Questo è implementato via <code>PatchOperationReplace</code> "
        "che filtra i mech-exosuit fuori dal <code>canCharge</code> check "
        "di quegli edifici. Il flavor: i mech-exosuit hanno un sistema di "
        "ricarica proprietario compatibile solo con la bay ibrida."
    ))
    
    story.append(code_block('''<!-- Patches/Patch_VanillaMechChargers.xml -->
<Patch>

  <!-- Rimuovi i mech-exosuit dalla lista dei mech caricabili dai charger vanilla -->
  <Operation Class="PatchOperationReplace">
    <xpath>/Defs/ThingDef[defName="MechCharger"]/comps/li[@Class="CompProperties_MechCharger"]/chargeableThings</xpath>
    <value>
      <chargeableThings>
        <li>Mech_Lifter</li>
        <li>Mech_Constructoid</li>
        <!-- ... tutti i mech vanilla, esclusi i nostri ModName_MechExosuitRace_* -->
      </chargeableThings>
    </value>
  </Operation>

  <!-- Stesso pattern per TheDeadmanswitch (se caricato) -->
  <Operation Class="PatchOperationFindMod">
    <mods>
      <li>thedeadmanswitch.MechChargers</li>
    </mods>
    <match Class="PatchOperationSequence">
      <operations>
        <li Class="PatchOperationReplace">
          <xpath>/Defs/ThingDef[starts-with(@ParentName,"TDS_MechChargerBase")]/comps/li[@Class="CompProperties_MechCharger"]/chargeableThings</xpath>
          <value>
            <chargeableThings>
              <!-- solo mech vanilla, no ModName -->
            </chargeableThings>
          </value>
        </li>
      </operations>
    </match>
  </Operation>

</Patch>'''))
    
    # ── 5.6 Subcore install/extract ──
    story.append(P('<b>5.6 — Installazione/estrazione subcore (F4)</b>',
                   ctx['styles']['H2']))
    story.append(body(
        "I comandi floating per installazione/estrazione del subcore "
        "appaiono nel menu contestuale della bay (clic destro sulla bay "
        "con un pawn selezionato). Due operazioni:"
    ))
    
    story.append(P('<b>Installa subcore</b>', ctx['styles']['H3']))
    story.append(body(
        "Precondizioni: (1) la bay ha un mech-exosuit 'shell vuota' "
        "(mech-exosuit senza subcore, creato gestando senza subcore — "
        "caso raro, o mech-exosuit braindead riportato alla bay); "
        "(2) il pawn selezionato ha un subcore (Standard o High) "
        "nell'inventario; (3) il pawn è adiacente alla bay. Effetto: "
        "il subcore viene 'installato' nel mech, che diventa operativo "
        "(se la batteria è carica)."
    ))
    
    story.append(P('<b>Estrai subcore</b>', ctx['styles']['H3']))
    story.append(body(
        "Precondizioni: (1) la bay ha un mech-exosuit dockato con subcore "
        "installato; (2) il pawn è adadjente alla bay. Effetto: il "
        "subcore viene 'estratto' e droppato come item accanto alla bay. "
        "Il mech-exosuit torna 'shell vuota' (non operativo, può essere "
        "riusato installando un nuovo subcore). HP del subcore al momento "
        "dell'estrazione vengono preservati sull'item (così come l'identità "
        "SubcoreInfo)."
    ))
    
    story.append(cb(
        'Perché permettere estrazione?',
        'L\'estrazione volontaria serve a due scopi: (1) recuperare un subcore '
        'prezioso (ad esempio High) da un mech-exosuit che il giocatore non '
        'vuole più usare — per installarlo in un altro; (2) sostituire un '
        'subcore danneggiato con uno nuovo prima che venga distrutto in '
        'combattimento. Questo secondo caso è importante per il bilanciamento: '
        'permette al giocatore di "ritirare" un subcore storico prima che sia '
        'troppo tardi, ma il subcore resta danneggiato — non viene ripristinato '
        'dall\'estrazione.',
        color=ctx['colors']['accent']
    ))
    
    # ── 5.7 Building cost & power ──
    story.append(P('<b>5.7 — Costo di costruzione e potenza</b>',
                   ctx['styles']['H2']))
    
    headers = ['Voce', 'Valore', 'Note']
    rows = [
        ['Work to build', '8.000 ticks (~1h game)',
         'Equivalente a una fabrication bench'],
        ['Costo materiali', '250 Steel + 8 ComponentIndustrial + 2 ComponentSpacer + 1 SubcoreEncoderModule',
         'SubcoreEncoderModule è vanilla 1.6'],
        ['Max HP', '250', 'Standard per edificio di produzione'],
        ['Power consumption (idle)', '50 W', 'Solo elettronica di base'],
        ['Power consumption (charging)', '350 W', 'Quando mech dockato in ricarica'],
        ['Power consumption (gestating)', '200 W', 'Durante gestazione attiva'],
        ['Flammability', '0.5', 'Più infiammabile di vanilla (ha componenti)'],
        ['Research prereq', 'ModName_HybridMechtech',
         'Sotto Standard Mechtech vanilla, vedi Sezione 9'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.30, 0.30, 0.40]))
    story.append(cap('Tabella 5.2 — Costi e consumi della Building_HybridGestator.'))
    
    story.append(Spacer(1, 18))
