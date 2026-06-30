"""Section 3: Schema Defs XML"""

from reportlab.platypus import Spacer


def build_section_03(story, ctx):
    h = ctx['heading']; so = ctx['section_opener']
    body = ctx['body']; bl = ctx['bullet_list']; cb = ctx['callout_box']
    dt = ctx['data_table']; cap = ctx['caption']
    P = ctx['Paragraph']; HR = ctx['HRFlowable']; KT = ctx['KeepTogether']
    code_block = ctx['code_block']
    
    story.extend(so('Capitolo 03 · Defs XML', 'Schema Defs XML',
                    chapter_num=3))
    
    story.append(body(
        "Questa sezione presenta gli schemi XML delle Def principali. Per "
        "ciascuna Def sono mostrati gli attributi essenziali e i collegamenti "
        "alle classi C# introdotte nella Sezione 2. Gli snippet sono "
        "<b>rappresentativi ma non completi</b>: i valori concreti (costi "
        "esatti, stat numeriche, texPath) sono in Sezione 8 (Bilanciamento) "
        "e nei file di texture dedicati."
    , ctx['styles']['BodyLead']))
    
    # ── 3.1 ThingDef Building_HybridGestator ──
    story.append(P('<b>3.1 — ThingDef: Building_HybridGestator</b>', ctx['styles']['H2']))
    story.append(body(
        "La bay ibrida è definita come ThingDef che eredita da "
        "<code>MaintanenceBayBase</code> di Exosuit Framework. La classe "
        "C# custom (<code>ModName.Building_HybridGestator</code>) sostituisce "
        "la <code>thingClass</code> di default, e l'<code>ITab_HybridBay</code> "
        "viene registrato via <code>inspectorTabs</code>."
    ))
    
    story.append(code_block('''<!-- Defs/ThingDefs_HybridGestator.xml -->
<Defs>

  <ThingDef ParentName="MaintanenceBayBase">  <!-- da Exosuit Framework -->
    <defName>ModName_HybridGestator</defName>
    <label>hybrid gestator bay</label>
    <description>Una stazione di gestazione ibrida che combina le funzioni
    di Maintenance Bay (Exosuit Framework) e Mech Gestator (vanilla).
    Permette di costruire mech-exosuit pilotati da subcore, configurarne
    il loadout, ricaricarli e gestire l'installazione/estrazione del
    subcore. Solo mech-exosuit possono essere ricaricati qui; i charger
    vanilla e di altri mod non funzionano su di essi.</description>

    <thingClass>ModName.Building_HybridGestator</thingClass>
    <graphicData>
      <texPath>Things/Building/HybridGestator</texPath>
      <graphicClass>Graphic_Multi</graphicClass>
      <drawSize>(4,4)</drawSize>
    </graphicData>
    <uiIconPath>Things/Building/HybridGestator_Icon</uiIconPath>

    <statBases>
      <MaxHitPoints>250</MaxHitPoints>
      <WorkToBuild>8000</WorkToBuild>
      <Flammability>0.5</Flammability>
    </statBases>

    <size>(3,3)</size>
    <costList>
      <Steel>250</Steel>
      <ComponentIndustrial>8</ComponentIndustrial>
      <ComponentSpacer>2</ComponentSpacer>
      <SubcoreEncoderModule>1</SubcoreEncoderModule>  <!-- vanilla 1.6 -->
    </costList>

    <researchPrerequisites>
      <li>ModName_HybridMechtech</li>  <!-- vedi Sezione 9 -->
    </researchPrerequisites>

    <!-- ITab custom per la UI ibrida -->
    <inspectorTabs>
      <li>ModName.ITab_HybridBay</li>
    </inspectorTabs>

    <comps>
      <li Class="CompProperties_AffectedByFacilities">
        <linkableFacilities>
          <li>MF_Building_ComponentStorage</li>
          <li>MF_Building_PayloadStorage</li>
          <li>ToolCabinet</li>
        </linkableFacilities>
      </li>
      <li Class="CompProperties_Power">
        <compClass>CompPowerTrader</compClass>
        <basePowerConsumption>350</basePowerConsumption>  <!-- per charging -->
      </li>
      <li Class="CompProperties_Flickable" />
      <li Class="CompProperties_Facility" />
    </comps>

    <modExtensions>
      <li Class="ModName.HybridGestatorExt">
        <supportedRecipes>
          <li>ModName_MakePatriotMechExosuit</li>
          <!-- altre suit aggiunte qui -->
        </supportedRecipes>
        <chargingRate>5</chargingRate>  <!-- W per tick -->
      </li>
    </modExtensions>
  </ThingDef>

</Defs>'''))
    
    # ── 3.2 PawnKindDef + ThingDef mech-exosuit ──
    story.append(P('<b>3.2 — PawnKindDef + ThingDef: Mech-Exosuit Race</b>',
                   ctx['styles']['H2']))
    story.append(body(
        "Il mech-exosuit è un pawn che eredita da <code>BaseMechanoid</code> "
        "(vanilla) e monta i nostri ThingComp (<code>CompSubcorePilot</code> "
        "e <code>CompMechExosuitBattery</code>) via <code>comps</code>. "
        "Il <code>BodyDef</code> custom (Sezione 3.3) definisce il subcore "
        "come body part interna."
    ))
    
    story.append(code_block('''<!-- Defs/PawnKindDefs_MechExosuit.xml -->
<Defs>

  <!-- ThingDef della razza (race) -->
  <ThingDef ParentName="BaseMechanoid">
    <defName>ModName_MechExosuitRace_Patriot</defName>
    <label>EXO-45 Patriot Mech-Exosuit</label>
    <description>Una variante mech-piloted della Patriot Exosuit. Il
    pilota è un subcore Standard o High installato fisicamente come
    body part interna. Operativo fino a quando il subcore ha HP e la
    batteria ha energia.</description>

    <race>
      <body>ModName_MechExosuitBody</body>  <!-- BodyDef custom, vedi 3.3 -->
      <meatCount>0</meatCount>
      <leatherDef>NULL</leatherDef>
      <intelligence>ToolUser</intelligence>
      <makesFootprints>true</makesFootshots>
      <lifeExpectancy>2000</lifeExpectancy>
      <bloodColor>(90, 70, 50)</bloodColor>  <!-- olio/color rame -->
    </race>

    <statBases>
      <MoveSpeed>3.5</MoveSpeed>
      <ArmorRating_Sharp>1.70</ArmorRating_Sharp>
      <ArmorRating_Blunt>1.80</ArmorRating_Blunt>
      <ArmorRating_Heat>1.5</ArmorRating_Heat>
      <MaxHitPoints>300</MaxHitPoints>  <!-- mech HP, separato da subcore -->
      <MarketValue>3500</MarketValue>
    </statBases>

    <tools>
      <li>
        <label>stomp</label>
        <capacities>
          <li>Blunt</li>
        </capacities>
        <power>30</power>
        <cooldownTime>2.0</cooldownTime>
      </li>
    </tools>

    <comps>
      <!-- I nostri due Comp custom -->
      <li Class="ModName.CompProperties_SubcorePilot" />
      <li Class="ModName.CompProperties_MechExosuitBattery">
        <maxEnergyTicks>36000</maxEnergyTicks>  <!-- ~12h gioco -->
      </li>

      <!-- Vanilla mech comps -->
      <li Class="CompProperties_OverseerSubject" />
      <li Class="CompProperties_MechEnergy" />  <!-- disabilitato via patch -->
      <li Class="CompProperties_Flickable" />
    </comps>

    <modExtensions>
      <li Class="ModName.MechExosuitExt">
        <baseSkillBonus>0</baseSkillBonus>  <!-- incrementato da subcore High -->
        <supportedJobs>
          <li>Violent</li>
          <li>Firefighter</li>
          <li>Construction</li>
        </supportedJobs>
        <sourceApparelDef>Aqued_Exosuit_Apparel_Core</sourceApparelDef>
      </li>
    </modExtensions>
  </ThingDef>

  <!-- PawnKindDef -->
  <PawnKindDef ParentName="BaseMechanoidKind">
    <defName>ModName_MechExosuit_Patriot</defName>
    <label>Patriot Mech-Exosuit</label>
    <race>ModName_MechExosuitRace_Patriot</race>
    <combatPower>350</combatPower>
    <lifeStages>
      <li>
        <label>operative</label>
        <visible>true</visible>
      </li>
    </lifeStages>
  </PawnKindDef>

</Defs>'''))
    
    # ── 3.3 BodyDef ──
    story.append(P('<b>3.3 — BodyDef: MechExosuitBody (con subcore come body part)</b>',
                   ctx['styles']['H2']))
    story.append(body(
        "Il BodyDef custom è il cuore del sistema di danno. Definisce il "
        "subcore come body part interna con <b>coverage 0.10</b> (10% dei "
        "colpi che penetrano l'armatura colpiscono il subcore). Il subcore "
        "ha i suoi HP separati dall'HP del mech, gestiti dal "
        "<code>CompSubcorePilot</code>."
    ))
    
    story.append(code_block('''<!-- Defs/BodyDefs_MechExosuit.xml -->
<Defs>

  <BodyDef>
    <defName>ModName_MechExosuitBody</defName>
    <label>mech-exosuit body</label>
    <corePart>
      <def>Torso</def>
      <height>Middle</height>
      <depth>Outside</depth>
      <groups>
        <li>Torso</li>
      </groups>
      <parts>
        <!-- Subcore: body part interna, profondità Inside, coverage bassa -->
        <li>
          <def>ModName_Subcore</def>
          <customLabel>subcore</customLabel>
          <coverage>0.10</coverage>
          <depth>Inside</Depth>
          <groups>
            <li>ModName_SubcoreGroup</li>
          </groups>
          <hitPoints>100</hitPoints>  <!-- override per Standard; High: 175 via Patch -->
        </li>

        <!-- Head (sensor cluster) -->
        <li>
          <def>Head</def>
          <coverage>0.10</coverage>
          <height>Top</height>
          <parts>
            <li>
              <def>Eye</def>
              <customLabel>left sensor</customLabel>
              <coverage>0.05</coverage>
            </li>
            <li>
              <def>Eye</def>
              <customLabel>right sensor</customLabel>
              <coverage>0.05</coverage>
            </li>
          </parts>
        </li>

        <!-- Arms (per slot ArmLeft/ArmRight) -->
        <li>
          <def>Shoulder</def>
          <customLabel>left shoulder</customLabel>
          <coverage>0.10</coverage>
          <parts>
            <li>
              <def>Arm</def>
              <customLabel>left arm</customLabel>
              <coverage>0.10</coverage>
            </li>
          </parts>
        </li>
        <li>
          <def>Shoulder</def>
          <customLabel>right shoulder</customLabel>
          <coverage>0.10</coverage>
          <parts>
            <li>
              <def>Arm</def>
              <customLabel>right arm</customLabel>
              <coverage>0.10</coverage>
            </li>
          </parts>
        </li>

        <!-- Legs -->
        <li>
          <def>Leg</def>
          <customLabel>left leg</customLabel>
          <coverage>0.15</coverage>
        </li>
        <li>
          <def>Leg</def>
          <customLabel>right leg</customLabel>
          <coverage>0.15</coverage>
        </li>
      </parts>
    </corePart>
  </BodyDef>

</Defs>'''))
    
    story.append(cb(
        'Perché coverage 0.10?',
        'Coverage 0.10 significa che il 10% dei colpi che penetrano l\'armatura '
        'colpiscono il subcore. Questo è un valore deliberatamente basso: il '
        'subcore è protetto dal frame dell\'exosuit (lore: è nel torso, dietro '
        'la corazza). Un valore più alto (0.20+) renderebbe il sistema troppo '
        'punitivo — ogni raid danneggerebbe il subcore. 0.10 crea invece '
        'eventi rari ma significativi: il subcore viene colpito in media '
        'una volta ogni 10 colpi subiti, dando al giocatore tempo di ritirare '
        'il mech prima che sia troppo tardi.',
        color=ctx['colors']['accent']
    ))
    
    # ── 3.4 SealedRelic ThingDef + CompRelic ──
    story.append(P('<b>3.4 — ThingDef: Relitto Sigillato + CompRelic</b>',
                   ctx['styles']['H2']))
    story.append(body(
        "Il Relitto Sigillato è un item che droppa quando il mech-exosuit "
        "muore. Non può essere aperto istantaneamente: richiede un pawn che "
        "esegua il <code>JobDriver_DismantleRelic</code> (200 ticks di "
        "lavoro, equivalente a ~3 minuti di gioco). Il <code>CompRelic</code> "
        "conserva lo stato del subcore al momento della morte del mech "
        "(HP residui, tier, identità SubcoreInfo)."
    ))
    
    story.append(code_block('''<!-- Defs/ThingDefs_Relics.xml -->
<Defs>

  <ThingDef ParentName="ItemBase">
    <defName>ModName_SealedRelic_Patriot</defName>
    <label>sealed relic of Patriot mech-exosuit</label>
    <description>I resti contorti di un Patriot Mech-Exosuit distrutto.
    Il relitto è sigillato; non è possibile sapere se il subcore interno
    è sopravvissuto finché non viene aperto. Lo smontaggio richiede
    lavoro manuale e produce: subcore recuperato (se sopravvissuto) o
    destroyed subcore, più materiali del frame.</description>

    <graphicData>
      <texPath>Things/Item/SealedRelic_Patriot</texPath>
      <graphicClass>Graphic_Single</graphicClass>
      <drawSize>(2,2)</drawSize>
    </graphicData>

    <statBases>
      <MaxHitPoints>100</MaxHitPoints>
      <Mass>80</Mass>
      <MarketValue>400</MarketValue>  <!-- solo materiali -->
      <Flammability>0</Flammability>
    </statBases>

    <thingCategories>
      <li>ModName_Relics</li>
    </thingCategories>

    <destroyOnDrop>false</destroyOnDrop>
    <tradeability>None</tradeability>  <!-- non vendibile, deve essere aperto -->
    <comps>
      <li Class="CompProperties_Forbiddable" />
      <li Class="ModName.CompProperties_Relic">
        <dismantleRecipe>ModName_DismantleRelic_Patriot</dismantleRecipe>
        <destroyedSubcoreDef>ModName_DestroyedSubcore_Standard</destroyedSubcoreDef>
        <destroyedSubcoreDefHigh>ModName_DestroyedSubcore_High</destroyedSubcoreDefHigh>
        <materialYield>
          <Steel>120</Steel>
          <Plasteel>40</Plasteel>
          <ComponentIndustrial>3</ComponentIndustrial>
        </materialYield>
      </li>
    </comps>
  </ThingDef>

</Defs>'''))
    
    # ── 3.5 Destroyed Subcore ──
    story.append(P('<b>3.5 — ThingDef: Destroyed Subcore</b>', ctx['styles']['H2']))
    story.append(body(
        "Quando il subcore viene distrutto (HP = 0 in combattimento, o "
        "roll fallito all'apertura del relitto), droppa un <b>Destroyed "
        "Subcore</b>. Questo item non ha utilizzo diretto: può essere "
        "smontato al machining table per recuperare acciaio e componenti. "
        "Esistono due varianti (Standard/High) che differiscono solo "
        "nell'aspetto grafico e nei materiali resi."
    ))
    
    story.append(code_block('''<!-- Defs/ThingDefs_DestroyedSubcore.xml -->
<Defs>

  <ThingDef ParentName="ItemBase">
    <defName>ModName_DestroyedSubcore_Standard</defName>
    <label>destroyed standard subcore</label>
    <description>Un subcore Standard andato irrimediabilmente distrutto.
    Non è più utilizzabile come pilota per mech-exosuit. Può essere
    smontato al machining table per recuperare acciaio e componenti.</description>

    <graphicData>
      <texPath>Things/Item/DestroyedSubcore_Standard</texPath>
      <graphicClass>Graphic_Single</graphicClass>
    </graphicData>
    <statBases>
      <MaxHitPoints>50</MaxHitPoints>
      <Mass>2</Mass>
      <MarketValue>40</MarketValue>
    </statBases>
    <thingCategories>
      <li>Items</li>
    </thingCategories>

    <tradeability>Sellable</tradeability>
    <smeltProducts>
      <Steel>15</Steel>
      <ComponentIndustrial>1</ComponentIndustrial>
    </smeltProducts>

    <recipeMaker>
      <recipeUsers>
        <li>TableMachining</li>
      </recipeUsers>
      <smeltProductsOverride>  <!-- se smontato al machining table -->
        <Steel>20</Steel>
        <ComponentIndustrial>1</ComponentIndustrial>
      </smeltProductsOverride>
    </recipeMaker>
  </ThingDef>

  <!-- Variante High: stessi pattern, più materiali resi -->
  <ThingDef ParentName="ItemBase">
    <defName>ModName_DestroyedSubcore_High</defName>
    <label>destroyed high subcore</label>
    <description>Un subcore High andato irrimediabilmente distrutto...</description>
    <graphicData>
      <texPath>Things/Item/DestroyedSubcore_High</texPath>
      <graphicClass>Graphic_Single</graphicClass>
    </graphicData>
    <statBases>
      <MaxHitPoints>50</MaxHitPoints>
      <Mass>3</Mass>
      <MarketValue>80</MarketValue>
    </statBases>
    <thingCategories>
      <li>Items</li>
    </thingCategories>
    <smeltProducts>
      <Steel>25</Steel>
      <ComponentIndustrial>2</ComponentIndustrial>
      <ComponentSpacer>1</ComponentSpacer>
    </smeltProducts>
  </ThingDef>

</Defs>'''))
    
    # ── 3.6 RecipeDefs ──
    story.append(P('<b>3.6 — RecipeDefs: crafting e smontaggio</b>', ctx['styles']['H2']))
    story.append(body(
        "Tre RecipeDef principali: (1) la ricetta di gestazione del mech "
        "(consuma subcore + materiali, eseguita nella bay ibrida); "
        "(2) la ricetta di smontaggio del relitto (eseguita dal pawn "
        "direttamente sul relitto, non in una bay); (3) la ricetta di "
        "smontaggio del Destroyed Subcore al machining table."
    ))
    
    story.append(code_block('''<!-- Defs/RecipeDefs_MechExosuit.xml -->
<Defs>

  <!-- 1. Gestazione mech-exosuit (eseguita nella bay ibrida) -->
  <RecipeDef ParentName="MechResurrectBase">  <!-- o simile vanilla -->
    <defName>ModName_MakePatriotMechExosuit</defName>
    <label>gestate Patriot mech-exosuit</label>
    <description>Gestisce un Patriot Mech-Exosuit usando un subcore
    Standard o High e i materiali del frame.</description>
    <jobString>Gestating Patriot mech-exosuit.</jobString>
    <workAmount>60000</workAmount>  <!-- 8h gioco con 1 crafter -->
    <skillRequirements>
      <Crafting>8</Crafting>
    </skillRequirements>

    <ingredients>
      <li>
        <filter>
          <thingDefs>
            <li>SubcoreRegular</li>
            <li>SubcoreHigh</li>
          </thingDefs>
        </filter>
        <count>1</count>
      </li>
      <li>
        <filter>
          <thingDefs>
            <li>Steel</li>
          </thingDefs>
        </filter>
        <count>150</count>
      </li>
      <li>
        <filter>
          <thingDefs>
            <li>Plasteel</li>
          </thingDefs>
        </filter>
        <count>250</count>
      </li>
      <li>
        <filter>
          <thingDefs>
            <li>ComponentIndustrial</li>
          </thingDefs>
        </filter>
        <count>10</count>
      </li>
    </ingredients>

    <fixedIngredientFilter>
      <thingDefs>
        <li>SubcoreRegular</li>
        <li>SubcoreHigh</li>
        <li>Steel</li>
        <li>Plasteel</li>
        <li>ComponentIndustrial</li>
      </thingDefs>
    </fixedIngredientFilter>

    <products>
      <ModName_MechExosuitRace_Patriot>1</ModName_MechExosuitRace_Patriot>
    </products>

    <recipeUsers>
      <li>ModName_HybridGestator</li>
    </recipeUsers>
    <researchPrerequisite>ModName_HybridMechtech</researchPrerequisite>
  </RecipeDef>

  <!-- 2. Smontaggio del relitto (eseguito dal pawn sul posto) -->
  <RecipeDef>
    <defName>ModName_DismantleRelic_Patriot</defName>
    <label>dismantle sealed relic</label>
    <description>Apri il relitto sigillato per recuperare il subcore
    (se sopravvissuto) e i materiali del frame.</description>
    <jobString>Dismantling sealed relic.</jobString>
    <workAmount>200</workAmount>  <!-- 200 ticks ≈ 3 secondi reali -->
    <workSpeedStat>GeneralLaborSpeed</workSpeedStat>
    <skillRequirements>
      <Crafting>4</Crafting>
    </skillRequirements>
    <effectWorking>Repair</effectWorking>
    <soundWorking>Recipe_Machining</soundWorking>
    <!-- Non ha ingredients: è un'azione su targetA -->
    <targetCount>1</targetCount>
    <workerCounterClass>ModName.JobDriver_DismantleRelic</workerCounterClass>
  </RecipeDef>

  <!-- 3. Smontaggio Destroyed Subcore al machining table (vanilla) -->
  <!-- (usa smeltProducts del ThingDef, vedi 3.5) -->

</Defs>'''))
    
    # ── 3.7 Directory structure ──
    story.append(P('<b>3.7 — Struttura directory del progetto mod</b>',
                   ctx['styles']['H2']))
    story.append(body(
        "Organizzazione raccomandata per i file della mod, conforme alle "
        "convenzioni RimWorld 1.6 e al pattern di LoadFolders.xml:"
    ))
    
    story.append(code_block('''ModName/
├── About/
│   ├── About.xml                  # metadati mod
│   ├── Preview.png
│   └── PublishedFileId.txt
├── LoadFolders.xml                # supporto 1.4/1.5/1.6
├── Common/                        # file condivisi tra versioni
│   ├── Defs/
│   │   ├── ThingDefs_HybridGestator.xml
│   │   ├── PawnKindDefs_MechExosuit.xml
│   │   ├── BodyDefs_MechExosuit.xml
│   │   ├── ThingDefs_Relics.xml
│   │   ├── ThingDefs_DestroyedSubcore.xml
│   │   ├── RecipeDefs_MechExosuit.xml
│   │   └── ResearchDefs.xml
│   ├── Patches/
│   │   ├── Patch_ExosuitFramework.xml
│   │   ├── Patch_VanillaMechChargers.xml
│   │   └── Patch_MechApparel.xml
│   ├── Textures/
│   │   ├── Things/Building/HybridGestator.png
│   │   ├── Things/Item/SealedRelic_Patriot.png
│   │   ├── Things/Item/DestroyedSubcore_Standard.png
│   │   ├── Things/Item/DestroyedSubcore_High.png
│   │   └── Things/Pawn/MechExosuit_Patriot.png
│   └── Languages/Italiano/Keyed/ModName.xml
├── 1.6/
│   └── Assemblies/
│       └── ModName.dll            # compilato da sorgente C#
├── Source/                        # repo del sorgente C#
│   ├── ModName.sln
│   └── ModName/
│       ├── CompSubcorePilot.cs
│       ├── CompMechExosuitBattery.cs
│       ├── Building_HybridGestator.cs
│       ├── ITab_HybridBay.cs
│       ├── JobDriver_DismantleRelic.cs
│       ├── CompRelic.cs
│       ├── SubcoreInfoBridge.cs
│       ├── HarmonyPatches/
│       │   ├── Patch_TakeDamage.cs
│       │   ├── Patch_MechDeath.cs
│       │   └── Patch_MechCharger.cs
│       └── ModSettings.cs
└── CE/                            # Combat Extended compat (se caricato)
    └── Patches/
        └── Patch_MechExosuitCE.xml'''))
    
    story.append(Spacer(1, 18))
