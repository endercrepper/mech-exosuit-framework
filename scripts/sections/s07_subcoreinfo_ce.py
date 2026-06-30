"""Section 7: Integrazione SubcoreInfo & CE"""

from reportlab.platypus import Spacer


def build_section_07(story, ctx):
    h = ctx['heading']; so = ctx['section_opener']
    body = ctx['body']; bl = ctx['bullet_list']; cb = ctx['callout_box']
    dt = ctx['data_table']; cap = ctx['caption']
    P = ctx['Paragraph']; HR = ctx['HRFlowable']; KT = ctx['KeepTogether']
    code_block = ctx['code_block']
    
    story.extend(so('Capitolo 07 · Integrazioni',
                    'Integrazione SubcoreInfo & Combat Extended',
                    chapter_num=7))
    
    story.append(body(
        "[Mod Name] è progettata con due integrazioni opzionali ma "
        "fortemente raccomandate: <b>SubcoreInfo</b> di eth0net (preserva "
        "l'identità del pawn scansionato sul subcore e la mostra nella "
        "scheda info del mech) e <b>Combat Extended</b> di NoImageAvailable "
        "(sistema di danno più realistico con penetrazione armatura "
        "calcolata per colpo). Entrambe le integrazioni sono <b>soft "
        "dependency</b>: la mod funziona anche senza, ma perde alcune "
        "feature."
    , ctx['styles']['BodyLead']))
    
    # ── 7.1 SubcoreInfo integration ──
    story.append(P('<b>7.1 — Integrazione con SubcoreInfo</b>',
                   ctx['styles']['H2']))
    
    story.append(body(
        "SubcoreInfo è una mod che 'ricorda' quale pawn è stato "
        "scansionato per produrre un subcore. Funziona attachando un "
        "<code>CompInfoBase</code> agli scanner (softscanner, ripscanner) "
        "e al mech gestator vanilla, un <code>CompSubcoreInfo</code> ai "
        "subcore stessi (SubcoreRegular, SubcoreHigh), e un "
        "<code>CompMechInfo</code> a tutti i mech via BaseMechanoid. "
        "L'identità viene poi copiata automaticamente dal subcore al mech "
        "quando il mech viene generato."
    ))
    
    story.append(body(
        "Per [Mod Name], l'integrazione consiste in:"
    ))
    
    story.append(bl([
        "<b>1. Trasferimento identità su gestazione</b> — quando la bay ibrida genera un mech-exosuit, chiamiamo <code>SubcoreInfoUtility.CopySubcoreInfo(subcoreItem, mechPawn)</code> per propagare l'identità del pawn scansionato dal subcore al mech-exosuit risultante",
        "<b>2. Trasferimento identità su recupero da relitto</b> — quando un pawn apre un Relitto Sigillato e il subcore sopravvive, chiamiamo <code>CopySubcoreInfo(relicThing, recoveredSubcoreItem)</code> per preservare l'identità sul subcore recuperato",
        "<b>3. Trasferimento identità su estrazione volontaria</b> — quando il giocatore estrae un subcore da un mech-exosuit dockato, chiamiamo <code>CopySubcoreInfo(mechPawn, subcoreItem)</code>",
        "<b>4. Patch su BaseMechanoid</b> — applichiamo la stessa patch di SubcoreInfo (<code>CompMechInfo</code> sui mech-exosuit) ma condizionata alla presenza di SubcoreInfo; se la mod non è caricata, la patch non viene applicata",
    ]))
    
    story.append(P('<b>7.1.1 — Chiamate al bridge</b>', ctx['styles']['H3']))
    story.append(body(
        "Tutte le chiamate passano per <code>SubcoreInfoBridge.CopySubcoreInfo</code> "
        "(Sezione 2.3), che è un no-op se SubcoreInfo non è caricato. "
        "Il bridge usa reflection per invocare il metodo pubblico di "
        "SubcoreInfo:"
    ))
    
    story.append(code_block('''// SubcoreInfoBridge.cs (snippet, vedi 2.3 per completo)
public static void CopySubcoreInfo(Thing source, Thing dest)
{
    if (!IsLoaded) return;
    try
    {
        var asm = AppDomain.CurrentDomain.GetAssemblies()
            .FirstOrDefault(a => a.GetName().Name == "SubcoreInfo");
        var util = asm?.GetType("SubcoreInfo.SubcoreInfoUtility");
        var method = util?.GetMethod("CopySubcoreInfo",
            new[] { typeof(Thing), typeof(Thing) });
        method?.Invoke(null, new object[] { source, dest });
    }
    catch (System.Exception e)
    {
        Log.Warning($"[ModName] SubcoreInfo bridge failed: {e.Message}");
    }
}'''))
    
    story.append(P('<b>7.1.2 — Quando il bridge viene chiamato</b>',
                   ctx['styles']['H3']))
    
    headers = ['Evento', 'Source', 'Dest', 'Note']
    rows = [
        ['Gestazione mech-exosuit completata',
         'Subcore item (consumato)',
         'Mech-exosuit Pawn appena spawnato',
         'In Building_HybridGestator.CompleteGestation()'],
        ['Apertura Relitto Sigillato (subcore sopravvissuto)',
         'Relitto (Thing con CompRelic)',
         'Subcore item spawnato',
         'In JobDriver_DismantleRelic.openToil'],
        ['Estrazione subcore (comando floating)',
         'Mech-exosuit Pawn',
         'Subcore item spawnato',
         'In CompSubcorePilot.ExtractSubcore()'],
        ['Installazione subcore (comando floating)',
         'Subcore item (consumato)',
         'Mech-exosuit Pawn',
         'In CompSubcorePilot.InstallSubcore()'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.32, 0.22, 0.22, 0.24]))
    story.append(cap('Tabella 7.1 — Tutti i punti in cui il bridge SubcoreInfo viene chiamato. '
                      'In ogni caso, se SubcoreInfo non è caricato, la chiamata è no-op.'))
    
    # ── 7.2 Combat Extended ──
    story.append(P('<b>7.2 — Integrazione con Combat Extended</b>',
                   ctx['styles']['H2']))
    
    story.append(body(
        "Combat Extended (CE) rimpiazza il sistema di danno vanilla con "
        "uno più realistico: ogni proiettile ha un valore di <b>penetrazione "
        "armatura (AP)</b> specifico, e l'armatura del bersaglio riduce "
        "il danno in modo proporzionale invece di un roll binario "
        "(bloccato/non bloccato). Questo ha implicazioni per il nostro "
        "sistema di subcore:"
    ))
    
    story.append(bl([
        "<b>Il coverage del subcore resta 0.10</b> — la probabilità che un colpo penetrante colpisca il subcore non cambia con CE",
        "<b>La penetrazione al subcore è più realistica</b> — in CE, un colpo che penetra l'armatura del mech-exosuit ha già 'superato' la corazza; il subcore (che è dietro la corazza) viene colpito con il danno residuo",
        "<b>I proiettili ad alto AP sono più pericolosi per il subcore</b> — un proiettile antimateriale (AP 50+) che penetra ha quasi sempre abbastanza danno residuo da distruggere il subcore in un colpo",
        "<b>I proiettili a basso AP sono meno pericolosi</b> — un colpo di pistola (AP 5) che 'penetra' ha poco danno residuo e danneggia il subcore solo minimamente",
    ]))
    
    story.append(P('<b>7.2.1 — Patch CE dedicata</b>', ctx['styles']['H3']))
    story.append(body(
        "Per garantire compatibilità CE, [Mod Name] include una patch XML "
        "dedicata in <code>1.6/CE/Patches/Patch_MechExosuitCE.xml</code> "
        "(caricata condizionalmente via LoadFolders.xml quando CE è "
        "presente). La patch fa tre cose:"
    ))
    
    story.append(code_block('''<!-- 1.6/CE/Patches/Patch_MechExosuitCE.xml -->
<Patch>

  <!-- 1. Registra il BodyDef custom per CE -->
  <Operation Class="PatchOperationAdd">
    <xpath>/Defs/BodyDef[defName="ModName_MechExosuitBody"]</xpath>
    <value>
      <ceBodyDef>ModName_MechExosuitBody_CE</ceBodyDef>
    </value>
  </Operation>

  <!-- 2. Aggiungi stat CE al ThingDef del mech-exosuit -->
  <Operation Class="PatchOperationSequence">
    <operations>
      <li Class="PatchOperationAdd">
        <xpath>/Defs/ThingDef[starts-with(defName,"ModName_MechExosuitRace_")]/statBases</xpath>
        <value>
          <Bulk>120</Bulk>
          <MeleeDodgeChance>0.05</MeleeDodgeChance>
          <MeleeParryChance>0.15</MeleeParryChance>
          <SmokeSensitivity>0</SmokeSensitivity>
          <AimingAccuracy>0.95</AimingAccuracy>
          <ShootingAccuracyPawn>1.0</ShootingAccuracyPawn>
        </value>
      </li>
    </operations>
  </Operation>

  <!-- 3. Assegna ammo set alle armi del mech-exosuit (per le suit che le usano) -->
  <!-- Per la Patriot: minigun usa 7.62x51mm NATO, autocannon usa 25mm, rocket launcher usa apposito set -->

</Patch>'''))
    
    story.append(P('<b>7.2.2 — BodyDef CE custom</b>', ctx['styles']['H3']))
    story.append(body(
        "CE usa un proprio sistema di <code>BodyPartHealth</code> per "
        "tracciare la salute delle singole body part. Per il subcore, "
        "definiamo una <b>body part custom CE</b> che ha un "
        "<code>health</code> separato e un <code>coverage</code> "
        "indipendente. La differenza chiave: in CE, la coverage può "
        "variare in base alla direzione del colpo (front/back/side), "
        "mentre in vanilla è uniforme. Per il subcore (nel torso), "
        "definiamo coverage 0.10 da tutte le direzioni tranne il "
        "dorso (0.15 — il subcore è più esposto da dietro)."
    ))
    
    # ── 7.3 Other compat ──
    story.append(P('<b>7.3 — Altre compatibilità</b>', ctx['styles']['H2']))
    
    story.append(body(
        "Oltre a SubcoreInfo e CE, [Mod Name] è testata per compatibilità "
        "con:"
    ))
    
    headers = ['Mod', 'Tipo dipendenza', 'Integrazione']
    rows = [
        ['Exosuit Framework (aoba.exosuit.framework)',
         'Hard dependency',
         'Necessaria per ParentName="MaintanenceBayBase" e per le Defs Slot/Module'],
        ['Vanilla Expanded Framework (oskarpotocki.vfe.core)',
         'Soft (via Exosuit Framework)',
         'VEF è dipendenza di Exosuit Framework; usiamo ApparelExtension se presente'],
        ['SubcoreInfo (eth0net.SubcoreInfo)',
         'Soft dependency',
         'Bridge via reflection, vedi 7.1'],
        ['Combat Extended (ceteam.combatextended)',
         'Soft dependency',
         'Patch XML dedicata in 1.6/CE/, vedi 7.2'],
        ['TheDeadmanswitch Mech Chargers',
         'Compatibilità passiva',
         'I nostri mech-exosuit sono esclusi dal charging di questi charger, vedi 5.5'],
        ['Harmony (brrainz.harmony)',
         'Hard dependency',
         'Richiesta per le patch su Pawn.TakeDamage e altri'],
        ['Vanilla Mechtech (Ludeon.RimWorld)',
         'Hard dependency',
         'Usa ThingDef SubcoreRegular, SubcoreHigh, BaseMechanoid, etc.'],
        ['HugsLib',
         'Opzionale, non richiesta',
         'Nessuna integrazione; se caricata, non genera conflitti'],
        ['Rocketman (kentington.saveourship2)',
         'Opzionale, non richiesta',
         'Compatibile (usa lo stesso sistema di caching vanilla)'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.35, 0.20, 0.45]))
    story.append(cap('Tabella 7.2 — Matrice di compatibilità con le mod più comuni.'))
    
    # ── 7.4 Testing matrix ──
    story.append(P('<b>7.4 — Matrice di testing raccomandata</b>',
                   ctx['styles']['H2']))
    story.append(body(
        "Durante lo sviluppo, testare le seguenti combinazioni di mod "
        "per garantire che non ci siano regressioni:"
    ))
    
    story.append(bl([
        "<b>Solo [Mod Name] + Exosuit Framework + VEF + Harmony</b> — baseline minima, deve funzionare",
        "<b>+ SubcoreInfo</b> — verifica che l'identità venga propagata in tutti e 4 i punti (Tabella 7.1)",
        "<b>+ Combat Extended</b> — verifica che il danno al subcore funzioni con penetrazione AP",
        "<b>+ SubcoreInfo + Combat Extended</b> — combinazione completa",
        "<b>+ TheDeadmanswitch Mech Chargers</b> — verifica che i mech-exosuit non vengano caricati dai charger custom",
        "<b>+ Vanilla Expanded: Mechanoids</b> — verifica compatibilità con mech custom aggiuntivi",
        "<b>+ Androids</b> — verifica che non ci siano conflitti con il sistema di pawn android (entrambi aggiungono pawnkind custom)",
    ]))
    
    story.append(Spacer(1, 18))
