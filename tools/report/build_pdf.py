"""Build a PDF copy of the report from the same block list as the .docx."""

from __future__ import annotations

import os
import re
import sys

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, Image,
                                KeepTogether, NextPageTemplate, PageBreak,
                                PageTemplate, Paragraph, Preformatted, Spacer,
                                Table, TableStyle)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import content  # noqa: E402

OUT = os.path.join(content.ROOT, "docs", "submission")

PAGE_W, PAGE_H = A4
MARGIN = 1 * inch
FRAME_W = PAGE_W - 2 * MARGIN

INK = colors.HexColor("#000000")
MUTED = colors.HexColor("#404040")
CAPTION = colors.HexColor("#333333")
RULE = colors.HexColor("#BFBFBF")
HDR = colors.HexColor("#DCE6F1")
CODE_BG = colors.HexColor("#F5F5F5")

TOKEN = re.compile(r"(<b>.*?</b>|<i>.*?</i>)", re.S)


def esc(text: str) -> str:
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def rich(text: str) -> str:
    """Escape XML but keep the report's own <b> and <i> tags."""
    out = []
    for piece in TOKEN.split(text):
        if not piece:
            continue
        if piece.startswith("<b>") and piece.endswith("</b>"):
            out.append("<b>" + esc(piece[3:-4]) + "</b>")
        elif piece.startswith("<i>") and piece.endswith("</i>"):
            out.append("<i>" + esc(piece[3:-4]) + "</i>")
        else:
            out.append(esc(piece))
    return "".join(out)


STYLES = {
    "body": ParagraphStyle("body", fontName="Times-Roman", fontSize=12,
                           leading=13.8, alignment=TA_JUSTIFY, spaceAfter=5,
                           textColor=INK),
    "h1": ParagraphStyle("h1", fontName="Times-Bold", fontSize=14, leading=16.8,
                         spaceBefore=12, spaceAfter=6, textColor=INK,
                         keepWithNext=1),
    "h2": ParagraphStyle("h2", fontName="Times-Bold", fontSize=12, leading=14.4,
                         spaceBefore=10, spaceAfter=4, textColor=INK,
                         keepWithNext=1),
    "caption": ParagraphStyle("caption", fontName="Times-Italic", fontSize=10,
                              leading=12, alignment=TA_CENTER, spaceBefore=3,
                              spaceAfter=10, textColor=CAPTION),
    "capabove": ParagraphStyle("capabove", fontName="Times-Italic", fontSize=10,
                               leading=12, alignment=TA_CENTER, spaceBefore=8,
                               spaceAfter=3, textColor=CAPTION),
    "cell": ParagraphStyle("cell", fontName="Times-Roman", fontSize=9,
                           leading=10.8, textColor=INK),
    "cellhead": ParagraphStyle("cellhead", fontName="Times-Bold", fontSize=9,
                               leading=10.8, textColor=INK),
    "code": ParagraphStyle("code", fontName="Courier", fontSize=8, leading=9.6,
                           textColor=INK, backColor=CODE_BG, spaceBefore=0,
                           spaceAfter=0, leftIndent=4, borderPadding=2),
    "ref": ParagraphStyle("ref", fontName="Times-Roman", fontSize=10.2, leading=11.8,
                          leftIndent=32, firstLineIndent=-32, spaceAfter=1,
                          alignment=TA_LEFT, textColor=INK),
    "cover_big": ParagraphStyle("cover_big", fontName="Times-Bold", fontSize=16,
                                leading=19, alignment=TA_CENTER, spaceAfter=3),
    "cover_mid": ParagraphStyle("cover_mid", fontName="Times-Roman", fontSize=12,
                                leading=14.5, alignment=TA_CENTER, spaceAfter=2),
    "cover_title": ParagraphStyle("cover_title", fontName="Times-Bold",
                                  fontSize=18, leading=22, alignment=TA_CENTER,
                                  spaceBefore=14, spaceAfter=10),
    "cover_cell": ParagraphStyle("cover_cell", fontName="Times-Roman", fontSize=11,
                                 leading=13.5, textColor=INK),
    "cover_head": ParagraphStyle("cover_head", fontName="Times-Bold", fontSize=11,
                                 leading=13.5, textColor=INK),
}


def header_footer(canvas, doc) -> None:
    canvas.saveState()
    if doc.page > 1:
        canvas.setFont("Times-Roman", 9)
        canvas.setFillColor(MUTED)
        canvas.drawString(MARGIN, PAGE_H - MARGIN + 22,
                          "EL-2003 COAL Lab  |  Fall 2026  |  Final Project Report")
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN, PAGE_H - MARGIN + 17,
                    PAGE_W - MARGIN, PAGE_H - MARGIN + 17)
        canvas.setFont("Times-Roman", 9)
        canvas.drawCentredString(PAGE_W / 2, MARGIN - 32, f"Page {doc.page}")
    canvas.restoreState()


def code_flowable(text: str, size=8.0) -> Preformatted:
    """Preformatted keeps the layout exactly and does not parse XML tags, which
    is what source code needs (<, > and & must stay literal)."""
    style = ParagraphStyle("code%d" % int(size * 10), parent=STYLES["code"],
                           fontSize=size, leading=size * 1.2)
    return Preformatted(text, style)


