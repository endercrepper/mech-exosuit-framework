"""Generate 4 diagrams (PNG) for the Mech-Exosuit design document.
Each diagram is an HTML file rendered to PNG via Playwright at 2x device scale.

Diagrams:
  1. architecture_class_diagram.png — C# class diagram
  2. damage_flow.png — Damage penetration flow (hit → armor → body part → subcore)
  3. death_flow.png — Mech death → relic → recovery flow
  4. bay_schema.png — Hybrid bay schema (4 functions)
"""

import os
import sys
import subprocess
from pathlib import Path

DIAGRAMS_DIR = Path("/home/z/my-project/diagrams")
DIAGRAMS_DIR.mkdir(parents=True, exist_ok=True)

# Common CSS palette — RimWorld Visual / earthy copper
PALETTE_CSS = """
:root {
  --bg: #f5f5f4;
  --card: #ebeae8;
  --header-fill: #4e4732;
  --cover-block: #746c56;
  --border: #c5bfac;
  --icon: #a48e4b;
  --accent: #92761f;
  --accent-2: #3aa0c2;
  --text-primary: #151513;
  --text-muted: #7e7c74;
  --node-fill: #faf7f0;
  --node-fill-accent: #fdf3e0;
  --node-fill-danger: #fae8e6;
  --node-fill-ok: #e8f4ec;
  --node-fill-mech: #e8eef4;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--bg);
  font-family: 'Noto Sans SC', 'Inter', sans-serif;
  color: var(--text-primary);
  padding: 30px;
}
.canvas {
  position: relative;
  background: var(--bg);
  padding: 0;
}
"""

# ─── Diagram 1: Architecture / Class Diagram ───────────────────────────────
DIAGRAM_1_HTML = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<title>Architettura Classi</title>
<style>
""" + PALETTE_CSS + """
.canvas { width: 1400px; height: 1000px; padding: 30px; }
.title-bar { font-size: 24px; font-weight: 700; color: var(--header-fill); margin-bottom: 6px; border-bottom: 2px solid var(--accent); padding-bottom: 6px; }
.subtitle { font-size: 13px; color: var(--text-muted); margin-bottom: 30px; }

.layer-band {
  position: absolute;
  left: 30px;
  right: 30px;
  height: 38px;
  border-left: 4px solid var(--accent);
  padding-left: 12px;
  padding-top: 8px;
  font-size: 11px;
  font-weight: 700;
  color: var(--header-fill);
  text-transform: uppercase;
  letter-spacing: 2px;
  background: rgba(146, 118, 31, 0.04);
}

.layer-1 { top: 110px; }
.layer-2 { top: 360px; }
.layer-3 { top: 660px; }

.node {
  position: absolute;
  width: 240px;
  background: var(--node-fill);
  border: 1.5px solid var(--border);
  border-radius: 4px;
  padding: 12px;
  font-size: 11px;
  line-height: 1.4;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}
.node .cls-name { font-weight: 700; color: var(--header-fill); font-size: 12px; margin-bottom: 4px; border-bottom: 1px solid var(--border); padding-bottom: 4px; }
.node .methods { color: var(--text-muted); font-family: 'Liberation Mono', monospace; font-size: 10px; }
.node.our { background: var(--node-fill-accent); border-color: var(--accent); border-left-width: 4px; }
.node.our .cls-name { color: var(--accent); }
.node.ext { background: var(--node-fill-mech); border-color: var(--accent-2); border-style: dashed; }
.node.ext .cls-name { color: var(--accent-2); }

/* positions */
.n-comp-subcore { left: 60px; top: 170px; }
.n-comp-battery { left: 330px; top: 170px; }
.n-tab { left: 600px; top: 170px; }
.n-jobdriver { left: 870px; top: 170px; }
.n-building { left: 1140px; top: 170px; width: 220px; }

.n-pawnkind { left: 60px; top: 420px; width: 220px; }
.n-bodydef { left: 320px; top: 420px; width: 220px; }
.n-thingdef-mech { left: 580px; top: 420px; width: 220px; }
.n-thingdef-relic { left: 840px; top: 420px; width: 220px; }
.n-thingdef-destroyed { left: 1100px; top: 420px; width: 260px; }

.n-ef-core { left: 80px; top: 720px; width: 220px; }
.n-ef-maint { left: 340px; top: 720px; width: 220px; }
.n-ef-destroy { left: 600px; top: 720px; width: 220px; }
.n-si { left: 860px; top: 720px; width: 220px; }
.n-vanilla-mech { left: 1120px; top: 720px; width: 240px; }

