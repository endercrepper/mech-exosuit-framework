"""Body PDF for [Mod Name] Design Document.
Generates 12 sections of the design document using ReportLab + TocDocTemplate.

Chapter numbering plan (per report.md Step 3.5):
| Outline Index | Type    | Chapter # | Title                                          |
|---------------|---------|-----------|------------------------------------------------|
| 1             | cover   | —         | (rendered separately via Playwright)          |
| 2             | toc     | —         | Indice                                         |
| 3             | content | 1         | Concept & Vision                              |
| 4             | content | 2         | Architettura Tecnica                          |
| 5             | content | 3         | Schema Defs XML                               |
| 6             | content | 4         | Sistema di Danno & Morte                      |
| 7             | content | 5         | Bay Ibrida & UI                               |
| 8             | content | 6         | Batteria & Bandwidth                          |
| 9             | content | 7         | Integrazione SubcoreInfo & CE                 |
| 10            | content | 8         | Bilanciamento — Caso Pilota Patriot           |
| 11            | content | 9         | Albero Tecnologico                            |
| 12            | content | 10        | Roadmap MVP                                   |
| 13            | content | 11        | Checklist Implementazione                     |
| 14            | content | 12        | Glossario                                     |
"""

import os
import sys
import hashlib
from pathlib import Path

# Add PDF skill scripts to path for install_font_fallback
PDF_SKILL_DIR = "/home/z/my-project/skills/pdf"
sys.path.insert(0, os.path.join(PDF_SKILL_DIR, "scripts"))
from pdf import install_font_fallback

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image,
    Table, TableStyle, KeepTogether, CondPageBreak, HRFlowable, ListFlowable, ListItem,
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from PIL import Image as PILImage

# ─── Font registration ─────────────────────────────────────────────────────
FONT_DIR = '/usr/share/fonts'
pdfmetrics.registerFont(TTFont('NotoSerifSC', f'{FONT_DIR}/truetype/noto-serif-sc/NotoSerifSC-Regular.ttf'))
pdfmetrics.registerFont(TTFont('NotoSerifSC-Bold', f'{FONT_DIR}/truetype/noto-serif-sc/NotoSerifSC-Bold.ttf'))
# NotoSansSC è variable font in questo sistema; usiamo NotoSerifSC come fallback CJK
# Sarasa Mono SC per code blocks
pdfmetrics.registerFont(TTFont('SarasaMonoSC', f'{FONT_DIR}/truetype/chinese/SarasaMonoSC-Regular.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif', f'{FONT_DIR}/truetype/freefont/FreeSerif.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-Bold', f'{FONT_DIR}/truetype/freefont/FreeSerifBold.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-Italic', f'{FONT_DIR}/truetype/freefont/FreeSerifItalic.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-BoldItalic', f'{FONT_DIR}/truetype/freefont/FreeSerifBoldItalic.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans', f'{FONT_DIR}/truetype/dejavu/DejaVuSansMono.ttf'))

# Aliases: 'Noto Sans SC' → 'NotoSerifSC' (per evitare variable font issues)
registerFontFamily('NotoSerifSC', normal='NotoSerifSC', bold='NotoSerifSC-Bold')
# Register 'Noto Sans SC' as alias of NotoSerifSC (since variable font is unreliable in ReportLab)
pdfmetrics.registerFont(TTFont('Noto Sans SC', f'{FONT_DIR}/truetype/noto-serif-sc/NotoSerifSC-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Noto Sans SC Bold', f'{FONT_DIR}/truetype/noto-serif-sc/NotoSerifSC-Bold.ttf'))
registerFontFamily('Noto Sans SC', normal='Noto Sans SC', bold='Noto Sans SC Bold')
registerFontFamily('FreeSerif', normal='FreeSerif', bold='FreeSerif-Bold',
                   italic='FreeSerif-Italic', boldItalic='FreeSerif-BoldItalic')
registerFontFamily('SarasaMonoSC', normal='SarasaMonoSC', bold='SarasaMonoSC')

install_font_fallback()