class CaptionedTable(Flowable):
    """A table caption and its table that never get separated.

    When the pair does not fit, the table is split by rows and the caption
    travels with the first part; if even the header would not fit, the whole
    block moves to the next page.
    """

    def __init__(self, caption, table):
        Flowable.__init__(self)
        self.caption = caption
        self.table = table
        self._width = 0
        self._height = 0

    def wrap(self, availWidth, availHeight):
        w1, h1 = self.caption.wrap(availWidth, availHeight)
        w2, h2 = self.table.wrap(availWidth, availHeight)
        self._width = max(w1, w2)
        self._height = h1 + h2
        self._cap_h = h1
        return self._width, self._height

    def split(self, availWidth, availHeight):
        if availHeight >= self._height:
            return [self]
        room = availHeight - self._cap_h
        if room < 3 * 12:                      # caption and almost nothing else
            return []
        parts = self.table.split(availWidth, room)
        rows = getattr(parts[0], "_cellvalues", None) if parts else None
        if not parts or rows is None or len(rows) < 3:   # header + 2 rows
            return []                          # let the block start a new page
        # hand the caption and the whole table back to the frame; the table
        # splits itself with one repeated header row
        return [self.caption, self.table]

    def draw(self):
        table_w = getattr(self.table, "_width", self._width)
        self.table.drawOn(self.canv, (self._width - table_w) / 2.0, 0)
        self.caption.drawOn(self.canv, 0, self._height - self._cap_h)

    def getSpaceBefore(self):
        return 8


def table_flowable(spec: dict) -> list:
    font = spec.get("font", 9.0)
    body = ParagraphStyle("t", parent=STYLES["cell"], fontSize=font,
                          leading=font * 1.2)
    head = ParagraphStyle("th", parent=STYLES["cellhead"], fontSize=font,
                          leading=font * 1.2)
    data = [[Paragraph(rich(c), head) for c in spec["cols"]]]
    for row in spec["rows"]:
        data.append([Paragraph(rich(c), body) for c in row])
    widths = [w * inch for w in spec["widths"]]
    total = sum(widths)
    if total > FRAME_W:
        widths = [w * FRAME_W / total for w in widths]
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="CENTER")
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#7F7F7F")),
        ("BACKGROUND", (0, 0), (-1, 0), HDR),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 1.8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8),
    ]))
    caption = Paragraph(rich(spec["caption"]), STYLES["capabove"])
    return [CaptionedTable(caption, table), Spacer(1, 8)]


def figure_flowable(spec: dict) -> KeepTogether:
    path = os.path.join(content.ASSETS, spec["path"])
    with PILImage.open(path) as im:
        w, h = im.size
    width = spec.get("width", 6.0) * inch
    height = width * h / w
    max_h = PAGE_H - 2 * MARGIN - 90
    if height > max_h:
        height = max_h
        width = height * w / h
    return KeepTogether([
        Spacer(1, 6),
        Image(path, width=width, height=height),
        Paragraph(rich(spec["caption"]), STYLES["caption"]),
    ])


def cover_flowables() -> list:
    flow = [Spacer(1, 46)]
    logo = os.path.join(content.ASSETS, "fast_nu_logo.png")
    if os.path.exists(logo):
        with PILImage.open(logo) as im:
            w, h = im.size
        width = 3.1 * inch
        flow.append(Image(logo, width=width, height=width * h / w))
        flow.append(Spacer(1, 10))
    flow += [
        Paragraph("National University of Computer and Emerging Sciences",
                  STYLES["cover_big"]),
        Paragraph("Karachi Campus", ParagraphStyle("cc", parent=STYLES["cover_mid"],
                                                   fontName="Times-Bold",
                                                   fontSize=13)),
        Spacer(1, 12),
        Paragraph("EL-2003&nbsp; Computer Organization and Assembly Language "
                  "(COAL) Lab", STYLES["cover_mid"]),
        Paragraph("Fall 2026", STYLES["cover_mid"]),
        Paragraph("FINAL PROJECT REPORT", STYLES["cover_title"]),
        Spacer(1, 10),
    ]
    rows = [
        ("Project Title", content.TITLE),
        ("Student IDs", content.STUDENT_IDS),
        ("Group Leader (Name & Roll No.)", "Muhammad Anas  \u2013  25K-0899"),
        ("Member 2 (Name & Roll No.)", "Syed Alyan Hussain  \u2013  25K-0648"),
        ("Member 3 (Name & Roll No.)", "Ali Raza  \u2013  25K-0827"),
        ("Lab Section", content.SECTION),
        ("Lab Instructor", content.INSTRUCTOR),
        ("Submission Date", content.SUBMIT_DATE),
    ]
    data = [[Paragraph(lbl, STYLES["cover_head"]),
             Paragraph(rich(val), STYLES["cover_cell"])] for lbl, val in rows]
    table = Table(data, colWidths=[2.35 * inch, 3.95 * inch], hAlign="CENTER")
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.6, colors.HexColor("#404040")),
        ("BACKGROUND", (0, 0), (0, -1), HDR),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    flow.append(table)
    return flow


