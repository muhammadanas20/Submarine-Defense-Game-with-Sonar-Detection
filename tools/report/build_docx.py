"""Build the final report as a Word .docx that follows the course template."""

from __future__ import annotations

import os
import re
import sys

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor, Emu

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import content  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = content.ROOT
OUT = os.path.join(ROOT, "docs", "submission")

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

# child order required by the WordprocessingML schema (subset we use)
PPR_ORDER = ["pStyle", "keepNext", "keepLines", "pageBreakBefore", "framePr",
             "widowControl", "numPr", "suppressLineNumbers", "pBdr", "shd",
             "tabs", "suppressAutoHyphens", "kinsoku", "wordWrap",
             "overflowPunct", "topLinePunct", "autoSpaceDE", "autoSpaceDN",
             "bidi", "adjustRightInd", "snapToGrid", "spacing", "ind",
             "contextualSpacing", "mirrorIndents", "suppressOverlap", "jc",
             "textDirection", "textAlignment", "textboxTightWrap", "outlineLvl",
             "divId", "cnfStyle", "rPr", "sectPr", "pPrChange"]
TCPR_ORDER = ["cnfStyle", "tcW", "gridSpan", "hMerge", "vMerge", "tcBorders",
              "shd", "noWrap", "tcMar", "textDirection", "tcFitText", "vAlign",
              "hideMark", "headers", "cellIns", "cellDel", "cellMerge",
              "tcPrChange"]
TRPR_ORDER = ["cnfStyle", "divId", "gridBefore", "gridAfter", "wBefore",
              "wAfter", "cantSplit", "trHeight", "tblHeader", "tblCellSpacing",
              "jc", "hidden", "ins", "del", "trPrChange"]


def insert_ordered(parent, element, order) -> None:
    """Insert element into parent at the position the schema requires."""
    tag = element.tag.replace(W, "")
    index = order.index(tag)
    for child in list(parent):
        child_tag = child.tag.replace(W, "")
        if child_tag in order and order.index(child_tag) > index:
            child.addprevious(element)
            return
    parent.append(element)


BODY_FONT = "Times New Roman"
CODE_FONT = "Consolas"
TEXT_COLOR = RGBColor(0x00, 0x00, 0x00)
HDR_FILL = "DCE6F1"
CODE_FILL = "F5F5F5"


# ---------------------------------------------------------------------------
# low-level helpers
# ---------------------------------------------------------------------------
def set_run_font(run, name=BODY_FONT, size=12, bold=None, italic=None,
                 color=TEXT_COLOR):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.color.rgb = color
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), name)


def shade(cell_or_par, fill):
    el = cell_or_par._element
    if el.tag.endswith("}tc"):
        pr, order = el.get_or_add_tcPr(), TCPR_ORDER
    else:
        pr, order = el.get_or_add_pPr(), PPR_ORDER
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    insert_ordered(pr, shd, order)


def para_border(paragraph, edge="bottom", size=6, color="A6A6A6", space=1):
    p_pr = paragraph._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    el = OxmlElement(f"w:{edge}")
    el.set(qn("w:val"), "single")
    el.set(qn("w:sz"), str(size))
    el.set(qn("w:space"), str(space))
    el.set(qn("w:color"), color)
    borders.append(el)
    insert_ordered(p_pr, borders, PPR_ORDER)


def add_field(paragraph, instr: str) -> None:
    run = paragraph.add_run()
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), instr)
    t = OxmlElement("w:t")
    t.text = "1"
    r = OxmlElement("w:r")
    r.append(t)
    fld.append(r)
    run._r.addnext(fld)


