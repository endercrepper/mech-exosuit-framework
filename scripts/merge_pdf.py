"""Merge cover PDF + body PDF into final output, with metadata."""

import os
import sys
from pypdf import PdfReader, PdfWriter

A4_W, A4_H = 595.28, 841.89

def normalize_page_to_a4(page):
    """Scale a page to A4 exactly (tolerance <0.5pt)."""
    box = page.mediabox
    w, h = float(box.width), float(box.height)
    if abs(w - A4_W) > 0.5 or abs(h - A4_H) > 0.5:
        page.scale_to(A4_W, A4_H)
    return page

def main():
    cover_pdf = '/home/z/my-project/scripts/cover.pdf'
    body_pdf = '/home/z/my-project/scripts/body.pdf'
    output_pdf = '/home/z/my-project/download/ModName_Design_Document.pdf'
    
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    
    writer = PdfWriter()
    
    # Cover as page 1
    cover_page = PdfReader(cover_pdf).pages[0]
    writer.add_page(normalize_page_to_a4(cover_page))
    
    # Body pages follow
    for page in PdfReader(body_pdf).pages:
        writer.add_page(normalize_page_to_a4(page))
    
    # Metadata
    writer.add_metadata({
        '/Title': '[Mod Name] Design Document',
        '/Author': 'Z.ai',
        '/Creator': 'Z.ai',
        '/Subject': 'Mech-Exosuit Framework Design Document for RimWorld 1.6',
        '/Keywords': 'RimWorld, mod, exosuit, mechanoid, subcore, design document',
    })
    
    with open(output_pdf, 'wb') as f:
        writer.write(f)
    
    size_kb = os.path.getsize(output_pdf) / 1024
    page_count = len(PdfReader(output_pdf).pages)
    print(f"Final PDF: {output_pdf}")
    print(f"Size: {size_kb:.1f} KB ({size_kb/1024:.2f} MB)")
    print(f"Pages: {page_count}")

if __name__ == '__main__':
    main()