# ─── Palette (cascade output) ──────────────────────────────────────────────
PAGE_BG       = colors.HexColor('#f5f5f4')
SECTION_BG    = colors.HexColor('#f2f1f0')
CARD_BG       = colors.HexColor('#ebeae8')
TABLE_STRIPE  = colors.HexColor('#ededeb')
HEADER_FILL   = colors.HexColor('#4e4732')
COVER_BLOCK   = colors.HexColor('#746c56')
BORDER        = colors.HexColor('#c5bfac')
ICON          = colors.HexColor('#a48e4b')
ACCENT        = colors.HexColor('#92761f')
ACCENT_2      = colors.HexColor('#3aa0c2')
TEXT_PRIMARY  = colors.HexColor('#151513')
TEXT_MUTED    = colors.HexColor('#7e7c74')
SEM_SUCCESS   = colors.HexColor('#529067')
SEM_WARNING   = colors.HexColor('#8c7443')
SEM_ERROR     = colors.HexColor('#a25b54')
SEM_INFO      = colors.HexColor('#507aa4')

TABLE_HEADER_COLOR = HEADER_FILL
TABLE_HEADER_TEXT  = colors.white
TABLE_ROW_EVEN     = colors.white
TABLE_ROW_ODD      = TABLE_STRIPE

# ─── Layout constants ──────────────────────────────────────────────────────
LEFT_MARGIN   = 22 * mm
RIGHT_MARGIN  = 22 * mm
TOP_MARGIN    = 24 * mm
BOTTOM_MARGIN = 22 * mm
PAGE_W, PAGE_H = A4
AVAILABLE_W = PAGE_W - LEFT_MARGIN - RIGHT_MARGIN

# ─── Styles ────────────────────────────────────────────────────────────────
H1_STYLE = ParagraphStyle(
    'H1', fontName='NotoSerifSC-Bold', fontSize=20, leading=26,
    textColor=HEADER_FILL, alignment=TA_LEFT, spaceBefore=12, spaceAfter=6,
)
H1_KICKER = ParagraphStyle(
    'H1Kicker', fontName='NotoSerifSC', fontSize=9, leading=12,
    textColor=ACCENT, alignment=TA_LEFT, spaceBefore=0, spaceAfter=2,
)
H2_STYLE = ParagraphStyle(
    'H2', fontName='NotoSerifSC-Bold', fontSize=14, leading=20,
    textColor=HEADER_FILL, alignment=TA_LEFT, spaceBefore=14, spaceAfter=6,
)
H3_STYLE = ParagraphStyle(
    'H3', fontName='NotoSerifSC-Bold', fontSize=11.5, leading=16,
    textColor=ACCENT, alignment=TA_LEFT, spaceBefore=10, spaceAfter=4,
)
BODY_STYLE = ParagraphStyle(
    'Body', fontName='NotoSerifSC', fontSize=10.5, leading=17,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT, wordWrap='CJK',
    firstLineIndent=0, spaceBefore=0, spaceAfter=8,
)
BODY_LEAD = ParagraphStyle(
    'BodyLead', fontName='NotoSerifSC', fontSize=11, leading=18,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT, wordWrap='CJK',
    spaceBefore=0, spaceAfter=10,
)
BULLET_STYLE = ParagraphStyle(
    'Bullet', fontName='NotoSerifSC', fontSize=10.5, leading=16,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT, wordWrap='CJK',
    leftIndent=18, bulletIndent=4, spaceBefore=2, spaceAfter=2,
)
CAPTION_STYLE = ParagraphStyle(
    'Caption', fontName='NotoSerifSC', fontSize=9, leading=12,
    textColor=TEXT_MUTED, alignment=TA_CENTER, spaceBefore=4, spaceAfter=14,
)
CODE_STYLE = ParagraphStyle(
    'Code', fontName='SarasaMonoSC', fontSize=8.5, leading=12,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT, wordWrap='CJK',
    leftIndent=12, rightIndent=8, spaceBefore=4, spaceAfter=8,
)
TABLE_HDR_STYLE = ParagraphStyle(
    'TableHdr', fontName='NotoSerifSC-Bold', fontSize=10, leading=13,
    textColor=colors.white, alignment=TA_CENTER,
)
TABLE_CELL_STYLE = ParagraphStyle(
    'TableCell', fontName='NotoSerifSC', fontSize=9.5, leading=13,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT, wordWrap='CJK',
)
TABLE_CELL_CENTER = ParagraphStyle(
    'TableCellC', fontName='NotoSerifSC', fontSize=9.5, leading=13,
    textColor=TEXT_PRIMARY, alignment=TA_CENTER, wordWrap='CJK',
)
TOC_L0 = ParagraphStyle(
    'TOC0', fontName='NotoSerifSC-Bold', fontSize=11, leading=18,
    textColor=HEADER_FILL, leftIndent=0, spaceBefore=4, spaceAfter=2,
)
TOC_L1 = ParagraphStyle(
    'TOC1', fontName='NotoSerifSC', fontSize=10, leading=15,
    textColor=TEXT_PRIMARY, leftIndent=20, spaceBefore=2, spaceAfter=2,
)