def repeat_header(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:tblHeader")
    el.set(qn("w:val"), "true")
    insert_ordered(tr_pr, el, TRPR_ORDER)


def cant_split(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:cantSplit")
    el.set(qn("w:val"), "true")
    insert_ordered(tr_pr, el, TRPR_ORDER)


TOKEN = re.compile(r"(<b>.*?</b>|<i>.*?</i>)", re.S)


def add_rich(paragraph, text: str, size=12, font=BODY_FONT,
             color=TEXT_COLOR) -> None:
    """Add text that may contain <b>..</b> and <i>..</i> runs."""
    for piece in TOKEN.split(text):
        if not piece:
            continue
        if piece.startswith("<b>") and piece.endswith("</b>"):
            set_run_font(paragraph.add_run(piece[3:-4]), font, size, bold=True,
                         color=color)
        elif piece.startswith("<i>") and piece.endswith("</i>"):
            set_run_font(paragraph.add_run(piece[3:-4]), font, size, italic=True,
                         color=color)
        else:
            set_run_font(paragraph.add_run(piece), font, size, color=color)


# ---------------------------------------------------------------------------
# document setup
# ---------------------------------------------------------------------------
def setup(doc: Document) -> None:
    sec = doc.sections[0]
    sec.page_width = Inches(8.27)
    sec.page_height = Inches(11.69)
    for side in ("top_margin", "bottom_margin", "left_margin", "right_margin"):
        setattr(sec, side, Inches(1))
    sec.header_distance = Inches(0.5)
    sec.footer_distance = Inches(0.5)

    normal = doc.styles["Normal"]
    normal.font.name = BODY_FONT
    normal.font.size = Pt(12)
    normal.font.color.rgb = TEXT_COLOR
    normal.paragraph_format.line_spacing = 1.15
    normal.paragraph_format.space_after = Pt(5)
    normal.paragraph_format.space_before = Pt(0)
    rpr = normal.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), BODY_FONT)

    for name, size, before, after in (("Heading 1", 14, 12, 6),
                                      ("Heading 2", 12, 10, 4)):
        st = doc.styles[name]
        st.font.name = BODY_FONT
        st.font.size = Pt(size)
        st.font.bold = True
        st.font.italic = False
        st.font.color.rgb = TEXT_COLOR
        st.paragraph_format.space_before = Pt(before)
        st.paragraph_format.space_after = Pt(after)
        st.paragraph_format.line_spacing = 1.15
        st.paragraph_format.keep_with_next = True
        rpr = st.element.get_or_add_rPr()
        rfonts = rpr.find(qn("w:rFonts"))
        if rfonts is None:
            rfonts = OxmlElement("w:rFonts")
            rpr.append(rfonts)
        # theme fonts would override the explicit font in Word
        for attr in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme",
                     "w:cstheme"):
            if rfonts.get(qn(attr)) is not None:
                del rfonts.attrib[qn(attr)]
        for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            rfonts.set(qn(attr), BODY_FONT)
        color = rpr.find(qn("w:color"))
        if color is not None:
            for attr in ("w:themeColor", "w:themeShade", "w:themeTint"):
                if color.get(qn(attr)) is not None:
                    del color.attrib[qn(attr)]

    # header / footer
    head = sec.header.paragraphs[0]
    head.alignment = WD_ALIGN_PARAGRAPH.LEFT
    set_run_font(head.add_run("EL-2003 COAL Lab  |  Fall 2026  |  "
                              "Final Project Report"), BODY_FONT, 9,
                 color=RGBColor(0x40, 0x40, 0x40))
    para_border(head, "bottom", size=4, color="BFBFBF", space=2)

    foot = sec.footer.paragraphs[0]
    foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run_font(foot.add_run("Page "), BODY_FONT, 9,
                 color=RGBColor(0x40, 0x40, 0x40))
    add_field(foot, "PAGE")


# ---------------------------------------------------------------------------
# block renderers
# ---------------------------------------------------------------------------
def add_cover(doc: Document) -> None:
    for _ in range(4):
        doc.add_paragraph()

    logo = os.path.join(content.ASSETS, "fast_nu_logo.png")
    if os.path.exists(logo):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(logo, width=Inches(3.1))

    lines = [
        ("National University of Computer and Emerging Sciences", 16, True),
        ("Karachi Campus", 13, True),
        ("", 8, False),
        ("EL-2003  Computer Organization and Assembly Language (COAL) Lab", 12, False),
        ("Fall 2026", 12, False),
        ("", 10, False),
        ("FINAL PROJECT REPORT", 18, True),
    ]
    for text, size, bold in lines:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
        if text:
            set_run_font(p.add_run(text), BODY_FONT, size, bold=bold)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(28)
    p.paragraph_format.space_after = Pt(6)

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
    table = doc.add_table(rows=len(rows), cols=2)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r, (label, value) in enumerate(rows):
        lc, vc = table.rows[r].cells
        lc.width = Inches(2.35)
        vc.width = Inches(3.95)
        lp = lc.paragraphs[0]
        set_run_font(lp.add_run(label), BODY_FONT, 11, bold=True)
        vp = vc.paragraphs[0]
        add_rich(vp, value, size=11)
        shade(lc, HDR_FILL)
        for c in (lc, vc):
            c.paragraphs[0].paragraph_format.space_after = Pt(2)
            c.paragraphs[0].paragraph_format.line_spacing = 1.0


def add_signature_table(doc: Document) -> None:
    table = doc.add_table(rows=4, cols=3)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    heads = ["Name", "Roll Number", "Signature"]
    widths = [Inches(2.5), Inches(1.6), Inches(2.2)]
    for c, (text, w) in enumerate(zip(heads, widths)):
        cell = table.rows[0].cells[c]
        cell.width = w
        set_run_font(cell.paragraphs[0].add_run(text), BODY_FONT, 10.5, bold=True)
        shade(cell, HDR_FILL)
    for r, (name, roll, _role) in enumerate(content.MEMBERS, start=1):
        for c, (text, w) in enumerate(zip([name, roll, ""], widths)):
            cell = table.rows[r].cells[c]
            cell.width = w
            set_run_font(cell.paragraphs[0].add_run(text), BODY_FONT, 10.5)
        table.rows[r].height = Inches(0.4)
    for row in table.rows:
        cant_split(row)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def add_caption(doc: Document, text: str, before=False) -> None:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6 if not before else 8)
    p.paragraph_format.space_after = Pt(10 if not before else 3)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.keep_with_next = before
    set_run_font(p.add_run(text), BODY_FONT, 10, italic=True,
                 color=RGBColor(0x33, 0x33, 0x33))


