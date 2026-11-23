from __future__ import annotations

import textwrap

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import (
    FancyBboxPatch,
    FancyArrowPatch,
    Polygon,
)

INK = "#1a1a1a"
MUTED = "#5a5a5a"

STYLES = {
    "term": dict(fc="#d9e8d2", ec="#2f6b2f"),
    "proc": dict(fc="#e8eef7", ec="#2f4f7f"),
    "data": dict(fc="#fdf3d8", ec="#8a6b1f"),
    "dec": dict(fc="#f7e6e6", ec="#8a2f2f"),
    "io": dict(fc="#ece7f7", ec="#4b3a7f"),
}

CHAR_W = 0.50


def new_figure(w: float, h: float):
    fig = plt.figure(figsize=(w, h), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def _wrap(text: str, width: float, fs: float) -> list[str]:
    limit = max(8, int(width / (fs * CHAR_W / 72.0)))
    out: list[str] = []
    for raw in text.split("\n"):
        out.extend(textwrap.wrap(raw, limit) or [""])
    return out


def box(ax, cx, cy, w, h, text, style="proc", fs=7.2, bold_first=False,
        shape="rect", color=None, text_color=INK, lw=0.9, zorder=3):
    st = STYLES[style]
    fc = color or st["fc"]
    ec = st["ec"]
    x0, y0 = cx - w / 2, cy - h / 2

    if shape == "diamond":
        pts = [(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)]
        ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=ec, lw=lw, zorder=zorder))
        inner_w = w * 0.62
    elif shape == "term":
        ax.add_patch(FancyBboxPatch((x0, y0), w, h,
                                    boxstyle="round,pad=0,rounding_size=%.4f" % (h / 2),
                                    fc=fc, ec=ec, lw=lw, zorder=zorder))
        inner_w = w * 0.9
    elif shape == "round":
        ax.add_patch(FancyBboxPatch((x0, y0), w, h,
                                    boxstyle="round,pad=0,rounding_size=0.07",
                                    fc=fc, ec=ec, lw=lw, zorder=zorder))
        inner_w = w * 0.9
    elif shape == "none":
        inner_w = w * 0.95
    else:
        ax.add_patch(FancyBboxPatch((x0, y0), w, h,
                                    boxstyle="square,pad=0",
                                    fc=fc, ec=ec, lw=lw, zorder=zorder))
        inner_w = w * 0.92

    lines = _wrap(text, inner_w, fs)
    line_h = fs * 1.22 / 72.0
    total = len(lines) * line_h
    y = cy + total / 2 - line_h * 0.78
    for i, line in enumerate(lines):
        ax.text(cx, y - i * line_h, line, ha="center", va="center",
                fontsize=fs, color=text_color, zorder=zorder + 1,
                fontweight="bold" if (bold_first and i == 0) else "normal",
                family="DejaVu Sans")
    return x0, y0, x0 + w, y0 + h


def arrow(ax, p1, p2, label=None, fs=6.4, style="-|>", lw=0.9,
          color=MUTED, rad=0.0, label_pos=0.5, label_dx=0.04, label_dy=0.0,
          ha="left", va="center"):
    a = FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=8,
                        lw=lw, color=color, shrinkA=0, shrinkB=0,
                        connectionstyle=f"arc3,rad={rad}", zorder=2)
    ax.add_patch(a)
    if label:
        lx = p1[0] + (p2[0] - p1[0]) * label_pos + label_dx
        ly = p1[1] + (p2[1] - p1[1]) * label_pos + label_dy
        ax.text(lx, ly, label, fontsize=fs, color=color, ha=ha, va=va,
                zorder=4, family="DejaVu Sans")


def polyline(ax, points, label=None, fs=6.4, color=MUTED, lw=0.9,
             label_at=None, label_dx=0.04, label_dy=0.0):
    pts = list(points)
    for a, b in zip(pts[:-2], pts[1:-1]):
        ax.plot([a[0], b[0]], [a[1], b[1]], color=color, lw=lw, zorder=2,
                solid_capstyle="butt")
    arrow(ax, pts[-2], pts[-1], color=color, lw=lw)
    if label:
        at = label_at or pts[len(pts) // 2]
        ax.text(at[0] + label_dx, at[1] + label_dy, label, fontsize=fs,
                color=color, ha="left", va="center", zorder=4,
                family="DejaVu Sans")


def save(fig, path: str, pad: float = 0.04) -> None:
    fig.savefig(path, dpi=300, facecolor="white",
                bbox_inches="tight", pad_inches=pad)
    plt.close(fig)
    print("wrote", path)
