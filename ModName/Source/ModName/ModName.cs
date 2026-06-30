// ModName.cs — Mod entry point
// M0 — Hello World Mech
//
// In M0 il codice C# è minimale: serve solo a:
// 1. Definire la Mod class per inizializzazione (Harmony patcher)
// 2. Definire la MechExosuitExt ModExtension referenziata dal ThingDef XML
//
// In M1+ aggiungeremo: CompSubcorePilot, CompMechExosuitBattery, Building_HybridGestator, ecc.

using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using HarmonyLib;
using RimWorld;
using Verse;

namespace ModName
{
    /// <summary>
    /// Mod entry point. Inizializza Harmony patches (nessuna in M0, ma la struttura è pronta).
    /// </summary>
    [StaticConstructorOnStartup]
    public static class ModNameMod
    {
        static ModNameMod()
        {
            // In M0 non ci sono Harmony patches da applicare.
            // In M1+ qui inseriremo:
            //   var harmony = new Harmony("endercrepper.mechexosuit.framework");
            //   harmony.PatchAll();
            Log.Message("[ModName] M0 — Hello World Mech initialized.");
        }
    }

    /// <summary>
    /// ModExtension per identificare i mech-exosuit.
    /// In M0 contiene solo dati passivi (sourceApparelDef, supportedJobs).
    /// In M1+ verrà estesa con bandwidthCost, baseSkillBonus, ecc.
    /// </summary>
    public class MechExosuitExt : DefModExtension
    {
        /// <summary>
        /// DefName dell'apparel originale (es. Aqued_Exosuit_Apparel_Core per la Patriot).
        /// Usato per risalire alle stat della suit originale quando necessario.
        /// </summary>
        public string sourceApparelDef;

        /// <summary>
        /// Lista di WorkTypes che il mech-exosuit può eseguire.
        /// In M0 non viene usata attivamente (la AI vanilla ignora questa lista),
        /// ma in M1+ verrà controllata dal CompSubcorePilot.
        /// </summary>
        public List<WorkTypeDef> supportedJobs;

        // In M1+ aggiungeremo:
        // public int bandwidthCost = 3;
        // public int baseSkillBonus = 0;
        // public float maxEnergyTicks = 36000f;
        // public Dictionary<SkillDef, int> baseSkills;
    }
}