/* arrows */
svg.connectors { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; }
.arrow-line { stroke: var(--cover-block); stroke-width: 1.2; fill: none; marker-end: url(#arr); }
.arrow-line.dashed { stroke-dasharray: 4 3; stroke: var(--accent-2); }
.legend {
  position: absolute;
  left: 30px;
  bottom: 30px;
  display: flex;
  gap: 20px;
  font-size: 10px;
  color: var(--text-muted);
}
.legend-item { display: flex; align-items: center; gap: 6px; }
.legend-swatch { width: 14px; height: 10px; border: 1px solid; border-radius: 2px; }
</style>
</head>
<body>
<div class="canvas">
  <div class="title-bar">Architettura C# — [Mod Name]</div>
  <div class="subtitle">Classi nostre (rame), Dipendenze Exosuit Framework (blu tratteggiato), Dipendenze vanilla/SubcoreInfo (grigio)</div>

  <div class="layer-band layer-1">Layer 1 — Comportamenti runtime (ThingComp / Building / ITab)</div>

  <div class="node our n-comp-subcore">
    <div class="cls-name">CompSubcorePilot : ThingComp</div>
    <div class="methods">
+ InstalledSubcore: Thing<br>
+ SubcoreHP: int<br>
+ PostSpawnSetup()<br>
+ CompTick():<br>
&nbsp;&nbsp;tick subcore damage<br>
+ Notify_Damaged(amount)<br>
+ ExtractSubcore(): Thing<br>
+ PostDestroy()
    </div>
  </div>

  <div class="node our n-comp-battery">
    <div class="cls-name">CompMechExosuitBattery : ThingComp</div>
    <div class="methods">
+ Energy: float<br>
+ MaxEnergy: float<br>
+ CompTick()<br>
+ Notify_LowPower()<br>
+ Recharge(amount)<br>
+ CanOperate: bool
    </div>
  </div>

  <div class="node our n-tab">
    <div class="cls-name">ITab_HybridBay : ITab</div>
    <div class="methods">
+ FillTab()<br>
+ DrawLoadoutSelector()<br>
+ DrawGestationProgress()<br>
+ DrawSubcorePanel()<br>
+ DrawBatteryStatus()
    </div>
  </div>

  <div class="node our n-jobdriver">
    <div class="cls-name">JobDriver_DismantleRelic : JobDriver</div>
    <div class="methods">
+ MakeNewToils()<br>
&nbsp;&nbsp;→ go to relic<br>
&nbsp;&nbsp;→ work 200 ticks<br>
&nbsp;&nbsp;→ spawn products<br>
&nbsp;&nbsp;→ consume relic
    </div>
  </div>

  <div class="node our n-building">
    <div class="cls-name">Building_HybridGestator : Building_MaintenanceBay</div>
    <div class="methods">
+ GestationRecipe: RecipeDef<br>
+ InstalledSubcore: Thing<br>
+ GestationProgress: float<br>
+ Tick():<br>
&nbsp;&nbsp;tick gestation<br>
&nbsp;&nbsp;tick charging<br>
+ GetFloatMenuOptions()<br>
+ TryStartGestation()<br>
+ TryExtractSubcore()
    </div>
  </div>

  <div class="layer-band layer-2">Layer 2 — Defs XML (static data)</div>

  <div class="node n-pawnkind">
    <div class="cls-name">PawnKindDef (mech-exosuit)</div>
    <div class="methods">
Parent: BaseMechanoid<br>
+ race: MechExosuitRace<br>
+ combatPower: 350<br>
+ lifeStages
    </div>
  </div>

  <div class="node n-bodydef">
    <div class="cls-name">BodyDef (MechExosuitBody)</div>
    <div class="methods">
+ corePart: Torso<br>
&nbsp;&nbsp;→ Subcore (internal)<br>
+ parts: Head, Arms, Legs<br>
Subcore: HP=100/175<br>
coverage=0.10 (low)
    </div>
  </div>

  <div class="node n-thingdef-mech">
    <div class="cls-name">ThingDef MechExosuitRace</div>
    <div class="methods">
Parent: BaseMechanoid<br>
+ comps:<br>
&nbsp;&nbsp;CompSubcorePilot<br>
&nbsp;&nbsp;CompMechExosuitBattery<br>
+ modExtensions:<br>
&nbsp;&nbsp;MechExosuitExt
    </div>
  </div>

  <div class="node n-thingdef-relic">
    <div class="cls-name">ThingDef SealedRelic</div>
    <div class="methods">
+ category: Item<br>
+ destroyOnDrop: false<br>
+ comps: CompForbiddable<br>
+ recipes: DismantleRelic
    </div>
  </div>

  <div class="node n-thingdef-destroyed">
    <div class="cls-name">ThingDef DestroyedSubcore</div>
    <div class="methods">
+ category: Item<br>
+ tradeability: None<br>
+ recipes: SmashAtMachiningTable<br>
products: Steel(15),<br>ComponentIndustrial(1)
    </div>
  </div>

  <div class="layer-band layer-3">Layer 3 — API esterne (sola lettura, soft/hard dep)</div>

  <div class="node ext n-ef-core">
    <div class="cls-name">Exosuit.Exosuit_Core</div>
    <div class="methods">
[Exosuit Framework]<br>
ThingClass base dell'apparel<br>
— usato come riferimento<br>
per i pattern di damage
    </div>
  </div>

  <div class="node ext n-ef-maint">
    <div class="cls-name">Exosuit.Building_MaintenanceBay</div>
    <div class="methods">
[Exosuit Framework]<br>
Classe base della nostra<br>Building_HybridGestator<br>
+ ITab_Exosuit (riferim.)
    </div>
  </div>

  <div class="node ext n-ef-destroy">
    <div class="cls-name">Exosuit.IExosuitDestructionHandler</div>
    <div class="methods">
[Exosuit Framework]<br>
Interfaccia hook<br>
OnExosuitDestroyed(...)<br>
— la implementiamo per<br>
droppare il relitto
    </div>
  </div>

  <div class="node ext n-si">
    <div class="cls-name">SubcoreInfo.SubcoreInfoUtility</div>
    <div class="methods">
[SubcoreInfo, soft dep]<br>
+ CopySubcoreInfo(src, dst)<br>
— chiamato in install<br>
e in relic-open
    </div>
  </div>

  <div class="node ext n-vanilla-mech">
    <div class="cls-name">Vanilla Mech / Mechanitor</div>
    <div class="methods">
[RimWorld core]<br>
CompOverseerSubject<br>
+ BandwidthCost<br>
+ ControlGroup<br>
Mechanitor → assegnazione
    </div>
  </div>

  <!-- SVG connectors -->
  <svg class="connectors" viewBox="0 0 1400 1000" preserveAspectRatio="none">
    <defs>
      <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
        <path d="M0,0 L10,5 L0,10 z" fill="var(--cover-block)"/>
      </marker>
      <marker id="arrDashed" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
        <path d="M0,0 L10,5 L0,10 z" fill="var(--accent-2)"/>
      </marker>
    </defs>
    <!-- Layer 1 internal links -->
    <path class="arrow-line" d="M 540,200 L 600,200" />
    <path class="arrow-line" d="M 840,200 L 870,200" />
    <path class="arrow-line" d="M 1110,200 L 1140,200" />
    <!-- Layer 1 -> Layer 2 -->
    <path class="arrow-line" d="M 180,270 L 180,420" />
    <path class="arrow-line" d="M 450,270 L 320,420" />
    <path class="arrow-line" d="M 720,270 L 580,420" />
    <path class="arrow-line" d="M 990,270 L 840,420" />
    <!-- Layer 2 internal -->
    <path class="arrow-line" d="M 280,460 L 320,460" />
    <path class="arrow-line" d="M 540,460 L 580,460" />
    <path class="arrow-line" d="M 800,460 L 840,460" />
    <path class="arrow-line" d="M 1060,460 L 1100,460" />
    <!-- Layer 2 -> Layer 3 (soft deps, dashed) -->
    <path class="arrow-line dashed" d="M 690,510 L 450,720" />
    <path class="arrow-line dashed" d="M 800,510 L 700,720" />
    <path class="arrow-line dashed" d="M 1100,490 L 220,720" />
    <path class="arrow-line dashed" d="M 580,510 L 1000,720" />
    <path class="arrow-line dashed" d="M 1180,510 L 1240,720" />
  </svg>

  <div class="legend">
    <div class="legend-item"><div class="legend-swatch" style="background: var(--node-fill-accent); border-color: var(--accent);"></div>Classi nostre (Nuove)</div>
    <div class="legend-item"><div class="legend-swatch" style="background: var(--node-fill); border-color: var(--border);"></div>Defs XML</div>
    <div class="legend-item"><div class="legend-swatch" style="background: var(--node-fill-mech); border-color: var(--accent-2); border-style: dashed;"></div>API esterne (dipendenze)</div>
    <div class="legend-item">→ dipendenza hard &nbsp;&nbsp; ╌╌→ dipendenza soft (opzionale)</div>
  </div>
</div>
</body>
</html>
"""

# ─── Diagram 2: Damage Flow ────────────────────────────────────────────────
DIAGRAM_2_HTML = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<title>Flusso di Danno</title>
<style>
""" + PALETTE_CSS + """
.canvas { width: 1400px; height: 850px; padding: 30px; }
.title-bar { font-size: 24px; font-weight: 700; color: var(--header-fill); margin-bottom: 6px; border-bottom: 2px solid var(--accent); padding-bottom: 6px; }
.subtitle { font-size: 13px; color: var(--text-muted); margin-bottom: 30px; }

.phase {
  position: absolute;
  font-size: 10px;
  font-weight: 700;
  color: var(--header-fill);
  text-transform: uppercase;
  letter-spacing: 2px;
  padding: 4px 10px;
  background: var(--card-bg);
  border-left: 3px solid var(--accent);
}

.node {
  position: absolute;
  width: 200px;
  background: var(--node-fill);
  border: 1.5px solid var(--border);
  border-radius: 4px;
  padding: 12px;
  font-size: 11px;
  line-height: 1.5;
  text-align: center;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}
.node .lbl { font-weight: 700; color: var(--header-fill); font-size: 12px; margin-bottom: 4px; }
.node .det { color: var(--text-muted); font-size: 10px; }
.node.start { background: var(--node-fill-mech); border-color: var(--accent-2); }
.node.danger { background: var(--node-fill-danger); border-color: var(--semantic-error); }
.node.danger .lbl { color: var(--semantic-error); }
.node.ok { background: var(--node-fill-ok); border-color: var(--semantic-success); }
.node.ok .lbl { color: var(--semantic-success); }
.node.decision {
  width: 220px;
  background: var(--node-fill-accent);
  border: 2px solid var(--accent);
  border-radius: 8px;
}
.node.decision .lbl { color: var(--accent); }
.node.subcore {
  background: var(--node-fill-accent);
  border-color: var(--accent);
  border-left-width: 4px;
}

svg.connectors { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; }
.arrow-line { stroke: var(--cover-block); stroke-width: 1.5; fill: none; marker-end: url(#arr2); }
.arrow-line.yes { stroke: var(--semantic-success); }
.arrow-line.no { stroke: var(--semantic-error); }
.edge-label { font-size: 10px; font-weight: 700; fill: var(--header-fill); }

/* positions */
.n1 { left: 60px; top: 100px; }
.n2 { left: 320px; top: 100px; }
.n3 { left: 580px; top: 100px; }
.n4 { left: 840px; top: 100px; }
.n5 { left: 1100px; top: 100px; }
.d1 { left: 540px; top: 280px; }
.n6a { left: 250px; top: 460px; }
.n6b { left: 800px; top: 460px; }
.d2 { left: 800px; top: 620px; }
.n7a { left: 540px; top: 760px; }
.n7b { left: 1060px; top: 760px; }

.p1 { left: 60px; top: 60px; }
.p2 { left: 60px; top: 240px; }
.p3 { left: 60px; top: 440px; }
.p4 { left: 60px; top: 600px; }
</style>
</head>
<body>
<div class="canvas">
  <div class="title-bar">Flusso di Danno — Penetrazione al Subcore</div>
  <div class="subtitle">Modello vanilla Exosuit Framework con subcore come body part interna</div>

  <div class="phase p1">Fase 1 — Hit & Armor</div>
  <div class="phase p2">Fase 2 — Body Part Selection</div>
  <div class="phase p3">Fase 3 — Subcore Hit?</div>
  <div class="phase p4">Fase 4 — Esito</div>

  <div class="node start n1">
    <div class="lbl">Colpo ricevuto</div>
    <div class="det">DamageInfo<br>(amount, Def, angle)</div>
  </div>
  <div class="node n2">
    <div class="lbl">Armor Check</div>
    <div class="det">ArmorRating_Sharp/Blunt<br>vanilla penetration roll</div>
  </div>
  <div class="node n3">
    <div class="lbl">Damage Taken</div>
    <div class="det">Mech HP -= amount<br>(health pool principale)</div>
  </div>
  <div class="node n4">
    <div class="lbl">Body Part Roll</div>
    <div class="det">BodyDef custom<br>coverage ponderata</div>
  </div>
  <div class="node subcore n5">
    <div class="lbl">Subcore body part</div>
    <div class="det">coverage = 0.10<br>HP separato: 100/175</div>
  </div>

  <div class="node decision d1">
    <div class="lbl">Subcore colpito?</div>
    <div class="det">roll su coverage 10%</div>
  </div>

  <div class="node ok n6a">
    <div class="lbl">NO — Solo mech</div>
    <div class="det">Subcore HP invariato<br>nessun danno aggiuntivo</div>
  </div>

  <div class="node danger n6b">
    <div class="lbl">SÌ — Subcore danneggiato</div>
    <div class="det">Subcore.HP -= amount<br>(stesso amount del colpo)</div>
  </div>

  <div class="node decision d2">
    <div class="lbl">Subcore HP &lt;= 0?</div>
  </div>

  <div class="node danger n7a">
    <div class="lbl">SÌ — Subcore Destroyed</div>
    <div class="det">Spawn "Destroyed [Std/High] Subcore"<br>Mech va in "braindead" state<br>(downed, non più riparabile)</div>
  </div>

  <div class="node ok n7b">
    <div class="lbl">NO — Subcore sopravvive</div>
    <div class="det">Mech continua a operare<br>HP subcore ridotto permane<br>fino a riparazione in bay</div>
  </div>

  <svg class="connectors" viewBox="0 0 1400 850" preserveAspectRatio="none">
    <defs>
      <marker id="arr2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
        <path d="M0,0 L10,5 L0,10 z" fill="var(--cover-block)"/>
      </marker>
    </defs>
    <path class="arrow-line" d="M 260,140 L 320,140" />
    <path class="arrow-line" d="M 520,140 L 580,140" />
    <path class="arrow-line" d="M 780,140 L 840,140" />
    <path class="arrow-line" d="M 1040,140 L 1100,140" />
    <path class="arrow-line" d="M 640,170 L 640,280" />
    <path class="arrow-line no" d="M 540,330 L 350,460" />
    <text x="380" y="400" class="edge-label">NO (90%)</text>
    <path class="arrow-line yes" d="M 740,330 L 900,460" />
    <text x="830" y="400" class="edge-label">SÌ (10%)</text>
    <path class="arrow-line" d="M 900,510 L 900,620" />
    <path class="arrow-line no" d="M 800,670 L 640,760" />
    <text x="650" y="720" class="edge-label">SÌ</text>
    <path class="arrow-line yes" d="M 1020,670 L 1160,760" />
    <text x="1080" y="720" class="edge-label">NO</text>
  </svg>
</div>
</body>
</html>
"""

# ─── Diagram 3: Death & Relic Flow ─────────────────────────────────────────
DIAGRAM_3_HTML = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<title>Flusso di Morte e Recupero</title>
<style>
""" + PALETTE_CSS + """
.canvas { width: 1400px; height: 800px; padding: 30px; }
.title-bar { font-size: 24px; font-weight: 700; color: var(--header-fill); margin-bottom: 6px; border-bottom: 2px solid var(--accent); padding-bottom: 6px; }
.subtitle { font-size: 13px; color: var(--text-muted); margin-bottom: 30px; }

.phase {
  position: absolute;
  font-size: 10px;
  font-weight: 700;
  color: var(--header-fill);
  text-transform: uppercase;
  letter-spacing: 2px;
  padding: 4px 10px;
  background: var(--card-bg);
  border-left: 3px solid var(--accent);
}

.node {
  position: absolute;
  width: 200px;
  background: var(--node-fill);
  border: 1.5px solid var(--border);
  border-radius: 4px;
  padding: 12px;
  font-size: 11px;
  line-height: 1.5;
  text-align: center;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}
.node .lbl { font-weight: 700; color: var(--header-fill); font-size: 12px; margin-bottom: 4px; }
.node .det { color: var(--text-muted); font-size: 10px; }
.node.start { background: var(--node-fill-mech); border-color: var(--accent-2); }
.node.danger { background: var(--node-fill-danger); border-color: var(--semantic-error); }
.node.ok { background: var(--node-fill-ok); border-color: var(--semantic-success); }
.node.special {
  background: var(--node-fill-accent);
  border: 2px dashed var(--accent);
}
.node.special .lbl { color: var(--accent); }

svg.connectors { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; }
.arrow-line { stroke: var(--cover-block); stroke-width: 1.5; fill: none; marker-end: url(#arr3); }
.arrow-line.danger { stroke: var(--semantic-error); }
.arrow-line.ok { stroke: var(--semantic-success); }
.edge-label { font-size: 10px; font-weight: 700; fill: var(--header-fill); }

.n1 { left: 60px; top: 100px; }
.d1 { left: 320px; top: 100px; width: 240px; background: var(--node-fill-accent); border: 2px solid var(--accent); border-radius: 8px; }
.n2a { left: 640px; top: 100px; }
.n2b { left: 900px; top: 100px; }
.n3 { left: 1140px; top: 100px; width: 220px; }

.n4 { left: 1140px; top: 280px; width: 220px; }
.n5 { left: 1140px; top: 460px; width: 220px; }

.d2 { left: 700px; top: 460px; width: 240px; background: var(--node-fill-accent); border: 2px solid var(--accent); border-radius: 8px; }
.n6a { left: 380px; top: 460px; }
.n6b { left: 60px; top: 460px; }

.n7 { left: 60px; top: 640px; }

.p1 { left: 60px; top: 60px; }
.p2 { left: 60px; top: 260px; }
.p3 { left: 60px; top: 440px; }
.p4 { left: 60px; top: 620px; }
</style>
</head>
<body>
<div class="canvas">
  <div class="title-bar">Flusso di Morte → Relitto → Recupero</div>
  <div class="subtitle">Sistema deterministico basato su HP residui del subcore al momento della morte</div>

  <div class="phase p1">Fase 1 — Morte del mech</div>
  <div class="phase p2">Fase 2 — Drop del relitto</div>
  <div class="phase p3">Fase 3 — Smontaggio del relitto</div>
  <div class="phase p4">Fase 4 — Esito finale</div>

  <div class="node start n1">
    <div class="lbl">Mech HP = 0</div>
    <div class="det">Distruzione in combattimento</div>
  </div>

  <div class="node d1">
    <div class="lbl">Subcore era già morto?</div>
    <div class="det">(HP subcore = 0 al momento della morte mech)</div>
  </div>

  <div class="node danger n2a">
    <div class="lbl">SÌ — Braindead</div>
    <div class="det">Spawn "Destroyed [Std/High] Subcore"<br>Relitto = solo materiali</div>
  </div>

  <div class="node ok n2b">
    <div class="lbl">NO — Subcore vivo</div>
    <div class="det">Subcore entra in relitto<br>con HP residui</div>
  </div>

  <div class="node special n3">
    <div class="lbl">Relitto Sigillato di [Suit]</div>
    <div class="det">ThingDef custom<br>destroyOnDrop: false<br>richiede smontaggio</div>
  </div>

  <div class="node n4">
    <div class="lbl">Pawn esegue JobDriver_DismantleRelic</div>
    <div class="det">200 ticks di lavoro<br>(machining table o bay)</div>
  </div>

  <div class="node n5">
    <div class="lbl">Roll deterministico</div>
    <div class="det">HP_recuperati =<br>HP_residui_morte × 0.70<br>(min 10%, max 100%)</div>
  </div>

  <div class="node d2">
    <div class="lbl">HP residui &gt; soglia?</div>
    <div class="det">soglia = 30% del max HP</div>
  </div>

  <div class="node ok n6a">
    <div class="lbl">SÌ — Subcore recuperato</div>
    <div class="det">Spawn "[Std/High] Subcore"<br>HP = 70% dei residui<br>SubcoreInfo: identità preservata</div>
  </div>

  <div class="node danger n6b">
    <div class="lbl">NO — Subcore distrutto</div>
    <div class="det">Spawn "Destroyed [Std/High] Subcore"<br>+ materiali del relitto</div>
  </div>

  <div class="node special n7">
    <div class="lbl">Subcore recuperato riutilizzabile</div>
    <div class="det">HP ridotti → più fragile al prossimo blow-through<br>Cumula con subcore già danneggiati<br>Reinstallabile in nuova suit</div>
  </div>

  <svg class="connectors" viewBox="0 0 1400 800" preserveAspectRatio="none">
    <defs>
      <marker id="arr3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
        <path d="M0,0 L10,5 L0,10 z" fill="var(--cover-block)"/>
      </marker>
    </defs>
    <path class="arrow-line" d="M 260,140 L 320,140" />
    <path class="arrow-line danger" d="M 560,140 L 640,140" />
    <text x="580" y="130" class="edge-label">SÌ</text>
    <path class="arrow-line ok" d="M 560,170 L 900,140" />
    <text x="700" y="130" class="edge-label">NO</text>
    <path class="arrow-line danger" d="M 840,140 L 1140,200" />
    <path class="arrow-line ok" d="M 1100,140 L 1140,140" />
    <path class="arrow-line" d="M 1240,200 L 1240,280" />
    <path class="arrow-line" d="M 1240,340 L 1240,460" />
    <path class="arrow-line" d="M 1140,490 L 940,490" />
    <path class="arrow-line ok" d="M 700,490 L 580,490" />
    <text x="600" y="480" class="edge-label">SÌ</text>
    <path class="arrow-line danger" d="M 700,520 L 260,490" />
    <text x="400" y="510" class="edge-label">NO</text>
    <path class="arrow-line ok" d="M 380,520 L 160,640" />
  </svg>
</div>
</body>
</html>
"""

# ─── Diagram 4: Hybrid Bay Schema ──────────────────────────────────────────
DIAGRAM_4_HTML = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<title>Schema Bay Ibrida</title>
<style>
""" + PALETTE_CSS + """
.canvas { width: 1400px; height: 800px; padding: 30px; }
.title-bar { font-size: 24px; font-weight: 700; color: var(--header-fill); margin-bottom: 6px; border-bottom: 2px solid var(--accent); padding-bottom: 6px; }
.subtitle { font-size: 13px; color: var(--text-muted); margin-bottom: 30px; }

.bay-container {
  position: absolute;
  left: 100px;
  top: 100px;
  width: 1200px;
  height: 580px;
  background: var(--node-fill);
  border: 3px solid var(--accent);
  border-radius: 6px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 60px 1fr 1fr;
  gap: 0;
}
.bay-header {
  grid-column: 1 / 3;
  background: var(--header-fill);
  color: white;
  padding: 18px 24px;
  font-size: 18px;
  font-weight: 700;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.bay-header .sub { font-size: 12px; font-weight: 400; opacity: 0.8; }

.function-block {
  padding: 18px;
  border: 1px solid var(--border);
  margin: 12px;
  border-radius: 4px;
  background: var(--card-bg);
  position: relative;
}
.function-block .num {
  position: absolute;
  top: -10px;
  left: 12px;
  background: var(--accent);
  color: white;
  padding: 2px 10px;
  font-size: 11px;
  font-weight: 700;
  border-radius: 3px;
}
.function-block .ftitle {
  font-size: 16px;
  font-weight: 700;
  color: var(--header-fill);
  margin-bottom: 8px;
  padding-top: 6px;
}
.function-block .fdesc {
  font-size: 11px;
  color: var(--text-muted);
  line-height: 1.5;
}
.function-block .fitems {
  margin-top: 8px;
  font-size: 10px;
  color: var(--text-primary);
  font-family: 'Liberation Mono', monospace;
  line-height: 1.6;
}
.function-block .fitems li {
  list-style: none;
  padding-left: 12px;
  position: relative;
}
.function-block .fitems li::before {
  content: '▸';
  position: absolute;
  left: 0;
  color: var(--accent);
}

.io-band {
  position: absolute;
  height: 40px;
  background: var(--node-fill-mech);
  border: 1px solid var(--accent-2);
  border-radius: 4px;
  padding: 8px 16px;
  font-size: 11px;
  color: var(--header-fill);
  display: flex;
  align-items: center;
  gap: 12px;
}
.io-band.in { left: 60px; top: 710px; }
.io-band.out { right: 60px; top: 710px; }
.io-band .lbl { font-weight: 700; color: var(--accent-2); }
.io-band .items { color: var(--text-muted); }

.note {
  position: absolute;
  left: 100px;
  top: 720px;
  font-size: 10px;
  color: var(--text-muted);
  width: 1200px;
  text-align: center;
  font-style: italic;
}
</style>
</head>
<body>
<div class="canvas">
  <div class="title-bar">Schema Bay Ibrida — 4 Funzioni Integrate</div>
  <div class="subtitle">Building_HybridGestator estende Building_MaintenanceBay (Exosuit Framework)</div>

  <div class="bay-container">
    <div class="bay-header">
      <span>Building_HybridGestator</span>
      <span class="sub">3×3 | Standard Mechtech | 250 steel + 8 components + 1 subcore encoder module</span>
    </div>

    <div class="function-block">
      <div class="num">F1</div>
      <div class="ftitle">Loadout UI</div>
      <div class="fdesc">Selezione frame + armi (replica ITab_Exosuit di Exosuit Framework)</div>
      <ul class="fitems">
        <li>ITab_HybridBay custom</li>
        <li>Slot supportati: Core, Head, Arms, Mounts</li>
        <li>Carica moduli da ThingDef</li>
        <li>Salva configurazione su bay</li>
      </ul>
    </div>

    <div class="function-block">
      <div class="num">F2</div>
      <div class="ftitle">Gestazione Mech</div>
      <div class="fdesc">Costruisce il mech-exosuit a partire da subcore + materiali</div>
      <ul class="fitems">
        <li>RecipeDef custom per suit</li>
        <li>Consuma: Subcore + Steel + Components</li>
        <li>Tempo: 8h gioco (modulabile)</li>
        <li>Richiede pawn crafter (Craft ≥ 8)</li>
        <li>Output: Pawn (MechExosuitRace)</li>
      </ul>
    </div>

    <div class="function-block">
      <div class="num">F3</div>
      <div class="ftitle">Charging Station</div>
      <div class="fdesc">Ricarica la batteria del mech-exosuit dockato</div>
      <ul class="fitems">
        <li>CompMechExosuitBattery ↔ bay</li>
        <li>Solo mech dockato qui si ricarica</li>
        <li>Vanilla mech charger: NON compatibile</li>
        <li>TheDeadmanswitch charger: NON compatibile</li>
        <li>Consumo: 5 W/tick (da rete elettrica)</li>
      </ul>
    </div>

    <div class="function-block">
      <div class="num">F4</div>
      <div class="ftitle">Subcore Install/Extract</div>
      <div class="fdesc">Comandi floating menu per gestione subcore</div>
      <ul class="fitems">
        <li>Installa: Subcore → mech vuoto</li>
        <li>Estrai: Mech dockato → Subcore + Frame item</li>
        <li>SubcoreInfo.CopySubcoreInfo() su entrambi</li>
        <li>Disponibile solo quando mech è fermo in bay</li>
      </ul>
    </div>
  </div>

  <div class="io-band in">
    <span class="lbl">INPUT:</span>
    <span class="items">Subcore (Std/High) · Steel · Components · Plasteel · Chemfuel (per charging) · Pawn crafter</span>
  </div>

  <div class="io-band out">
    <span class="lbl">OUTPUT:</span>
    <span class="items">Mech-Exosuit (Pawn) · Subcore recuperato (su estrazione) · Frame item (su estrazione)</span>
  </div>
</div>
</body>
</html>
"""

# ─── Write HTML files ──────────────────────────────────────────────────────
DIAGRAMS = [
    ("architecture_class_diagram", DIAGRAM_1_HTML, 1400, 1000),
    ("damage_flow",                 DIAGRAM_2_HTML, 1400, 850),
    ("death_flow",                  DIAGRAM_3_HTML, 1400, 800),
    ("bay_schema",                  DIAGRAM_4_HTML, 1400, 800),
]

for name, html, w, h in DIAGRAMS:
    out_html = DIAGRAMS_DIR / f"{name}.html"
    out_html.write_text(html, encoding="utf-8")
    print(f"Written: {out_html}")

# ─── Render to PNG via Playwright ──────────────────────────────────────────
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    for name, html, w, h in DIAGRAMS:
        out_png = DIAGRAMS_DIR / f"{name}.png"
        page = browser.new_page(viewport={"width": w + 60, "height": h + 60}, device_scale_factor=2)
        page.goto(f"file://{DIAGRAMS_DIR / (name + '.html')}")
        page.wait_for_load_state("networkidle")
        # screenshot the .canvas element specifically
        canvas = page.locator(".canvas")
        canvas.screenshot(path=str(out_png), type="png")
        page.close()
        print(f"Rendered: {out_png}")
    browser.close()

print("\nAll diagrams rendered successfully.")
