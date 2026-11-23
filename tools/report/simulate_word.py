from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pymupdf
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch

import build_pdf
import content

POST = "/tmp/word_simulation.pdf"


def main() -> None:
    build_pdf.STYLES["body"] = ParagraphStyle(
        "body_sim", fontName="Times-Roman", fontSize=12, leading=15.87,
        alignment=4, spaceAfter=5)
    build_pdf.STYLES["ref"] = ParagraphStyle(
        "ref_sim", fontName="Times-Roman", fontSize=11, leading=14.5,
        leftIndent=32, firstLineIndent=-32, spaceAfter=1)
    doc = build_pdf.BaseDocTemplate(
        POST, pagesize=build_pdf.A4, leftMargin=inch, rightMargin=inch,
        topMargin=inch, bottomMargin=inch)
    frame = build_pdf.Frame(inch, inch, build_pdf.FRAME_W,
                            build_pdf.PAGE_H - 2 * inch, id="b",
                            leftPadding=0, rightPadding=0, topPadding=0,
                            bottomPadding=0)
    gutter = 14
    col_w = (build_pdf.FRAME_W - gutter) / 2.0
    col_h = build_pdf.PAGE_H - 2 * inch
    left = build_pdf.Frame(inch, inch, col_w, col_h, id="col1",
                           leftPadding=0, rightPadding=0, topPadding=0,
                           bottomPadding=0)
    right = build_pdf.Frame(inch + col_w + gutter, inch, col_w, col_h, id="col2",
                            leftPadding=0, rightPadding=0, topPadding=0,
                            bottomPadding=0)
    doc.addPageTemplates([build_pdf.PageTemplate(id="all", frames=[frame]),
                          build_pdf.PageTemplate(id="two",
                                                 frames=[left, right])])
    doc.build(build_pdf.render(content.build_blocks()))

    pdf = pymupdf.open(POST)
    appendix = next((i + 1 for i, page in enumerate(pdf)
                     if "Appendix A:" in page.get_text()), None)
    print(f"total pages {len(pdf)}, appendix starts on page {appendix}, "
          f"body pages {appendix - 2} (limit 15)")


if __name__ == "__main__":
    main()
