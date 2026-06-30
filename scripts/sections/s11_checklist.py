"""Section 11: Checklist Implementazione"""

from reportlab.platypus import Spacer, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT


def build_section_11(story, ctx):
    h = ctx['heading']; so = ctx['section_opener']
    body = ctx['body']; bl = ctx['bullet_list']; cb = ctx['callout_box']
    dt = ctx['data_table']; cap = ctx['caption']
    P = ctx['Paragraph']; HR = ctx['HRFlowable']; KT = ctx['KeepTogether']
    
    story.extend(so('Capitolo 11 · Checklist', 'Checklist Implementazione',
                    chapter_num=11))
    
    story.append(body(
        "Questa sezione è pensata come <b>cookbook da tenere aperto</b> "
        "durante il coding. Per ogni milestone, fornisce: l'ordine "
        "operativo dei task, i riferimenti alle sezioni del documento, "
        "le signature API da implementare, e i pattern di testing."
    , ctx['styles']['BodyLead']))
    
    # ── 11.1 Setup iniziale ──
    story.append(P('<b>11.1 — Setup iniziale del progetto</b>',
                   ctx['styles']['H2']))
    story.append(body(
        "Prima di toccare qualsiasi codice C#, configurare l'ambiente:"
    ))
    
    story.append(bl([
        "<b>1.</b> Creare repo git: <code>git init ModName && cd ModName</code>",
        "<b>2.</b> Creare struttura directory (Sezione 3.7)",
        "<b>3.</b> Aggiungere come reference: <code>Assembly-CSharp.dll</code> (da RimWorld install), <code>UnityEngine.dll</code>, <code>0Harmony.dll</code>, <code>Exosuit.dll</code> (da Exosuit Framework), <code>0MultiplayerAPI.dll</code> (da Exosuit Framework)",
        "<b>4.</b> Creare file <code>About.xml</code> con packageId, name, supportedVersions=1.6, modDependencies per Exosuit Framework + Harmony",
        "<b>5.</b> Creare file <code>LoadFolders.xml</code> per supportare 1.6 (e opzionalmente 1.5)",
        "<b>6.</b> Creare soluzione Visual Studio / Rider: <code>ModName.csproj</code> con target framework .NET Framework 4.8",
        "<b>7.</b> Configurare build post-event: <code>copy /Y $(TargetDir)ModName.dll $(SolutionDir)..\\1.6\\Assemblies\\</code>",
        "<b>8.</b> Test: copiare la cartella mod in <code>%RIMWORLD_DIR%/Mods/</code>, lanciare gioco, verificare che la mod appaia nel mod manager",
    ]))
    
    # ── 11.2 API signatures ──
    story.append(P('<b>11.2 — API signatures pubbliche da implementare</b>',
                   ctx['styles']['H2']))
    story.append(body(
        "Riepilogo delle API pubbliche delle 5 classi C#. Ogni signature "
        "deve essere implementata e testata individualmente prima di "
        "passare alla successiva."
    ))
    
    headers = ['Classe', 'Metodo pubblico', 'Firma', 'Sezione rif.']
    rows = [
        ['CompSubcorePilot', 'InstallSubcore',
         'void InstallSubcore(Thing subcoreItem)', '2.2.1'],
        ['CompSubcorePilot', 'Notify_SubcoreHit',
         'void Notify_SubcoreHit(DamageInfo dinfo)', '2.2.1'],
        ['CompSubcorePilot', 'OnMechDeath',
         'void OnMechDeath()', '2.2.1'],
        ['CompSubcorePilot', 'ExtractSubcore',
         'void ExtractSubcore(Building_HybridGestator bay)', '2.2.1'],
        ['CompMechExosuitBattery', 'Recharge',
         'void Recharge(float amount)', '2.2.2'],
        ['CompMechExosuitBattery', 'Notify_LowPower',
         'void Notify_LowPower()', '2.2.2'],
        ['Building_HybridGestator', 'TryStartGestation',
         'void TryStartGestation(RecipeDef recipe, Thing subcore)', '2.2.3'],
        ['Building_HybridGestator', 'CompleteGestation',
         'private void CompleteGestation()', '2.2.3'],
        ['Building_HybridGestator', 'GetFloatMenuOptions',
         'IEnumerable<FloatMenuOption> GetFloatMenuOptions(Pawn)', '2.2.3'],
        ['ITab_HybridBay', 'FillTab',
         'protected override void FillTab()', '2.2.4'],
        ['JobDriver_DismantleRelic', 'MakeNewToils',
         'protected override IEnumerable<Toil> MakeNewToils()', '2.2.5'],
        ['SubcoreInfoBridge', 'CopySubcoreInfo (static)',
         'static void CopySubcoreInfo(Thing src, Thing dst)', '2.3'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.22, 0.22, 0.40, 0.16]))
    story.append(cap('Tabella 11.1 — API pubbliche da implementare. '
                      'L\'ordine di implementazione segue le milestone M0-M7.'))
    
    # ── 11.3 Testing patterns ──
    story.append(P('<b>11.3 — Pattern di testing</b>', ctx['styles']['H2']))
    story.append(body(
        "Testing in RimWorld avviene principalmente <b>in gioco</b> via "
        "dev mode. Non esiste un framework di unit testing ufficiale, ma "
        "esistono pattern ripetibili per testare ciascuna feature."
    ))
    
    story.append(P('<b>11.3.1 — Test: danno al subcore</b>',
                   ctx['styles']['H3']))
    story.append(bl([
        "Spawnare un mech-exosuit via dev mode (Action -> Spawn pawn -> ModName_MechExosuit_Patriot)",
        "Installare un subcore via dev mode (Action -> Set installed subcore)",
        "Aprire la scheda info del mech, verificare che il subcore sia visibile con HP corretti",
        "Spawnare un pawn hostile (es. raider) e forzarlo ad attaccare il mech",
        "Dopo 10-20 colpi penetranti, verificare che l'HP del subcore si sia ridotto",
        "Continuare fino a HP subcore = 0, verificare spawn Destroyed Subcore e mech in braindead state",
    ]))
    
    story.append(P('<b>11.3.2 — Test: morte del mech e drop relitto</b>',
                   ctx['styles']['H3']))
    story.append(bl([
        "Spawnare mech-exosuit con subcore a HP vari (100, 50, 30, 20, 0)",
        "Uccidere il mech via dev mode (Action -> Damage -> instakill)",
        "Verificare spawn Relitto Sigillato",
        "Forzare un pawn a smontare il relitto (right-click -> Dismantle)",
        "Verificare esito in base alla tabella 4.2 (formula 30% soglia)",
    ]))
    
    story.append(P('<b>11.3.3 — Test: bay ibrida end-to-end</b>',
                   ctx['styles']['H3']))
    story.append(bl([
        "Costruire la bay ibrida (Architect -> Production -> Hybrid Gestator Bay)",
        "Verificare che la bay appaia e abbia l'ITab custom",
        "Aprire l'ITab, verificare tutte le 5 sezioni",
        "Aggiungere materiali + subcore in una storage vicina",
        "Cliccare 'Avvia gestazione' nell'ITab, selezionare Patriot",
        "Verificare che un pawn crafter inizi a lavorare alla bay",
        "Attendere 8 ore game (~5 minuti reali a 3x speed)",
        "Verificare spawn del mech-exosuit + assegnazione al mechanitor",
        "Verificare che il mech-exosuit abbia il subcore installato (scheda info)",
    ]))
    
    story.append(P('<b>11.3.4 — Test: SubcoreInfo integration</b>',
                   ctx['styles']['H3']))
    story.append(bl([
        "Installare SubcoreInfo mod",
        "Produrre un subcore via ripscanner (pawn scansionato: es. 'Colonist John')",
        "Verificare che il subcore mostri 'Origin: Colonist John' nella scheda info",
        "Usare il subcore per gestare un mech-exosuit",
        "Verificare che il mech-exosuit mostri 'Pilot: Colonist John' nella scheda info",
        "Uccidere il mech, aprire il relitto, verificare che il subcore recuperato mantenga 'Origin: Colonist John'",
    ]))
    
    story.append(P('<b>11.3.5 — Test: CE compat</b>', ctx['styles']['H3']))
    story.append(bl([
        "Installare Combat Extended mod",
        "Spawnare un mech-exosuit + un pawn hostile con arma ad alto AP (es. sniper rifle)",
        "Verificare che i colpi penetranti danneggino il subcore con danno residuo (non full damage)",
        "Verificare che i colpi a basso AP (es. pistol) non danneggino quasi mai il subcore",
    ]))
    
    # ── 11.4 Common pitfalls ──
    story.append(P('<b>11.4 — Pitfall comuni e soluzioni</b>',
                   ctx['styles']['H2']))
    
    headers = ['Pitfall', 'Sintomo', 'Soluzione']
    rows = [
        ['BodyDef custom non caricato',
         'Mech-exosuit spawna senza body part subcore',
         'Verificare che BodyDef sia in Defs/ e che defName nel ThingDef race match'],
        ['Harmony patch non applicata',
         'Danno al subcore non funziona',
         'Verificare [HarmonyPatch] attribute + classe pubblica + ModName.cs con Harmony.PatchAll()'],
        ['SubcoreInfo bridge fallisce silenziosamente',
         'Identità non propagata ma nessun errore in log',
         'Aggiungere Log.Message nel catch del bridge per debug'],
        ['ITab non appare',
         'Bay costruita ma senza ITab custom',
         'Verificare inspectorTabs nel ThingDef e che ITab_HybridBay sia pubblica'],
        ['Mech-exosuit non entra in control group',
         'Mech spawnato ma rimane unassigned',
         'Verificare CompProperties_OverseerSubject nel ThingDef e che mechanitor abbia bandwidth'],
        ['Charger vanilla cerca di caricare mech-exosuit',
         'Error spam in log quando mech-exosuit vicino a charger',
         'Verificare PatchOperationReplace su chargeableThings del MechCharger'],
        ['Relitto non droppa',
         'Mech muore ma niente item a terra',
         'Verificare Patch_MechDeath + che OnMechDeath sia chiamato (Log.Message di debug)'],
        ['Subcore HP non serializzato',
         'Save/load resetta HP subcore a max',
         'Verificare PostExposeData in CompSubcorePilot con Scribe_Values.Look'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.25, 0.30, 0.45]))
    story.append(cap('Tabella 11.2 — Pitfall comuni durante lo sviluppo e relative soluzioni.'))
    
    # ── 11.5 Build & deploy ──
    story.append(P('<b>11.5 — Build e deploy</b>', ctx['styles']['H2']))
    story.append(body(
        "Workflow di build e deploy iterativo durante lo sviluppo:"
    ))
    
    story.append(bl([
        "<b>1.</b> Compilare in Visual Studio/Rider (Release config)",
        "<b>2.</b> Copiare <code>ModName.dll</code> da <code>bin/Release/</code> a <code>1.6/Assemblies/</code>",
        "<b>3.</b> Copiare l'intera cartella mod in <code>%RIMWORLD_DIR%/Mods/ModName/</code>",
        "<b>4.</b> Lanciare RimWorld, attivare la mod nel mod manager",
        "<b>5.</b> Testare in gioco",
        "<b>6.</b> Per modifiche XML/Defs: chiudere il gioco, modificare i file, riaprire (non serve ricompilare C#)",
        "<b>7.</b> Per modifiche C#: chiudere il gioco, ricompilare, copiare la DLL, riaprire",
        "<b>8.</b> Per debug veloce: usare <code>Log.Message()</code> nel codice e <code>dev mode -> log window</code>",
    ]))
    
    story.append(Spacer(1, 18))
