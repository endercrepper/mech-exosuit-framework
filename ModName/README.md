# ModName/ — Cartella mod per RimWorld 1.6

> **Status: M0 — Hello World Mech**
> 
> Questa è la prima milestone del progetto. Aggiunge solo un mech-exosuit di test (Patriot placeholder) che può essere spawnato via dev mode. Nessuna feature core è ancora implementata.

## 📁 Struttura

```
ModName/
├── About/
│   ├── About.xml                          # metadati mod (packageId, deps)
│   └── Preview.png                        # preview per Steam Workshop
├── LoadFolders.xml                        # supporto 1.6 + CE compat
├── Common/
│   ├── Defs/
│   │   ├── ThingDefs_Race/
│   │   │   └── ModName_MechExosuitRace_Patriot.xml   # ThingDef race custom
│   │   └── PawnKindDefs/
│   │       └── ModName_MechExosuit_Patriot.xml       # PawnKindDef custom
│   └── Textures/
│       └── Things/Pawn/MechExosuit_Patriot/
│           ├── MechExosuit_Patriot_north.png  # placeholder texture (128x128)
│           ├── MechExosuit_Patriot_south.png
│           ├── MechExosuit_Patriot_east.png
│           ├── MechExosuit_Patriot_west.png
│           └── MechExosuit_Patriot_icon.png
├── 1.6/
│   └── Assemblies/                        # qui va la DLL compilata (ModName.dll)
├── Source/                                # sorgente C#
│   ├── ModName.sln                        # soluzione Visual Studio / Rider
│   └── ModName/
│       ├── ModName.csproj                 # progetto .NET Framework 4.8
│       ├── ModName.cs                     # Mod class + MechExosuitExt
│       └── Properties/AssemblyInfo.cs
└── Languages/
    ├── Italiano/Keyed/ModName.xml         # (vuoto per M0)
    └── English/Keyed/ModName.xml          # (vuoto per M0)
```

## 🚀 Come testare M0 in gioco

### Step 1 — Installa le mod dipendenti

Assicurati di avere queste mod installate e attivate in RimWorld 1.6:
- **Harmony** (brrainz.harmony) — prerequisito
- **Exosuit Framework** (aoba.exosuit.framework) — hard dependency

### Step 2 — Copia la cartella ModName nella directory Mods di RimWorld