# ─── TOC Document Template ─────────────────────────────────────────────────
class TocDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if hasattr(flowable, 'bookmark_name'):
            level = getattr(flowable, 'bookmark_level', 0)
            text = getattr(flowable, 'bookmark_text', '')
            key = getattr(flowable, 'bookmark_key', '')
            self.notify('TOCEntry', (level, text, self.page, key))

# ─── Helpers ───────────────────────────────────────────────────────────────
def heading(text, style, level=0, chapter_num=None):
    """Add a heading with bookmark for TOC."""
    display = text
    if chapter_num is not None:
        display = f"{chapter_num}. {text}"
    key = 'h_' + hashlib.md5(display.encode()).hexdigest()[:8]
    p = Paragraph(f'<a name="{key}"/>{display}', style)
    p.bookmark_name = key
    p.bookmark_level = level
    p.bookmark_text = display
    p.bookmark_key = key
    return p

def section_opener(kicker, title, chapter_num=None):
    """Build a H1 section opener: small kicker + accent rule + big title."""
    items = []
    if kicker:
        items.append(Paragraph(kicker.upper(), H1_KICKER))
        items.append(HRFlowable(width=40, thickness=2, color=ACCENT,
                                 spaceBefore=0, spaceAfter=6))
    items.append(heading(title, H1_STYLE, level=0, chapter_num=chapter_num))
    items.append(HRFlowable(width="100%", thickness=0.5, color=BORDER,
                             spaceBefore=0, spaceAfter=12))
    return items

def body(text, style=BODY_STYLE):
    return Paragraph(text, style)

def bullet_list(items, style=BULLET_STYLE):
    """Build a bullet list. Each item is a string."""
    return ListFlowable(
        [ListItem(Paragraph(it, style), leftIndent=18, value='•') for it in items],
        bulletType='bullet', start='•', leftIndent=18,
        bulletFontName='NotoSerifSC', bulletFontSize=10,
    )

def code_block(text):
    """Build a code block with light background and accent left border."""
    lines = text.strip('\n').split('\n')
    paragraphs = [Paragraph(line.replace(' ', ' ').replace('<', '<').replace('>', '>') or ' ', CODE_STYLE) for line in lines]
    t = Table([[p] for p in paragraphs], colWidths=[AVAILABLE_W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('LINEBEFORE', (0,0), (0,-1), 2, ACCENT),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    return t

def callout_box(title, text, color=ACCENT, bg=CARD_BG):
    """Build a callout box."""
    title_p = Paragraph(f'<b>{title}</b>',
                        ParagraphStyle('CalT', fontName='NotoSerifSC-Bold',
                                       fontSize=10.5, leading=14, textColor=color))
    body_p = Paragraph(text, ParagraphStyle('CalB', fontName='NotoSerifSC',
                                            fontSize=10, leading=14, textColor=TEXT_PRIMARY,
                                            wordWrap='CJK'))
    t = Table([[title_p], [body_p]], colWidths=[AVAILABLE_W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('LINEBEFORE', (0,0), (0,-1), 3, color),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    return t

def data_table(headers, rows, col_ratios=None, header_bg=None):
    """Build a styled table.
    headers: list of strings (header labels)
    rows: list of list of strings
    col_ratios: list of floats summing to 1.0
    """
    if col_ratios is None:
        col_ratios = [1.0 / len(headers)] * len(headers)
    col_widths = [r * AVAILABLE_W for r in col_ratios]
    
    # Build data with Paragraphs
    data = [[Paragraph(f'<b>{h}</b>', TABLE_HDR_STYLE) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(cell), TABLE_CELL_STYLE) for cell in row])
    
    t = Table(data, colWidths=col_widths, hAlign='CENTER', repeatRows=1)
    
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), header_bg or HEADER_FILL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.4, BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]
    # Alternating row colors
    for i in range(1, len(data)):
        bg = TABLE_ROW_EVEN if i % 2 == 1 else TABLE_ROW_ODD
        style_cmds.append(('BACKGROUND', (0, i), (-1, i), bg))
    
    t.setStyle(TableStyle(style_cmds))
    return t

def fit_image(path, max_width=None, max_height=None):
    """Embed image preserving aspect ratio."""
    if max_width is None:
        max_width = AVAILABLE_W
    if max_height is None:
        max_height = PAGE_H * 0.45
    
    pil_img = PILImage.open(path)
    orig_w, orig_h = pil_img.size
    
    ratio_w = max_width / orig_w if orig_w > max_width else 1.0
    ratio_h = max_height / orig_h if orig_h > max_height else 1.0
    ratio = min(ratio_w, ratio_h)
    
    return Image(path, width=orig_w * ratio, height=orig_h * ratio)

def caption(text):
    return Paragraph(f'<i>{text}</i>', CAPTION_STYLE)

# ─── Header / footer ───────────────────────────────────────────────────────
def header_footer(canvas, doc):
    canvas.saveState()
    # Header
    canvas.setFont('NotoSerifSC', 8)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawString(LEFT_MARGIN, PAGE_H - 14*mm, '[Mod Name] — Design Document')
    canvas.drawRightString(PAGE_W - RIGHT_MARGIN, PAGE_H - 14*mm, 'Mech-Exosuit Framework')
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(0.8)
    canvas.line(LEFT_MARGIN, PAGE_H - 16*mm, PAGE_W - RIGHT_MARGIN, PAGE_H - 16*mm)
    
    # Footer
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.4)
    canvas.line(LEFT_MARGIN, 14*mm, PAGE_W - RIGHT_MARGIN, 14*mm)
    canvas.setFont('NotoSerifSC', 8)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawString(LEFT_MARGIN, 9*mm, 'v0.1 Draft · 30 Giugno 2026')
    canvas.drawRightString(PAGE_W - RIGHT_MARGIN, 9*mm, f'Pagina {doc.page}')
    canvas.restoreState()

