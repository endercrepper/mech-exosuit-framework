"""Section 2: Architettura Tecnica"""

from reportlab.platypus import Spacer


def build_section_02(story, ctx):
    h = ctx['heading']; so = ctx['section_opener']
    body = ctx['body']; bl = ctx['bullet_list']; cb = ctx['callout_box']
    dt = ctx['data_table']; cap = ctx['caption']; img = ctx['fit_image']
    P = ctx['Paragraph']; HR = ctx['HRFlowable']; KT = ctx['KeepTogether']
    code_block = ctx['code_block']
    
    story.extend(so('Capitolo 02 · Architettura', 'Architettura Tecnica',
                    chapter_num=2))
    
    # ── Overview ──
    story.append(body(
        "L'architettura di [Mod Name] si compone di <b>tre layer logici</b>: "
        "(1) un layer di comportamenti runtime, costituito dai ThingComp e "
        "dalle Building custom che gestiscono subcore, batteria e UI; "
        "(2) un layer di Defs XML statiche che descrivono i nuovi oggetti "
        "(mech-exosuit, relitto, subcore distrutto, bay ibrida); "
        "(3) un layer di integrazione con API esterne — Exosuit Framework, "
        "SubcoreInfo e vanilla mechtech — che vengono consumate in sola "
        "lettura via Harmony patch e reflection sicura."
    , ctx['styles']['BodyLead']))
    
    story.append(body(
        "Il diagramma sottostante illustra le classi C# principali e le loro "
        "relazioni. Le classi nuove (cinque in totale) sono evidenziate in "
        "rame con bordo sinistro rinforzato. Le classi di Exosuit Framework "
        "e SubcoreInfo sono mostrate in blu tratteggiato per indicare che "
        "sono dipendenze esterne consumate via interfaccia o reflection."
    ))
    
    # ── Architecture diagram ──
    story.append(Spacer(1, 12))
    story.append(P('<b>2.1 — Diagramma dell\'architettura</b>', ctx['styles']['H3']))
    story.append(img(f"{ctx['diagrams_dir']}/architecture_class_diagram.png",
                     max_width=ctx['available_w'], max_height=ctx['colors']['accent'] and 380))
    story.append(cap('Figura 2.1 — Diagramma delle classi C# e delle loro dipendenze. '
                      'Layer 1: ThingComp/Building runtime. Layer 2: Defs XML statiche. '
                      'Layer 3: API esterne.'))
    
    # ── Classi principali ──
    story.append(P('<b>2.2 — Classi C# principali</b>', ctx['styles']['H2']))
    
    story.append(body(
        "Di seguito gli scheletri delle cinque classi C# principali. Per "
        "ciascuna sono mostrate le firme pubbliche e l'implementazione di "
        "1-2 metodi chiave; il resto è marcato come <code>// TODO</code> e "
        "verrà completato in fase di coding. La convenzione di naming "
        "segue quella di RimWorld (PascalCase per metodi pubblici, "
        "camelCase per campi privati, underscore per campi serializzati)."
    ))
    
    # Class 1: CompSubcorePilot
    story.append(P('<b>2.2.1 — CompSubcorePilot</b>', ctx['styles']['H3']))
    story.append(body(
        "Il Comp centrale della mod. Si attacca a ogni mech-exosuit via XML "
        "(<code><comps><li Class=\"ModName.CompProperties_SubcorePilot\"/></comps></code>). "
        "Gestisce: installazione del subcore all'atto della gestazione, "
        "tracking dell'HP del subcore (separato dall'HP del mech), "
        "danneggiamento su blow-through, estrazione volontaria, e "
        "drop del relitto su morte."
    ))
    
    story.append(code_block('''// CompSubcorePilot.cs — scheletro
namespace ModName
{
    public class CompSubcorePilot : ThingComp
    {
        // Stato serializzato (salvato nel savegame)
        private Thing installedSubcore;       // ref al subcore installato (o null)
        private int subcoreHP;                 // HP corrente del subcore
        private int subcoreMaxHP;              // max HP in base al tier (100/175)

        public Thing InstalledSubcore => installedSubcore;
        public int SubcoreHP => subcoreHP;
        public int SubcoreMaxHP => subcoreMaxHP;
        public bool HasSubcore => installedSubcore != null;

        public override void PostExposeData()
        {
            Scribe_References.Look(ref installedSubcore, "installedSubcore");
            Scribe_Values.Look(ref subcoreHP, "subcoreHP", 0);
            Scribe_Values.Look(ref subcoreMaxHP, "subcoreMaxHP", 100);
        }

        // Chiamato quando il mech-exosuit viene generato dalla bay
        public void InstallSubcore(Thing subcoreItem)
        {
            // TODO: validazione (tier corretto, non già installato)
            installedSubcore = subcoreItem;
            subcoreMaxHP = (subcoreItem.def == ThingDefOf.SubcoreHigh) ? 175 : 100;
            subcoreHP = subcoreMaxHP;

            // Integrazione SubcoreInfo (soft dep, via reflection)
            SubcoreInfoBridge.CopySubcoreInfo(subcoreItem, parent);
        }

        // Chiamato da Harmony patch su Pawn.TakeDamage quando il colpo
        // penetra e colpisce la body part "Subcore"
        public void Notify_SubcoreHit(DamageInfo dinfo)
        {
            subcoreHP -= dinfo.Amount;
            if (subcoreHP <= 0)
            {
                OnSubcoreDestroyed();
            }
        }

        private void OnSubcoreDestroyed()
        {
            // TODO: spawn "Destroyed [Std/High] Subcore" come item separato
            // TODO: mettere il mech in stato "braindead" (downed, non riparabile)
            // TODO: notifica messaggio al giocatore
            installedSubcore = null;
            subcoreHP = 0;
        }

        // Chiamato quando il mech muore (HP mech = 0)
        public void OnMechDeath()
        {
            if (installedSubcore == null) return;
            // TODO: determinare se subcore sopravvive in base a subcoreHP
            // TODO: spawn Relitto Sigillato con subcore "intrappolato" dentro
            // (il relitto ha un CompRelic che conserva HP residui + identità)
        }

        // Comando floating menu: estrai subcore (richiede mech in bay)
        public void ExtractSubcore(Building_HybridGestator bay)
        {
            // TODO: validare che il mech sia dockato
            // TODO: spawn subcore item accanto alla bay
            // TODO: SubcoreInfoBridge.CopySubcoreInfo(parent, subcoreItem) per preservare identità
            // TODO: disattivare il mech (diventa "shell vuota" da ricaricare)
            installedSubcore = null;
            subcoreHP = 0;
        }
    }

    public class CompProperties_SubcorePilot : CompProperties
    {
        public CompProperties_SubcorePilot()
        {
            compClass = typeof(CompSubcorePilot);
        }
    }
}'''))
    
    # Class 2: CompMechExosuitBattery
    story.append(P('<b>2.2.2 — CompMechExosuitBattery</b>', ctx['styles']['H3']))
    story.append(body(
        "Gestisce l'energia del mech-exosuit. Diversamente dal FuelCell di "
        "Exosuit Framework (che è un boost opzionale), questo Comp è la "
        "<b>fonte primaria di operatività</b>: quando l'energia arriva a 0, "
        "il mech va in 'low power mode' (downed, non morto). La ricarica "
        "avviene solo nella bay ibrida — i charger vanilla e di "
        "TheDeadmanswitch sono disabilitati per questi mech via Patch."
    ))
    
    story.append(code_block('''// CompMechExosuitBattery.cs — scheletro
namespace ModName
{
    public class CompMechExosuitBattery : ThingComp
    {
        private float energy;             // 0..1 (normalizzato)
        private float maxEnergyTicks;     // ~12h gioco = 36000 ticks per Standard; 18h = 54000 per High

        public float EnergyPct => energy;
        public bool CanOperate => energy > 0.05f;
        public bool IsLowPower => energy < 0.10f;

        public override void CompTick()
        {
            if (!CanOperate) return;
            energy -= 1f / maxEnergyTicks;
            if (energy < 0) energy = 0;

            if (energy == 0 && !IsInLowPowerState)
            {
                Notify_LowPower();
            }
        }

        public void Notify_LowPower()
        {
            // TODO: downed state (non death) — come mech senza bandwidth
            // TODO: messaggio "Mech-Exosuit [X] è andato in low power mode"
            // TODO: gizmo "Ritorna alla bay" auto-attivato
        }

        public void Recharge(float amount)
        {
            energy = System.Math.Min(1f, energy + amount);
        }

        public override void PostExposeData()
        {
            Scribe_Values.Look(ref energy, "energy", 1f);
            Scribe_Values.Look(ref maxEnergyTicks, "maxEnergyTicks", 36000f);
        }

        public override string CompInspectStringExtra()
        {
            return $"Batteria: {energy*100:F0}%\\nStato: {(CanOperate ? "Operativo" : "Low power")}";
        }
    }

    public class CompProperties_MechExosuitBattery : CompProperties
    {
        public float maxEnergyTicks = 36000f;  // override da XML per tier diverso

        public CompProperties_MechExosuitBattery()
        {
            compClass = typeof(CompMechExosuitBattery);
        }
    }
}'''))
    
    # Class 3: Building_HybridGestator
    story.append(P('<b>2.2.3 — Building_HybridGestator</b>', ctx['styles']['H3']))
    story.append(body(
        "Estende <code>Exosuit.Building_MaintenanceBay</code> aggiungendo "
        "quattro funzioni: (1) loadout UI stile ITab_Exosuit, (2) gestazione "
        "del mech a partire da subcore + materiali, (3) stazione di ricarica "
        "per mech dockato, (4) comandi floating per installazione/estrazione "
        "subcore. Vedi Sezione 5 per il dettaglio della UI."
    ))
    
    story.append(code_block('''// Building_HybridGestator.cs — scheletro
namespace ModName
{
    public class Building_HybridGestator : Exosuit.Building_MaintenanceBay
    {
        private Thing pendingSubcore;        // subcore caricato per la prossima gestazione
        private float gestationProgress;     // 0..1
        private RecipeDef activeRecipe;
        private int chargingMechId = -1;     // ID del mech dockato per ricarica

        public bool IsGestating => activeRecipe != null;
        public float GestationPct => gestationProgress;

        public override void Tick()
        {
            base.Tick();  // eredita maintenance bay behavior

            // Tick gestazione
            if (IsGestating)
            {
                gestationProgress += 1f / activeRecipe.workAmount;
                if (gestationProgress >= 1f)
                {
                    CompleteGestation();
                }
            }

            // Tick charging per mech dockato
            if (chargingMechId != -1)
            {
                var mech = FindMechById(chargingMechId);
                if (mech?.TryGetComp<CompMechExosuitBattery>() is { } batt)
                {
                    batt.Recharge(0.001f);  // 5W/tick ≈ ricarica ~3h game per 0->100%
                }
                else
                {
                    chargingMechId = -1;
                }
            }
        }

        public void TryStartGestation(RecipeDef recipe, Thing subcore)
        {
            // TODO: validare materiali + skill + subcore tier
            // TODO: consumare materiali
            pendingSubcore = subcore;
            activeRecipe = recipe;
            gestationProgress = 0f;
        }

        private void CompleteGestation()
        {
            // TODO: spawn Pawn (MechExosuitRace) usando PawnGenerator
            // TODO: InstallSubcore(pendingSubcore) sul mech appena creato
            // TODO: assegnazione al control group del mechanitor
            // TODO: notifica "Mech-Exosuit [X] è operativo"
            activeRecipe = null;
            gestationProgress = 0f;
            pendingSubcore = null;
        }

        public override IEnumerable<FloatMenuOption> GetFloatMenuOptions(Pawn pawn)
        {
            foreach (var opt in base.GetFloatMenuOptions(pawn))
                yield return opt;

            // TODO: aggiungi "Installa subcore" se mech vuoto e pawn ha subcore in inventory
            // TODO: aggiungi "Estrai subcore" se mech dockato con subcore
            // TODO: aggiungi "Avvia gestazione" se mech vuoto + materiali disponibili
        }
    }
}'''))
    
    # Class 4: ITab_HybridBay
    story.append(P('<b>2.2.4 — ITab_HybridBay</b>', ctx['styles']['H3']))
    story.append(body(
        "Tab custom che replica la UI di ITab_Exosuit di Exosuit Framework "
        "per la selezione del loadout (frame + armi + moduli) e aggiunge "
        "pannelli per gestazione e stato batteria. Vedi Sezione 5 per "
        "dettaglio della UI."
    ))
    
    story.append(code_block('''// ITab_HybridBay.cs — scheletro
namespace ModName
{
    public class ITab_HybridBay : ITab
    {
        private Vector2 scrollPos = Vector2.zero;
        private Building_HybridGestator Bay => (Building_HybridGestator)SelThing;

        public ITab_HybridBay()
        {
            size = new Vector2(440f, 540f);
            labelKey = "TabHybridBay";
        }

        protected override void FillTab()
        {
            // TODO: disegna 4 sezioni:
            // 1. Header con nome bay + stato (idle/gestating/charging)
            // 2. Loadout selector (replica ITab_Exosuit)
            // 3. Subcore panel (mostra subcore installato, HP, identità)
            // 4. Battery status (barra energia del mech dockato)
            // 5. Gestation progress bar (se in corso)

            var rect = new Rect(0, 0, size.x, size.y).ContractedBy(10f);
            Widgets.BeginScrollView(rect, ref scrollPos, viewRect);

            // ... rendering ...

            Widgets.EndScrollView();
        }
    }
}'''))
    
    # Class 5: JobDriver_DismantleRelic
    story.append(P('<b>2.2.5 — JobDriver_DismantleRelic</b>', ctx['styles']['H3']))
    story.append(body(
        "Job driver per lo smontaggio del Relitto Sigillato. Il pawn va "
        "al relitto, lavora per ~200 ticks, e produce: subcore recuperato "
        "(se gli HP residui lo permettono) o Destroyed Subcore + materiali."
    ))
    
    story.append(code_block('''// JobDriver_DismantleRelic.cs — scheletro
namespace ModName
{
    public class JobDriver_DismantleRelic : JobDriver
    {
        private const int WorkTicks = 200;
        private CompRelic Relic => job.targetA.Thing.TryGetComp<CompRelic>();

        public override bool TryMakePreToilReservations(bool errorOnFailed)
        {
            return pawn.Reserve(job.targetA, job, 1, -1, null, errorOnFailed);
        }

        protected override IEnumerable<Toil> MakeNewToils()
        {
            this.FailOnDespawnedNullOrForbidden(TargetIndex.A);

            yield return Toils_Goto.GotoThing(TargetIndex.A, PathEndMode.Touch);
            yield return Toils_General.Wait(WorkTicks)
                .WithProgressBarToilDelay(TargetIndex.A)
                .FailOnDespawnedNullOrForbidden(TargetIndex.A);

            var openToil = new Toil();
            openToil.initAction = () =>
            {
                var relic = job.targetA.Thing;
                var comp = Relic;
                if (comp == null) return;

                // Determina esito in base a HP residui
                bool survives = comp.CalculateSurvival();
                if (survives)
                {
                    var subcore = ThingMaker.MakeThing(comp.SubcoreDef);
                    subcore.HitPoints = comp.CalculateRecoveredHP();
                    SubcoreInfoBridge.CopySubcoreInfo(relic, subcore);
                    GenPlace.TryPlaceThing(subcore, pawn.Position, Map, ThingPlaceMode.Near);
                }
                else
                {
                    var destroyed = ThingMaker.MakeThing(comp.DestroyedSubcoreDef);
                    GenPlace.TryPlaceThing(destroyed, pawn.Position, Map, ThingPlaceMode.Near);
                }

                // Materiali del relitto (sempre)
                foreach (var thingDef in comp.MaterialYield)
                {
                    var mat = ThingMaker.MakeThing(thingDef.def);
                    mat.stackCount = thingDef.count;
                    GenPlace.TryPlaceThing(mat, pawn.Position, Map, ThingPlaceMode.Near);
                }

                relic.Destroy();
            };
            yield return openToil;
        }
    }
}'''))
    
    # ── SubcoreInfoBridge ──
    story.append(Spacer(1, 12))
    story.append(P('<b>2.3 — SubcoreInfoBridge (helper per soft dependency)</b>',
                   ctx['styles']['H2']))
    
    story.append(body(
        "Per mantenere [Mod Name] standalone pur supportando SubcoreInfo, "
        "tutte le chiamate a SubcoreInfo passano per un <b>bridge statico</b> "
        "che rileva a runtime se la mod è caricata (via "
        "<code>LoadedModManager.RunningMods</code>) e in caso contrario "
        "esegue un no-op. Questo pattern è idiomatico in RimWorld e permette "
        "alla mod di funzionare anche se SubcoreInfo viene disinstallato "
        "a metà savegame."
    ))
    
    story.append(code_block('''// SubcoreInfoBridge.cs — soft dependency wrapper
namespace ModName
{
    public static class SubcoreInfoBridge
    {
        private static bool? _isLoaded;
        public static bool IsLoaded => _isLoaded ??= IsModLoaded("eth0net.SubcoreInfo");

        private static bool IsModLoaded(string packageId)
        {
            return LoadedModManager.RunningMods
                .Any(m => m.PackageIdPlayerFacing == packageId);
        }

        /// <summary>
        /// Copia l'identità del pawn scansionato da subcore-item a mech-pawn
        /// (o viceversa). No-op se SubcoreInfo non è caricato.
        /// </summary>
        public static void CopySubcoreInfo(Thing source, Thing dest)
        {
            if (!IsLoaded) return;
            try
            {
                // Reflection sicura: cerca il metodo pubblico CopySubcoreInfo in SubcoreInfo.dll
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
        }
    }
}'''))
    
    story.append(Spacer(1, 8))
    story.append(cb(
        'Pattern architetturale: soft dependency via reflection',
        'Il bridge via reflection è il pattern raccomandato per mod che vogliono '
        'integrarsi opzionalmente con altre mod senza richiederle come hard '
        'dependency. Alternative: (a) <code>[AttributeLoaded("...")]</code> di '
        'Harmony per caricare conditionalmente le patch; (b) multimod target '
        'con LoadFolders.xml. Per [Mod Name] il bridge statico è sufficiente '
        'perché l\'unica superficie di integrazione è un singolo metodo.',
        color=ctx['colors']['accent2']
    ))
    
    story.append(Spacer(1, 18))