- **Windows**: `%STEAM%\steamapps\common\RimWorld\Mods\ModName\`
- **Linux**: `~/.steam/steam/steamapps/common/RimWorld/Mods/ModName/`
- **macOS**: `~/Library/Application Support/Steam/steamapps/common/RimWorld/Mods/ModName/`

Verifica che la struttura sia `Mods/ModName/About/About.xml` (non `Mods/ModName/ModName/About/About.xml`).

### Step 3 — Compila la DLL C#

#### Opzione A — Visual Studio / Rider
1. Imposta le variabili d'ambiente:
   ```bash
   # Windows (PowerShell)
   $env:RIMWORLD_DIR = "C:\Steam\steamapps\common\RimWorld"
   $env:EXOSUIT_FRAMEWORK_DIR = "C:\Steam\steamapps\common\RimWorld\Mods\3352894993"
   
   # Linux/macOS
   export RIMWORLD_DIR=/path/to/RimWorld
   export EXOSUIT_FRAMEWORK_DIR=/path/to/RimWorld/Mods/3352894993
   ```
   (Sostituisci `3352894993` con la cartella Workshop di Exosuit Framework — verifica nella tua Mods/)

2. Apri `Source/ModName.sln` in Visual Studio o Rider
3. Build → Release
4. La DLL viene copiata automaticamente in `1.6/Assemblies/ModName.dll` dal post-build event

#### Opzione B — dotnet CLI
```bash
cd ModName/Source
export RIMWORLD_DIR=/path/to/RimWorld
export EXOSUIT_FRAMEWORK_DIR=/path/to/RimWorld/Mods/3352894993
dotnet build ModName.sln -c Release
```

#### Opzione C — Senza compilare (M0 funziona anche senza DLL)
Per M0 la DLL C# è opzionale: contiene solo una `Log.Message()` di inizializzazione e la classe `MechExosuitExt` (ModExtension). Se non compili, RimWorld caricherà comunque la mod, ma il `MechExosuitExt` non sarà riconosciuto e il ThingDef potrebbe dare un warning in log.

**Raccomandazione**: per testare solo M0, puoi saltare la compilazione se sei disposto a vedere un warning in log. Per M1+ in poi la compilazione è obbligatoria.

### Step 4 — Attiva la mod in RimWorld

1. Avvia RimWorld
2. MainMenu → Mods → trova "[Mod Name]" → attivala
3. Verifica che le mod dipendenti siano attivate (Harmony, Exosuit Framework)
4. Carica una colonia esistente o iniziane una nuova

### Step 5 — Test in dev mode

1. Opzioni → Developer mode: ON
2. In gioco, apri il **menu dev** (icona bug in basso a destra)
3. Vai a **Spawn pawn** → cerca **Patriot Mech-Exosuit**
4. Clicca per spawnare il mech-exosuit

### Step 6 — Verifica

✅ **M0 è completo se**:
- Il mech-exosuit appare a schermo con la texture placeholder (rame scuro con freccia direzionale)
- Puoi selezionarlo cliccandoci sopra
- La scheda info (tab "Pawn" in basso) mostra il nome "EXO-45 Patriot Mech-Exosuit (M0 test)"
- Muovendosi, le 4 direzioni (north/south/east/west) si vedono correttamente
- Non ci sono errori rossi nel log di gioco

❌ **Se qualcosa fallisce**:
- **Mod non appare nel mod manager**: verifica che `About/About.xml` sia ben formato XML e che la cartella sia in `Mods/ModName/` (non annidata)
- **Warning "Cannot find texture path"**: verifica che le 4 PNG siano in `Common/Textures/Things/Pawn/MechExosuit_Patriot/`
- **Warning "MechExosuitExt not found"**: la DLL non è compilata o non è in `1.6/Assemblies/`
- **Error "Cannot find type ModName.MechExosuitExt"**: stesso motivo — devi compilare la DLL

## 🎯 Cosa NON fa M0

- ❌ Non ha il sistema di subcore pilot (arriva in M1)
- ❌ Non ha la batteria scarica (arriva in M4)
- ❌ Non ha la bay ibrida per costruirlo (arriva in M3)
- ❌ Non ha il drop del relitto su morte (arriva in M2)
- ❌ Non ha SubcoreInfo integration (arriva in M5)
- ❌ Non ha Combat Extended patches (arriva in M6)
- ❌ Il mech-exosuit attualmente usa il BodyDef vanilla `Mechanoid` (in M1 verrà sostituito con `ModName_MechExosuitBody` custom con subcore come body part interna)
- ❌ Il mech-exosuit attualmente si ricarica con i charger vanilla (in M4 verrà disattivato)

## 📝 Note di implementazione

### Perché la texture è così brutta
Le PNG in `Common/Textures/` sono **placeholder generati programmaticamente** (rami quadrati con frecce direzionali) per validare il setup. In M7 (Polish) verranno sostituite con texture custom proper, possibilmente riusando le texture originali della Patriot Exosuit (con autorizzazione dell'autore).

### Perché la DLL è opzionale in M0
La DLL contiene solo:
1. `ModNameMod` — static constructor che stampa un messaggio in log
2. `MechExosuitExt` — DefModExtension referenziata dal ThingDef XML

Senza la DLL, RimWorld carica comunque le Def XML ma logga un warning per il ModExtension mancante. Il mech-exosuit funziona comunque (usa comps vanilla).

### BodyDef vanilla `Mechanoid`
In M0 il ThingDef usa `<body>Mechanoid</body>` (vanilla) — questo significa che il mech-exosuit ha il body standard dei mechanoidi vanilla (Head, Torso, Arms, Legs, ecc.) ma **non ha il subcore come body part interna**. Questo arriverà in M1 quando introdurremo il `BodyDef` custom `ModName_MechExosuitBody`.

### Comps vanilla usati
- `CompProperties_OverseerSubject` — permette al mechanitor di assegnare il mech-exosuit a un control group (vanilla 1.6)
- `CompProperties_MechEnergy` — sistema energia vanilla (placeholder; sarà disattivato in M4)
- `CompProperties_Flickable` — per on/off (vanilla)

## 🐛 Problemi noti M0

Nessuno al momento. Se trovi un bug, apri una issue su GitHub:
https://github.com/endercrepper/mech-exosuit-framework/issues

## 📦 Prossimi step (M1)

Dopo aver validato M0, procediamo con M1 — Subcore Install:
1. Implementare `CompSubcorePilot.cs` ( tracking HP subcore, install/extract)
2. Definire `BodyDef` custom `ModName_MechExosuitBody` con subcore come body part interna (coverage 0.10)
3. Implementare Harmony patch `Patch_TakeDamage` per reindirizzare danno al subcore
4. Aggiungere `CompProperties_SubcorePilot` al ThingDef XML

Vedi Sezione 10.3 del design document per il dettaglio.