# ─── Build story ───────────────────────────────────────────────────────────
from content_sections import build_all_sections

def main():
    output_path = '/home/z/my-project/scripts/body.pdf'
    
    doc = TocDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=LEFT_MARGIN, rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN, bottomMargin=BOTTOM_MARGIN,
        title='[Mod Name] Design Document',
        author='Z.ai',
        creator='Z.ai',
        subject='Mech-Exosuit Framework Design Document for RimWorld 1.6',
    )
    
    # Build TOC
    toc = TableOfContents()
    toc.levelStyles = [TOC_L0, TOC_L1]
    
    story = []
    # TOC page
    story.append(Paragraph('<b>Indice</b>',
                           ParagraphStyle('TOCTitle', fontName='NotoSerifSC-Bold',
                                          fontSize=22, leading=28, textColor=HEADER_FILL,
                                          spaceBefore=0, spaceAfter=12)))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT, spaceAfter=18))
    story.append(toc)
    story.append(PageBreak())
    
    # Build content sections
    ctx = {
        'heading': heading,
        'section_opener': section_opener,
        'body': body,
        'bullet_list': bullet_list,
        'code_block': code_block,
        'callout_box': callout_box,
        'data_table': data_table,
        'fit_image': fit_image,
        'caption': caption,
        'KeepTogether': KeepTogether,
        'CondPageBreak': CondPageBreak,
        'Spacer': Spacer,
        'PageBreak': PageBreak,
        'Paragraph': Paragraph,
        'HRFlowable': HRFlowable,
        'styles': {
            'H1': H1_STYLE, 'H2': H2_STYLE, 'H3': H3_STYLE,
            'Body': BODY_STYLE, 'BodyLead': BODY_LEAD, 'Bullet': BULLET_STYLE,
            'Caption': CAPTION_STYLE, 'Code': CODE_STYLE,
        },
        'colors': {
            'accent': ACCENT, 'accent2': ACCENT_2, 'header_fill': HEADER_FILL,
            'text_primary': TEXT_PRIMARY, 'text_muted': TEXT_MUTED,
            'border': BORDER, 'card_bg': CARD_BG,
            'success': SEM_SUCCESS, 'warning': SEM_WARNING, 'error': SEM_ERROR, 'info': SEM_INFO,
        },
        'available_w': AVAILABLE_W,
        'diagrams_dir': '/home/z/my-project/diagrams',
    }
    
    story = build_all_sections(story, ctx)
    
    # Build PDF
    doc.multiBuild(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"Body PDF generated: {output_path}")
    print(f"Size: {os.path.getsize(output_path) / 1024:.1f} KB")

if __name__ == '__main__':
    main()