def add_figure(doc: Document, spec: dict) -> None:
    path = os.path.join(content.ASSETS, spec["path"])
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(path, width=Inches(spec.get("width", 6.0)))
    add_caption(doc, spec["caption"])


def add_code(doc: Document, text: str, caption: str | None, size=8.5) -> None:
    for line in text.splitlines():
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        pf.line_spacing = 1.0
        pf.left_indent = Inches(0.05 if size < 7 else 0.08)
        pf.first_line_indent = Inches(0)
        if size >= 6.5:
            shade(p, CODE_FILL)
        set_run_font(p.add_run(line if line.strip() else " "), CODE_FONT, size)
    if caption:
        add_caption(doc, caption)


def add_table(doc: Document, spec: dict) -> None:
    add_caption(doc, spec["caption"], before=True)
    cols = spec["cols"]
    rows = spec["rows"]
    font = spec.get("font", 9.0)
    table = doc.add_table(rows=1 + len(rows), cols=len(cols))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    table._tbl.tblPr.append(layout)
    widths = spec["widths"]
    total = sum(widths)
    limit = 8.27 - 2 * 1.0                 # A4 width less the two 1" margins
    if total > limit:                      # never spill past the right margin
        widths = [w * limit / total for w in widths]
    widths = [Inches(w) for w in widths]

    for c, text in enumerate(cols):
        cell = table.rows[0].cells[c]
        cell.width = widths[c]
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = 1.0
        add_rich(p, text, size=font, color=TEXT_COLOR)
        for run in p.runs:
            run.bold = True
        shade(cell, HDR_FILL)
    repeat_header(table.rows[0])

    for r, values in enumerate(rows, start=1):
        for c, text in enumerate(values):
            cell = table.rows[r].cells[c]
            cell.width = widths[c]
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.0
            add_rich(p, text, size=font)
        cant_split(table.rows[r])
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def add_refs(doc: Document, items: list[str]) -> None:
    for item in items:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.left_indent = Inches(0.45)
        pf.first_line_indent = Inches(-0.45)
        pf.space_after = Pt(1)
        pf.line_spacing = 1.12
        add_rich(p, item, size=10.2)


def add_body(doc: Document, text: str) -> None:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    add_rich(p, text)


def render(doc: Document, blocks: list) -> None:
    for kind, payload in blocks:
        if kind == "h1":
            doc.add_heading(payload, level=1)
        elif kind == "h2":
            doc.add_heading(payload, level=2)
        elif kind == "p":
            add_body(doc, payload)
        elif kind == "bullets":
            for item in payload:
                p = doc.add_paragraph(style="List Bullet")
                add_rich(p, item)
        elif kind == "table":
            add_table(doc, payload)
        elif kind == "figure":
            add_figure(doc, payload)
        elif kind == "code":
            add_code(doc, payload["text"], payload.get("caption"),
                     size=payload.get("size", 8.5))
        elif kind == "newtemplate":
            section = doc.add_section(WD_SECTION.NEW_PAGE)
            sect = section._sectPr
            cols = sect.find(qn("w:cols"))
            if cols is None:
                cols = OxmlElement("w:cols")
                sect.append(cols)
            cols.set(qn("w:num"), "2")
            cols.set(qn("w:space"), "300")
        elif kind == "codehead":
            head = doc.add_paragraph()
            head.paragraph_format.space_before = Pt(6)
            head.paragraph_format.space_after = Pt(2)
            head.paragraph_format.line_spacing = 1.0
            head.paragraph_format.keep_with_next = True
            set_run_font(head.add_run(payload), CODE_FONT, 7.5, bold=True)
        elif kind == "codefile":
            path = os.path.join(content.ROOT, payload["path"])
            head = doc.add_paragraph()
            head.paragraph_format.space_before = Pt(10)
            head.paragraph_format.space_after = Pt(3)
            head.paragraph_format.keep_with_next = True
            set_run_font(head.add_run(payload["path"]), CODE_FONT, 10, bold=True)
            set_run_font(head.add_run("  \u2014  " + payload["desc"]), BODY_FONT,
                         10, italic=True)
            add_code(doc, content.read(path), None, size=8.5)
        elif kind == "refs":
            add_refs(doc, payload)
        elif kind == "cover":
            add_cover(doc)
        elif kind == "signature_table":
            add_signature_table(doc)
        elif kind == "pagebreak":
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        elif kind == "spacer":
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(payload)
        else:
            raise ValueError(kind)


def build() -> str:
    doc = Document()
    setup(doc)
    props = doc.core_properties
    props.title = ("Depth Charge: A Real-Time Submarine Defense Game with Sonar "
                   "Detection in x86 Assembly using Irvine32")
    props.author = "Muhammad Anas, Syed Alyan Hussain, Ali Raza"
    props.subject = "EL-2003 COAL Lab, Fall 2026 - Final Project Report"
    props.keywords = "x86 assembly, MASM, Irvine32, COAL, game, sonar"
    render(doc, content.build_blocks())
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, content.REPORT_NAME + ".docx")
    doc.save(path)
    print("wrote", path)
    return path


if __name__ == "__main__":
    build()
