"""Section 4: Sistema di Danno & Morte"""

from reportlab.platypus import Spacer


def build_section_04(story, ctx):
    h = ctx['heading']; so = ctx['section_opener']
    body = ctx['body']; bl = ctx['bullet_list']; cb = ctx['callout_box']
    dt = ctx['data_table']; cap = ctx['caption']; img = ctx['fit_image']
    P = ctx['Paragraph']; HR = ctx['HRFlowable']; KT = ctx['KeepTogether']
    code_block = ctx['code_block']
    
    story.extend(so('Capitolo 04 · Danno & Morte', 'Sistema di Danno & Morte',
                    chapter_num=4))
    
    story.append(body(
        "Il sistema di danno di [Mod Name] è un <b>estensione del modello "
        "di Exosuit Framework</b>: il mech-exosuit ha un health pool "
        "principale (come qualsiasi pawn) e il subcore è trattato come "
        "body part interna con health pool separato. Quando un colpo "
        "penetra l'armatura e colpisce la body part 'Subcore', il danno "
        "viene applicato all'HP del subcore invece che all'HP del mech. "
        "Questo crea il flavor tematico 'il colpo ha trapassato la corazza "
        "e colpito il cervello del mech'."
    , ctx['styles']['BodyLead']))
    
    # ── 4.1 Damage flow ──
    story.append(P('<b>4.1 — Flusso del danno (penetrazione al subcore)</b>',
                   ctx['styles']['H2']))
    story.append(body(
        "Il diagramma sottostante illustra il flusso completo di un colpo "
        "ricevuto dal mech-exosuit, dalla generazione del DamageInfo fino "
        "all'esito finale (subcore illeso, subcore danneggiato, o subcore "
        "distrutto). Il sistema è <b>deterministico</b> in tutti i punti "
        "tranne che nel roll di coverage (10% di probabilità che un colpo "
        "penetrante colpisca il subcore)."
    ))
    
    story.append(Spacer(1, 8))
    story.append(img(f"{ctx['diagrams_dir']}/damage_flow.png",
                     max_width=ctx['available_w'], max_height=400))
    story.append(cap('Figura 4.1 — Flusso del danno: colpo → armor check → body part roll → '
                      'subcore hit (10%) → esito. Il subcore ha HP separato dal mech.'))
    
    # ── 4.2 Armor & body part mechanics ──
    story.append(P('<b>4.2 — Meccanica armor e body part selection</b>',
                   ctx['styles']['H2']))
    
    story.append(body(
        "L'armor check è <b>completamente vanilla</b>: il mech-exosuit ha "
        "stat <code>ArmorRating_Sharp</code>, <code>ArmorRating_Blunt</code> "
        "e <code>ArmorRating_Heat</code> definite nel ThingDef (Sezione 3.2), "
        "e RimWorld gestisce il roll di penetrazione in modo standard. "
        "Se l'armatura blocca completamente il colpo, il danno è ridotto "
        "del 50% (mechanica Sharp armor) o del 100% (Blunt). Se l'armatura "
        "non blocca, il colpo penetra e procede al roll di body part."
    ))
    
    story.append(body(
        "La <b>body part selection</b> usa il BodyDef custom di Sezione 3.3. "
        "RimWorld sceglie la body part colpita in base alla <code>coverage</code> "
        "di ciascuna parte: Torso (35%), Head (10%), braccia (20% totali), "
        "gambe (30%), <b>Subcore (10%)</b>. Nota: coverage non è normalizzata "
        "a 100% — RimWorld fa un roll ponderato. Il subcore ha coverage 0.10 "
        "che si traduce in circa il 10% dei colpi penetranti che lo colpiscono."
    ))
    
    story.append(P('<b>4.2.1 — Quando il subcore viene colpito</b>',
                   ctx['styles']['H3']))
    story.append(body(
        "Quando RimWorld determina che un colpo ha colpito la body part "
        "'Subcore', viene chiamato <code>Pawn.TakeDamage</code> con un "
        "<code>DamageInfo</code> che ha <code>HitPart = Subcore</code>. "
        "Una Harmony patch nostra (vedi snippet sotto) intercetta questo "
        "caso e reindirizza il danno al <code>CompSubcorePilot</code> "
        "invece di applicarlo all'HP del mech. Questo preserva il flavor "
        "'il colpo ha trapassato il frame ma non ha distrutto il mech — "
        "ha colpito il cervello'."
    ))
    
    story.append(code_block('''// HarmonyPatches/Patch_TakeDamage.cs
using HarmonyLib;

namespace ModName.HarmonyPatches
{
    [HarmonyPatch(typeof(Pawn), nameof(Pawn.TakeDamage))]
    public static class Patch_TakeDamage
    {
        public static bool Prefix(Pawn __instance, ref DamageInfo dinfo, ref DamageWorker.DamageResult __result)
        {
            // Solo per i nostri mech-exosuit
            if (__instance.def.defName.StartsWith("ModName_MechExosuitRace_"))
            {
                var subcoreComp = __instance.TryGetComp<CompSubcorePilot>();
                if (subcoreComp == null || !subcoreComp.HasSubcore) return true;

                // Se il colpo ha colpito la body part Subcore, ridirigi
                if (dinfo.HitPart?.defName == "ModName_Subcore")
                {
                    subcoreComp.Notify_SubcoreHit(dinfo);
                    // Non applicare il danno all'HP del mech
                    __result = new DamageWorker.DamageResult();
                    return false;  // skip vanilla damage application
                }
            }
            return true;  // procedi con vanilla damage
        }
    }
}'''))
    
    # ── 4.3 Subcore HP & destruction ──
    story.append(P('<b>4.3 — HP del subcore e distruzione</b>',
                   ctx['styles']['H2']))
    
    headers = ['Tier subcore', 'HP massimi', 'Coverage body part', 'Note']
    rows = [
        ['Standard (SubcoreRegular)', '100', '0.10',
         'Sblocca tier base. Richiede Standard Mechtech.'],
        ['High (SubcoreHigh)', '175', '0.10',
         'Tier avanzato. +75% HP, +4 skill bonus, 18h batteria.'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.30, 0.18, 0.18, 0.34]))
    story.append(cap('Tabella 4.1 — HP del subcore per tier. Coverage identica perché dipende dal BodyDef.'))
    
    story.append(body(
        "Quando l'HP del subcore arriva a 0 (in combattimento, per colpi "
        "penetranti), si attiva <code>OnSubcoreDestroyed()</code> (Sezione "
        "2.2.1). Effetti: (1) viene droppato un <code>Destroyed [Std/High] "
        "Subcore</code> come item separato accanto al mech; (2) il mech "
        "entra in stato 'braindead' — è downed, non può più operare, e "
        "non può essere riparato (perché il cervello è andato); "
        "(3) viene inviato un messaggio al giocatore con il nome del "
        "subcore (se SubcoreInfo è attivo) e la causa della distruzione."
    ))
    
    story.append(body(
        "Il mech in stato 'braindead' <b>non scompare</b>: rimane sul campo "
        "come 'shell vuota'. Il giocatore può: (a) abbandonarlo e lasciare "
        "che si deteriori naturalmente, (b) smontarlo al machining table "
        "per recuperarne i materiali del frame, (c) trascinarlo alla bay "
        "ibrida e — se ha un nuovo subcore — reinstallarlo per riattivarlo. "
        "L'opzione (c) è intenzionalmente costosa in lavoro (~4 ore di "
        "game) per bilanciare la possibilità di 'salvare' il frame."
    ))
    
    # ── 4.4 Death flow ──
    story.append(P('<b>4.4 — Flusso di morte del mech e drop del relitto</b>',
                   ctx['styles']['H2']))
    story.append(body(
        "Quando l'HP <b>del mech</b> (non del subcore) arriva a 0, il mech "
        "muore. A differenza dei pawn umani (che droppano un corpo), il "
        "mech-exosuit droppa un <b>Relitto Sigillato</b>. Il relitto "
        "contiene potenzialmente il subcore ancora funzionante — ma il "
        "giocatore non lo sa finché non lo apre."
    ))
    
    story.append(Spacer(1, 8))
    story.append(img(f"{ctx['diagrams_dir']}/death_flow.png",
                     max_width=ctx['available_w'], max_height=400))
    story.append(cap('Figura 4.2 — Flusso di morte del mech, drop del relitto, smontaggio, '
                      'esito finale. Il roll è deterministico in base agli HP residui del subcore.'))
    
    # ── 4.5 Survival formula ──
    story.append(P('<b>4.5 — Formula di sopravvivenza del subcore</b>',
                   ctx['styles']['H2']))
    
    story.append(body(
        "Il sistema di sopravvivenza del subcore nel relitto è "
        "<b>deterministico, non probabilistico</b>: non c'è un roll "
        "casuale. L'esito dipende esclusivamente dagli HP residui del "
        "subcore al momento della morte del mech. La formula:"
    ))
    
    story.append(cb(
        'Formula di recupero',
        '<b>HP_recuperati = HP_residui_morte × 0.70</b><br/>'
        '<b>Soglia di sopravvivenza = 30% del max HP</b><br/><br/>'
        'Interpretazione: se il subcore aveva almeno il 30% dei suoi HP '
        'massimi al momento della morte del mech, sopravvive con HP '
        'ridotti al 70% dei residui. Se aveva meno del 30%, viene '
        'distrutto nell\'esplosione del mech.',
        color=ctx['colors']['accent']
    ))
    
    story.append(body(
        "Esempio numerico per un subcore Standard (max 100 HP):"
    ))
    
    headers = ['HP residui al momento della morte', 'Esito', 'HP subcore dopo recupero']
    rows = [
        ['100 (intatto)', 'Sopravvive', '70 (= 100 × 0.70)'],
        ['80', 'Sopravvive', '56 (= 80 × 0.70)'],
        ['50', 'Sopravvive', '35 (= 50 × 0.70)'],
        ['31 (appena sopra soglia)', 'Sopravvive', '21 (= 31 × 0.70)'],
        ['30 (soglia)', 'Sopravvive', '21 (= 30 × 0.70)'],
        ['29 (appena sotto soglia)', 'Distrutto', '— (spawn Destroyed Subcore)'],
        ['0 (era già braindead)', 'Distrutto', '— (spawn Destroyed Subcore)'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.40, 0.20, 0.40]))
    story.append(cap('Tabella 4.2 — Esempi numerici di esito del recupero. '
                      'Soglia di sopravvivenza: 30 HP su 100 (Standard) o 52 HP su 175 (High).'))
    
    # ── 4.6 Cumulative degradation ──
    story.append(P('<b>4.6 — Degradazione cumulativa del subcore</b>',
                   ctx['styles']['H2']))
    
    story.append(body(
        "Un subcore recuperato ha HP ridotti — ed è <b>riutilizzabile</b>. "
        "Ma quando viene reinstallato in un nuovo mech-exosuit, i suoi HP "
        "<b>non vengono ripristinati</b>: inizia già danneggiato. Questo "
        "significa che al prossimo blow-through, ha meno HP assoluti prima "
        "di essere distrutto. Inoltre, la soglia di sopravvivenza (30% del "
        "max) resta calcolata sul max originale — quindi un subcore con "
        "HP max 100 ma HP correnti 50 ha ancora bisogno di 30 HP residui "
        "per sopravvivere a un eventuale morte del mech."
    ))
    
    story.append(body(
        "Questo crea una <b>progressione di degrado</b>: ogni ciclo morte-"
        "recupero-riuso riduce gli HP del subcore di ~30% in media. Dopo "
        "2-3 cicli, il subcore diventa troppo rischioso da usare in "
        "combattimento (soglia di sopravvivenza raggiunta rapidamente) e "
        "il giocatore è incentivato a smontarlo per i materiali. Questo "
        "è il <b>costo reale al fallimento</b> promesso dal Pilastro 1 "
        "della Sezione 1."
    ))
    
    # ── 4.7 Subcore HP repair ──
    story.append(P('<b>4.7 — Riparazione del subcore (opzionale)</b>',
                   ctx['styles']['H2']))
    
    story.append(body(
        "Un subcore danneggiato <b>può essere riparato</b> alla bay "
        "ibrida usando un'operazione dedicata (costo: 2000 ticks di "
        "lavoro + 1 ComponentIndustrial + 20 Steel). La riparazione "
        "ripristina il subcore al suo max HP. Tuttavia, ogni riparazione "
        "riduce il <code>MaxHP</code> del subcore di 5 punti (irreversibile): "
        "dopo 5 riparazioni un subcore Standard passa da max 100 a max 75, "
        "rendendolo progressivamente meno attrattivo."
    ))
    
    story.append(cb(
        'Bilanciamento: perché 5 HP per riparazione?',
        'Il numero 5 è calcolato per rendere il break-even point intorno alla '
        '5ª riparazione: a quel punto, il subcore ha max 75 HP, è più fragile '
        'di un nuovo Standard, e il costo cumulativo di riparazione (5 × '
        '20 Steel + 5 × 1 ComponentIndustrial) è paragonabile al costo di '
        'creare un nuovo subcore. Il giocatore razionale smonta il subcore '
        'danneggiato e ne crea uno nuovo, chiudendo il loop di bilanciamento.',
        color=ctx['colors']['accent2']
    ))
    
    # ── 4.8 Combat Extended integration ──
    story.append(P('<b>4.8 — Integrazione con Combat Extended</b>',
                   ctx['styles']['H2']))
    
    story.append(body(
        "Combat Extended (CE) rimpiazza il sistema di danno vanilla con "
        "uno più realistico basato su <b>penetrazione armatura calcolata "
        "per colpo</b> anziché un roll binario. Per [Mod Name], questo "
        "significa che il coverage del subcore (10%) va ricalcolato: in "
        "CE, il colpo 'sceglie' la body part <i>dopo</i> aver determinato "
        "se penetra l'armatura, ma la probabilità di colpire il subcore "
        "resta determinata dal BodyDef."
    ))
    
    story.append(body(
        "La compatibilità CE richiede una <b>Patch XML dedicata</b> in "
        "<code>1.6/CE/Patches/Patch_MechExosuitCE.xml</code> che aggiunga "
        "<code>ceBodyDef</code> e <code>BodyPartHealth</code> custom per "
        "il subcore. Vedere Sezione 7 per il dettaglio."
    ))
    
    story.append(Spacer(1, 18))