def signature_flowables() -> list:
    head = [Paragraph(h, STYLES["cover_head"])
            for h in ("Name", "Roll Number", "Signature")]
    data = [head]
    for name, roll, _role in content.MEMBERS:
        data.append([Paragraph(name, STYLES["cover_cell"]),
                     Paragraph(roll, STYLES["cover_cell"]),
                     Paragraph("", STYLES["cover_cell"])])
    table = Table(data, colWidths=[2.4 * inch, 1.5 * inch, 2.4 * inch],
                  hAlign="CENTER", rowHeights=[None, 30, 30, 30])
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.6, colors.HexColor("#404040")),
        ("BACKGROUND", (0, 0), (-1, 0), HDR),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]))
    return [table, Spacer(1, 8)]


def render(blocks: list) -> list:
    flow = []
    for kind, payload in blocks:
        if kind == "h1":
            flow.append(Paragraph(esc(payload), STYLES["h1"]))
        elif kind == "h2":
            flow.append(Paragraph(esc(payload), STYLES["h2"]))
        elif kind == "p":
            flow.append(Paragraph(rich(payload), STYLES["body"]))
        elif kind == "bullets":
            for item in payload:
                flow.append(Paragraph(rich(item),
                                      ParagraphStyle("b", parent=STYLES["body"],
                                                     leftIndent=18,
                                                     bulletIndent=6,
                                                     spaceAfter=3),
                                      bulletText="\u2022"))
        elif kind == "table":
            flow.extend(table_flowable(payload))
        elif kind == "figure":
            fig = figure_flowable(payload)
            head = flow[-1] if flow else None
            # a heading must never be left alone at the bottom of a page
            if head is not None and getattr(head, "style", None) is not None \
                    and head.style.name in ("h1", "h2"):
                flow.pop()
                inner = getattr(fig, "_content", None)
                flow.append(KeepTogether([head] + list(inner) if inner
                                         else [head, fig]))
            else:
                flow.append(fig)
        elif kind == "code":
            size = payload.get("size", 8.0)
            flow.append(Spacer(1, 4 if size >= 8 else 2))
            flow.append(code_flowable(payload["text"], size))
            if payload.get("caption"):
                flow.append(Paragraph(rich(payload["caption"]),
                                      STYLES["caption"]))
        elif kind == "codefile":
            head = ParagraphStyle("fh", fontName="Courier-Bold", fontSize=9.5,
                                  leading=11.4, spaceBefore=12, spaceAfter=3,
                                  keepWithNext=1, textColor=INK)
            flow.append(Paragraph(esc(payload["path"]), head))
            flow.append(Paragraph(esc(payload["desc"]),
                                  ParagraphStyle("fd", parent=STYLES["caption"],
                                                 alignment=TA_LEFT,
                                                 spaceBefore=0, spaceAfter=4,
                                                 keepWithNext=1)))
            flow.append(code_flowable(content.read(payload["path"]), 7.6))
            flow.append(Spacer(1, 6))
        elif kind == "refs":
            for item in payload:
                flow.append(Paragraph(rich(item), STYLES["ref"]))
        elif kind == "cover":
            flow.extend(cover_flowables())
        elif kind == "signature_table":
            flow.extend(signature_flowables())
        elif kind == "newtemplate":
            flow.append(NextPageTemplate(payload))
            flow.append(PageBreak())
        elif kind == "codehead":
            flow.append(Paragraph(esc(payload), ParagraphStyle(
                "ah", fontName="Courier-Bold", fontSize=7.0, leading=8.6,
                spaceBefore=10, spaceAfter=3, keepWithNext=1, textColor=INK)))
        elif kind == "pagebreak":
            flow.append(PageBreak())
        elif kind == "spacer":
            flow.append(Spacer(1, payload))
        else:
            raise ValueError(kind)
    return flow


def build() -> str:
    path = os.path.join(OUT, content.REPORT_NAME + ".pdf")
    doc = BaseDocTemplate(path, pagesize=A4, leftMargin=MARGIN,
                          rightMargin=MARGIN, topMargin=MARGIN,
                          bottomMargin=MARGIN, title="COAL Final Project Report "
                          "- Depth Charge", author="Muhammad Anas, Syed Alyan "
                          "Hussain, Ali Raza", subject="EL-2003 COAL Lab Fall 2026")
    frame = Frame(MARGIN, MARGIN, FRAME_W, PAGE_H - 2 * MARGIN, id="body",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    gutter = 14
    col_w = (FRAME_W - gutter) / 2.0
    col_h = PAGE_H - 2 * MARGIN
    left = Frame(MARGIN, MARGIN, col_w, col_h, id="col1",
                 leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    right = Frame(MARGIN + col_w + gutter, MARGIN, col_w, col_h, id="col2",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([
        PageTemplate(id="all", frames=[frame], onPage=header_footer),
        PageTemplate(id="two", frames=[left, right], onPage=header_footer),
    ])
    doc.build(render(content.build_blocks()))
    print("wrote", path)
    return path


if __name__ == "__main__":
    build()
