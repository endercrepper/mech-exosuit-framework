"""Section 9: Albero Tecnologico"""

from reportlab.platypus import Spacer, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER


def build_section_09(story, ctx):
    h = ctx['heading']; so = ctx['section_opener']
    body = ctx['body']; bl = ctx['bullet_list']; cb = ctx['callout_box']
    dt = ctx['data_table']; cap = ctx['caption']
    P = ctx['Paragraph']; HR = ctx['HRFlowable']; KT = ctx['KeepTogether']
    
    story.extend(so('Capitolo 09 · Tech Tree', 'Albero Tecnologico',
                    chapter_num=9))
    
    story.append(body(
        "L'albero tecnologico di [Mod Name] è costruito <b>sopra</b> "
        "Standard Mechtech vanilla: il giocatore deve prima sbloccare "
        "Standard Mechtech (che dà accesso ai subcore Standard e al "
        "mechanitor), e solo dopo può ricercare i nodi nostri. Questo "
        "posizionamento è coerente con il design vanilla di mechtech "
        "come prerequisito per qualsiasi estensione mech."
    , ctx['styles']['BodyLead']))
    
    # ── 9.1 Tree visualization ──
    story.append(P('<b>9.1 — Visualizzazione dell\'albero</b>',
                   ctx['styles']['H2']))
    
    # Tree as a styled table (ReportLab non supporta span/style inline)
    from reportlab.platypus import Table, TableStyle
    from reportlab.lib import colors
    
    tree_node_style = ParagraphStyle('TreeNode', fontName='NotoSerifSC-Bold',
                                      fontSize=9, leading=12, textColor=colors.white,
                                      alignment=TA_CENTER)
    tree_label_style = ParagraphStyle('TreeLabel', fontName='NotoSerifSC',
                                       fontSize=8, leading=10, textColor=ctx['colors']['text_muted'],
                                       alignment=TA_CENTER)
    tree_arrow_style = ParagraphStyle('TreeArrow', fontName='NotoSerifSC',
                                       fontSize=10, leading=12, textColor=ctx['colors']['text_muted'],
                                       alignment=TA_CENTER)
    
    HEADER_FILL = ctx['colors']['header_fill']
    ACCENT = ctx['colors']['accent']
    ACCENT_LIGHT = colors.HexColor('#c89669')
    CARD_BG = ctx['colors']['card_bg']
    BORDER = ctx['colors']['border']
    
    # Row 1: Standard Mechtech → ModName_HybridMechtech
    row1 = [
        Paragraph('<b>Standard Mechtech</b><br/><font size="7">(vanilla)</font>', tree_node_style),
        Paragraph('→ prerequisite →', tree_arrow_style),
        Paragraph('<b>ModName_HybridMechtech</b><br/><font size="7">(base mod)</font>', tree_node_style),
        '', '',
    ]
    # Row 2: three intermediate nodes
    row2 = [
        '', '',
        Paragraph('<b>ModName_SubcoreFrameIntegration</b><br/><font size="7">4000 research<br/>+ Subcore HP boost</font>',
                  ParagraphStyle('TreeNode2', fontName='NotoSerifSC-Bold', fontSize=9, leading=11,
                                 textColor=ctx['colors']['text_primary'], alignment=TA_CENTER)),
        Paragraph('<b>ModName_AdvancedMechExosuit</b><br/><font size="7">6000 research<br/>+ Subcore High support</font>',
                  ParagraphStyle('TreeNode2', fontName='NotoSerifSC-Bold', fontSize=9, leading=11,
                                 textColor=ctx['colors']['text_primary'], alignment=TA_CENTER)),
        Paragraph('<b>ModName_BatteryOptimization</b><br/><font size="7">3000 research<br/>+50% battery life</font>',
                  ParagraphStyle('TreeNode2', fontName='NotoSerifSC-Bold', fontSize=9, leading=11,
                                 textColor=ctx['colors']['text_primary'], alignment=TA_CENTER)),
    ]
    # Row 3: arrow down
    row3 = ['', '', Paragraph('↓ tutti e tre ↓', tree_arrow_style), '', '']
    # Row 4: final node
    row4 = [
        '', '',
        Paragraph('<b>ModName_MasterMechExosuit</b><br/><font size="7">10000 research<br/>Sblocca: riparazione subcore + frame custom</font>',
                  tree_node_style),
        '', '',
    ]
    
    tree_data = [row1, row2, row3, row4]
    col_w = ctx['available_w'] / 5
    tree_table = Table(tree_data, colWidths=[col_w]*5, hAlign='CENTER')
    tree_table.setStyle(TableStyle([
        # Row 1: header style (dark)
        ('BACKGROUND', (0, 0), (0, 0), HEADER_FILL),
        ('BACKGROUND', (2, 0), (2, 0), ACCENT),
        ('SPAN', (0, 0), (0, 0)),
        # Row 2: intermediate (rame light)
        ('BACKGROUND', (2, 1), (2, 1), ACCENT_LIGHT),
        ('BACKGROUND', (3, 1), (3, 1), ACCENT_LIGHT),
        ('BACKGROUND', (4, 1), (4, 1), ACCENT_LIGHT),
        # Row 4: final (dark)
        ('BACKGROUND', (2, 3), (2, 3), HEADER_FILL),
        ('SPAN', (2, 3), (4, 3)),
        # Common
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0, colors.white),
        ('BACKGROUND', (0, 1), (1, 1), colors.white),
        ('BACKGROUND', (0, 2), (1, 2), colors.white),
        ('BACKGROUND', (0, 3), (1, 3), colors.white),
        ('BACKGROUND', (3, 2), (4, 2), colors.white),
        ('BACKGROUND', (3, 3), (4, 3), colors.white),
    ]))
    story.append(tree_table)
    story.append(cap('Figura 9.1 — Albero tecnologico di [Mod Name]. '
                      'Standard Mechtech (vanilla) è prerequisito diretto di HybridMechtech. '
                      'I 3 nodi intermedi sono prerequisiti del nodo finale Master.'))
    
    # ── 9.2 Research nodes ──
    story.append(P('<b>9.2 — Nodi di ricerca</b>', ctx['styles']['H2']))
    
    headers = ['Nodo', 'Costo (research)', 'Prerequisiti', 'Sblocca']
    rows = [
        ['ModName_HybridMechtech', '4.000',
         'Standard Mechtech (vanilla)',
         'Building_HybridGestator + Patriot Mech-Exosuit (con Subcore Standard)'],
        ['ModName_SubcoreFrameIntegration', '4.000',
         'ModName_HybridMechtech',
         'Subcore HP +25% (Standard 125, High 220); sblocca riparazione subcore'],
        ['ModName_AdvancedMechExosuit', '6.000',
         'ModName_HybridMechtech',
         'Subcore High utilizzabile; +1 slot di loadout per tutte le suit'],
        ['ModName_BatteryOptimization', '3.000',
         'ModName_HybridMechtech',
         'Battery capacity ×1.5 (Standard 18h, High 27h)'],
        ['ModName_MasterMechExosuit', '10.000',
         'Tutti e 3 i nodi intermedi',
         'Riparazione subcore senza perdita di maxHP; frame custom (scout, constructor)'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.28, 0.15, 0.22, 0.35]))
    story.append(cap('Tabella 9.1 — Nodi di ricerca di [Mod Name]. '
                      'Costo totale: 27.000 research points (~5-7 ore gioco per completare).'))
    
    # ── 9.3 Techprints ──
    story.append(P('<b>9.3 — Techprints</b>', ctx['styles']['H2']))
    
    story.append(body(
        "Per coerenza con il design vanilla di mechtech (che usa techprints "
        "per i nodi principali), anche i nodi di [Mod Name] richiedono "
        "<b>techprints</b>. I techprint sono item che riducono il costo "
        "di ricerca del 50% e sono fondamentali per rendere i nodi "
        "raggiungibili in tempo ragionevole."
    ))
    
    headers = ['Nodo', 'Techprints richiesti', 'Fonte techprint']
    rows = [
        ['ModName_HybridMechtech', '2',
         'Quest: "Mech-Exosuit Prototype" (rare quest reward)'],
        ['ModName_SubcoreFrameIntegration', '1',
         'Trade: outlander towns (rare)'],
        ['ModName_AdvancedMechExosuit', '2',
         'Quest: "Subcore High Recovery" (rare quest reward)'],
        ['ModName_BatteryOptimization', '1',
         'Trade: outlander towns (uncommon)'],
        ['ModName_MasterMechExosuit', '3',
         'Quest: "Ancient Mech Lab" (very rare, late game)'],
    ]
    story.append(dt(headers, rows, col_ratios=[0.35, 0.20, 0.45]))
    story.append(cap('Tabella 9.2 — Techprints per nodo. I techprint sono item '
                      'che dimezzano il costo di ricerca e sono ricercabili solo quando posseduti.'))
    
    # ── 9.4 Positioning in vanilla tree ──
    story.append(P('<b>9.4 — Posizionamento nell\'albero vanilla</b>',
                   ctx['styles']['H2']))
    
    story.append(body(
        "I nodi di [Mod Name] si posizionano nel ramo <b>Mechtech</b> "
        "dell'albero vanilla, tra Standard Mechtech e High Mechtech. "
        "Il nodo finale (Master MechExosuit) è approssimativamente allo "
        "stesso livello di High Mechtech vanilla, rendendo il percorso "
        "di ricerca alternativo ma non sostitutivo: il giocatore che "
        "vuole usare mech-exosuit investe in [Mod Name], mentre il "
        "giocatore che preferisce mech vanilla investe in High Mechtech. "
        "Entrambi i percorsi possono essere percorsi in parallelo."
    ))
    
    story.append(Spacer(1, 18))
