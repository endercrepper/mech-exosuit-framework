# [Mod Name] — Mech-Exosuit Framework

> **Status:** Design phase (v0.1 Draft)
> **Target:** RimWorld 1.6
> **Author:** endercrepper

Una mod per RimWorld 1.6 che introduce **exosuit meccanoid-guidate**: entità ibride che combinano l'estetica e l'autonomia operativa dei mechanoidi vanilla con la modularità e la configurabilità dell'[Exosuit Framework](https://steamcommunity.com/sharedfiles/filedetails/?id=3352894993) di Aoba.

Il cuore del concept: invece di un pawn umano a bordo dell'exosuit, il pilota è un **subcore vanilla** (Standard o High) installato fisicamente come body part interna, con health pool separato dal mech.

## 📖 Documentazione

- **[Design Document v0.1 (PDF)](design_doc/ModName_Design_Document.pdf)** — 70 pagine: concept, architettura C#, schema XML, sistema di danno/morte, bay ibrida, bilanciamento (caso pilota Patriot), roadmap MVP, glossario
- **[Diagrammi](diagrams/)** — sorgenti HTML + PNG renderizzati (architettura classi, flow danno, flow morte, schema bay)

## 🎯 Concept in breve

| Aspetto | Decisione |
|---|---|
| Pilota interno | Subcore Standard/High vanilla (HP 100/175) |
| Danno al pilota | Health pool separato, coverage 10% (colpi penetranti) |
| Morte subcore | Deterministica — HP=0 → Destroyed Subcore |
| Morte mech | Drop Relitto Sigillato → smontaggio → esito deterministico su HP residui |
| Batteria | Scarsa (~12h gioco), ricarica solo nella bay ibrida |
| Bandwidth | Come mech vanilla (consuma control group del mechanitor) |
| Sblocco tech | Standard Mechtech prerequisito |
| Skill | Suit base + bonus subcore (Standard +0, High +4) |
| Estrazione | Comando floating menu — subcore + frame separati |
| SubcoreInfo | Soft dependency via reflection bridge |

## 🏗️ Roadmap MVP

| ID | Nome | Stima ore | Dipendenze |
|---|---|---|---|
| M0 | Hello World Mech | 8-12 | — |
| M1 | Subcore Install | 12-18 | M0 |
| M2 | Death & Relic | 16-24 | M1 |
| M3 | Bay Ibrida | 20-30 | M2 |
| M4 | Batteria & Bandwidth | 10-15 | M3 |
| M5 | SubcoreInfo Integration | 6-10 | M3 |
| M6 | CE Compat | 8-12 | M3 |
| M7 | Polish & Bilanciamento | 20-40 | M4, M5, M6 |

Stima totale: 100-161 ore (~3-4 settimane full-time). Dettagli nel [design document](design_doc/ModName_Design_Document.pdf), Sezione 10.

## 📁 Struttura del repository

```
mech-exosuit-framework/
├── README.md                          # questo file
├── LICENSE                            # MIT (vedi sotto)
├── .gitignore
├── design_doc/
│   ├── ModName_Design_Document.pdf    # deliverable principale
│   └── README.md                      # come rigenerare il PDF
├── diagrams/                          # 4 diagrammi (HTML sorgente + PNG)
│   ├── architecture_class_diagram.*
│   ├── damage_flow.*
│   ├── death_flow.*
│   └── bay_schema.*
├── scripts/                           # script Python per rigenerare PDF
│   ├── build_body.py                  # corpo del PDF (ReportLab)
│   ├── content_sections.py            # dispatcher sezioni
│   ├── cover.html                     # cover HTML (Playwright)
│   ├── merge_pdf.py                   # merge cover + body
│   ├── generate_diagrams.py           # genera diagrammi PNG
│   └── sections/                      # 12 sezioni del documento
│       ├── s01_concept.py
│       ├── s02_architecture.py
│       ├── ...
│       └── s12_glossary.py
└── docs/
    └── reference_mods/                # mod di riferimento analizzate
        ├── exosuit_framework/         # Aoba.Exosuit.Framework
        ├── helldivers_patriot/        # Aqued.Exosuits (caso pilota)
        └── subcoreinfo/               # eth0net.SubcoreInfo
```

## 🔧 Rigenerare il design document

