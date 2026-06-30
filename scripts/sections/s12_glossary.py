"""Section 12: Glossario"""

from reportlab.platypus import Spacer


def build_section_12(story, ctx):
    h = ctx['heading']; so = ctx['section_opener']
    body = ctx['body']; bl = ctx['bullet_list']; cb = ctx['callout_box']
    dt = ctx['data_table']; cap = ctx['caption']
    P = ctx['Paragraph']; HR = ctx['HRFlowable']; KT = ctx['KeepTogether']
    
    story.extend(so('Capitolo 12 · Glossario', 'Glossario', chapter_num=12))
    
    story.append(body(
        "Definizioni dei termini chiave usati nel documento e nella mod. "
        "I termini vanilla RimWorld sono marcati con <b>[vanilla]</b>, i "
        "termini di mod di terze parti con <b>[mod name]</b>, i termini "
        "introdotti da [Mod Name] con <b>[Mod Name]</b>."
    , ctx['styles']['BodyLead']))
    
    # ── Glossary table ──
    headers = ['Termine', 'Tipo', 'Definizione']
    rows = [
        ['Subcore', 'vanilla',
         'Oggetto (Thing) prodotto da softscanner o ripscanner. Esistono 3 tier vanilla: Basic, Standard, High. In [Mod Name] usiamo Standard e High, più un nuovo tier custom Persona AI (vedi voce dedicata).'],
        ['SubcoreRegular', 'vanilla',
         'ThingDef del subcore Standard. HP vanilla 50, usato come pilota per mech-exosuit con HP custom 100.'],
        ['SubcoreHigh', 'vanilla',
         'ThingDef del subcore High. HP vanilla 80, usato come pilota per mech-exosuit con HP custom 175. Bonus +4 a tutte le skill della suit.'],
        ['Persona Core', 'vanilla',
         'Item raro di RimWorld vanilla. Normalmente usato per pilotare ship AI. In [Mod Name] è un ingrediente per craftare il Persona AI Subcore.'],
        ['Persona AI Subcore (ModName_SubcorePersonaAI)', '[Mod Name]',
         'Nuovo ThingDef custom della mod. Tier 3 del sistema subcore: +8 skill (cap vanilla 20), 250 HP, +2 BW, +25% battery rispetto al Standard. Craftato a partire da un Persona Core vanilla.'],
        ['Bandwidth', 'vanilla',
         'Risorsa del mechanitor che limita il numero di mech assegnabili. Ogni mech ha un bandwidthCost (1-5). I mech-exosuit consumano bandwidth come mech vanilla.'],
        ['Mechanitor', 'vanilla',
         'Pawn con implantato un Mechlink. Può controllare mech via Overseer subject. Prerequisito per usare mech-exosuit.'],
        ['Control group', 'vanilla',
         'Gruppo di mech assegnati a un mechanitor. Il mechanitor può comandare il gruppo (work, follow, escort, draft). I mech-exosuit entrano nel control group.'],
        ['Dormant mode', 'vanilla',
         'Stato di un mech quando il suo mechanitor muore o perde bandwidth. Il mech è downed ma non morto; si riattiva quando viene assegnato a un nuovo mechanitor.'],
        ['ITab', 'vanilla',
         'Tab nell\'inspector panel di una Thing (sinistra). Customizzabile via inspectorTabs nel ThingDef. Noi usiamo ITab_HybridBay.'],
        ['ModExtension', 'vanilla',
         'Classe C# custom che può essere attachata a una Def via XML <modExtensions>. Permette di aggiungere campi custom alla Def senza subclassare. Noi usiamo MechExosuitExt e HybridGestatorExt.'],
        ['ThingComp', 'vanilla',
         'Componente runtime attachato a una Thing via XML <comps>. Permette di aggiungere behavior custom. Noi usiamo CompSubcorePilot, CompMechExosuitBattery, CompRelic.'],
        ['CompProperties', 'vanilla',
         'Classe C# che definisce i parametri configurabili di un ThingComp via XML. Esempio: CompProperties_SubcorePilot.'],
        ['Harmony patch', 'mod',
         'Libreria (brrainz.harmony) che permette di modificare metodi di classi vanilla senza subclassare. Usata per Patch_TakeDamage e Patch_MechDeath.'],
        ['BodyDef', 'vanilla',
         'Def che descrive la struttura anatomica di un pawn. Noi creiamo ModName_MechExosuitBody con subcore come body part interna.'],
        ['PawnKindDef', 'vanilla',
         'Def che descrive un tipo di pawn (es. lifter, centipede, raider). Noi creiamo ModName_MechExosuit_Patriot.'],
        ['Coverage', 'vanilla',
         'Probabilità relativa che un colpo penetrante colpisca una body part. Il subcore ha coverage 0.10 (10% dei colpi penetranti).'],
        ['Blow-through', 'vanilla',
         'Meccanica per cui un colpo che distrugge una body part può passare alla body part adiacente. Rilevante per il danno al subcore.'],
        ['Exosuit Framework', 'mod (aoba.exosuit.framework)',
         'Mod di Aoba che fornisce il sistema di slot per exosuit (Core, Head, Arms, Mounts). Hard dependency di [Mod Name].'],
        ['Exosuit.SlotDef', 'mod (Exosuit Framework)',
         'Def custom di Exosuit Framework che definisce gli slot di equipaggiamento di una exosuit. 7 slot: Core, Head, Attachment, ArmLeft, ArmRight, MountLeft, MountRight.'],
        ['Exosuit.Exosuit_Core', 'mod (Exosuit Framework)',
         'Classe C# base dell\'apparel-exosuit. Le nostre mech-exosuit sono pawn (non apparel), ma usano lo stesso pattern di danno.'],
        ['Building_MaintenanceBay', 'mod (Exosuit Framework)',
         'Classe C# della docking bay originale di Exosuit Framework. La nostra Building_HybridGestator la estende.'],
        ['IExosuitDestructionHandler', 'mod (Exosuit Framework)',
         'Interfaccia pubblica di Exosuit Framework per intercettare la distruzione di una exosuit. Noi la implementiamo per drop il relitto.'],
        ['SubcoreInfo', 'mod (eth0net.SubcoreInfo)',
         'Mod di eth0net che traccia quale pawn è stato scansionato per produrre un subcore. Soft dependency di [Mod Name].'],
        ['SubcoreInfoUtility.CopySubcoreInfo', 'mod (SubcoreInfo)',
         'Metodo pubblico statico di SubcoreInfo che copia l\'identità del pawn scansionato da un Thing a un altro. Usato dal nostro bridge.'],
        ['Combat Extended (CE)', 'mod (ceteam.combatextended)',
         'Mod di CEteam che rimpiazza il sistema di danno vanilla con uno più realistico basato su AP (armor penetration). Soft dependency di [Mod Name].'],
        ['Vanilla Expanded Framework (VEF)', 'mod (oskarpotocki.vfe.core)',
         'Framework di Oskar Potocki usato da molte mod VE. Dipendenza di Exosuit Framework, soft per [Mod Name].'],
        ['Mech-exosuit', '[Mod Name]',
         'Pawn custom generato dalla bay ibrida. È un mech vanilla a tutti gli effetti (consume bandwidth, va dormant) ma con subcore installato come body part interna.'],
        ['Bay ibrida', '[Mod Name]',
         'Building_HybridGestator. Edificio 3×3 che combina 4 funzioni: loadout editor, gestation, charging, subcore install/extract.'],
        ['Relitto Sigillato', '[Mod Name]',
         'Item droppato quando un mech-exosuit muore. Contiene potenzialmente il subcore. Richiede smontaggio (JobDriver_DismantleRelic) per rivelare l\'esito.'],
        ['Destroyed Subcore', '[Mod Name]',
         'Item droppato quando il subcore viene distrutto (HP = 0 in combattimento, o roll fallito all\'apertura del relitto). Smontabile al machining table per acciaio e componenti.'],
        ['Subcore braindead', '[Mod Name]',
         'Stato del mech-exosuit quando il suo subcore viene distrutto in combattimento. Il mech è downed e non riparabile, ma può essere smontato per i materiali o riportato alla bay per reinstallare un nuovo subcore.'],
        ['Low power mode', '[Mod Name]',
         'Stato del mech-exosuit quando la batteria arriva a 0. Il mech è downed ma non morto. Si ripristina ricaricandolo nella bay ibrida.'],
        ['Shell vuota', '[Mod Name]',
         'Mech-exosuit senza subcore installato. Può essere creato gestando senza subcore (raro), o essere il risultato di estrazione volontaria o subcore braindead. Non operativo finché non si installa un nuovo subcore.'],
        ['Soft dependency', '[Mod Name] pattern',
         'Pattern in cui [Mod Name] funziona anche se la mod dipendente non è caricata, ma perde alcune feature. Implementato via ModDetector + reflection bridge.'],
        ['Hard dependency', '[Mod Name] pattern',
         'Pattern in cui [Mod Name] non può funzionare senza la mod dipendente. Implementato via modDependencies in About.xml. Exosuit Framework è hard dependency.'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.20, 0.20, 0.60]))
    story.append(cap('Tabella 12.1 — Glossario dei termini usati nel documento e nella mod.'))
    
    # ── Final note ──
    story.append(Spacer(1, 18))
    story.append(cb(
        'Prossimi passi',
        'Questo documento è la <b>baseline di design</b> per [Mod Name]. Il prossimo '
        'passo è implementare M0 (Hello World Mech) seguendo la checklist '
        'della Sezione 11. Una volta raggiunto M0, procedere con M1 '
        '(Subcore Install) e così via. Tornare a questo documento per '
        'rivedere le decisioni di design quando si implementano feature '
        'specifiche. Aggiornare il documento (nuova versione) quando '
        'cambiano le decisioni di bilanciamento o si aggiungono nuove suit.',
        color=ctx['colors']['accent']
    ))
    
    story.append(Spacer(1, 18))