Il PDF è generato programmaticamente. Per rigenerarlo dopo modifiche:

```bash
# Prerequisiti
pip install reportlab pypdf pillow playwright
playwright install chromium

# 1. Rigenera i diagrammi (richiede Playwright)
python3 scripts/generate_diagrams.py

# 2. Rigenera il body PDF (richiede i font Noto Serif SC + Sarasa Mono)
python3 scripts/build_body.py

# 3. Renderizza la cover (richiede Node.js + Playwright)
node $(which html2poster.js) scripts/cover.html --output scripts/cover.pdf --width 794px
# (oppure usa lo script del skill PDF locale)

# 4. Merge cover + body
python3 scripts/merge_pdf.py

# Output finale: download/ModName_Design_Document.pdf
```

Font richiesti (Linux):
- `/usr/share/fonts/truetype/noto-serif-sc/NotoSerifSC-Regular.ttf`
- `/usr/share/fonts/truetype/noto-serif-sc/NotoSerifSC-Bold.ttf`
- `/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf`
- `/usr/share/fonts/truetype/freefont/FreeSerif*.ttf`

## 📦 Mod di riferimento

Le mod analizzate come riferimento per il design sono in `docs/reference_mods/`:

| Mod | packageId | Ruolo nel progetto |
|---|---|---|
| Exosuit Framework | `aoba.exosuit.framework` | Hard dependency — fornisce SlotDef, Building_MaintenanceBay, ITab_Exosuit |
| Helldivers Patriot Exosuit | `Aqued.Exosuits` | Caso pilota per la mech-ificazione |
| SubcoreInfo | `eth0net.SubcoreInfo` | Soft dependency — preserva identità pawn scansionato |

> ⚠️ I file in `docs/reference_mods/` sono di proprietà dei rispettivi autori e sono inclusi qui solo per riferimento di sviluppo. Non distribuire.

## 🤝 Compatibilità

| Mod | Tipo | Stato |
|---|---|---|
| Exosuit Framework | Hard dep | ✅ Integrazione confermata |
| Harmony | Hard dep | ✅ Patch standard |
| Vanilla Mechtech (Ludeon) | Hard dep | ✅ SubcoreRegular, SubcoreHigh, BaseMechanoid |
| SubcoreInfo | Soft dep | ✅ Bridge via reflection |
| Combat Extended | Soft dep | ✅ Patch CE dedicata |
| TheDeadmanswitch Mech Chargers | Compat passiva | ✅ Mech-exosuit esclusi |
| Vanilla Expanded Framework | Soft (via EF) | ✅ Eredita da EF |
| HugsLib | Opzionale | ✅ Nessun conflitto |
| Rocketman | Opzionale | ✅ Compatibile |

## 📝 Licensing

- **Codice sorgente della mod** (ancora da scrivere): MIT License — vedi [LICENSE](LICENSE)
- **Design document e script di generazione**: MIT License
- **Mod di riferimento in `docs/reference_mods/`**: proprietà dei rispettivi autori, non MIT

## 🚧 Stato del progetto

- [x] Concept & vision
- [x] Design document v0.1
- [x] Analisi mod di riferimento
- [x] Architettura C# (su carta)
- [x] Schema Defs XML (su carta)
- [x] Bilanciamento caso pilota Patriot
- [x] Roadmap MVP
- [ ] Implementazione M0 — Hello World Mech
- [ ] Implementazione M1 — Subcore Install
- [ ] Implementazione M2 — Death & Relic
- [ ] Implementazione M3 — Bay Ibrida
- [ ] Implementazione M4-M7
- [ ] Aggiunta altre suit (AMP, Mobile Dragon, ...)
- [ ] Pubblicazione Steam Workshop v1.0

## ⚠️ Note

- `[Mod Name]` è un placeholder — il nome definitivo sarà scelto prima della pubblicazione
- I valori di bilanciamento nella Sezione 8 del design doc sono **valori di partenza**, pronti per essere tweakati durante il playtesting
- Il design document è in italiano (lingua di sviluppo); lo Steam Workshop page sarà localizzato in IT/EN

---

**Disclaimer:** Questo progetto non è affiliato con Ludeon Studios, Aoba, Aqued, eth0net, o il team di Combat Extended. RimWorld è un marchio di Ludeon Studios.
