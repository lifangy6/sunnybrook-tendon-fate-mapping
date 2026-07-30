"""Shared visual language for the BINF6999 poster figures.

One semantic colour mapping is used across every figure so a viewer never has to
re-learn the legend: blue always means regenerative / TSPC / innervated, red
always means fibrotic / T-FAP / denervated, and the two bystander populations
recede into grey. All figures render transparent and untitled -- the poster's
own typography supplies headings and captions.

Blue/red is deliberate: red-green is the pair the common colour-vision
deficiencies (protan, deutan) confuse, so no other colour in this palette may
be blue. That constraint is why the TF-family and Venn colours below are warm
or violet rather than the blues they would otherwise naturally take.
"""
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import matplotlib.patheffects as pe

# --- semantic palette -------------------------------------------------------
BLUE = "#1F6FA8"        # regenerative / TSPC / innervated
BLUE_L = "#8DBEDC"
RED = "#BE3A34"         # fibrotic / T-FAP / denervated
RED_L = "#E5A29D"
INK = "#16202A"         # primary text
INK_2 = "#5C6B7A"       # secondary text
GREY = "#93A3B2"        # bystander population 1 (Tenogenic-progenitor)
GREY_L = "#C2CBD4"      # bystander population 2 (Stromal)
GOLD = "#C8892B"        # accent, used only for the surviving/unanimous set
PANEL = "#F4F6F7"

CELL_COLORS = {
    "TSPC": BLUE,
    "T-FAP": RED,
    "Tenogenic-progenitor": GREY,
    "Stromal": GREY_L,
}
COND_COLORS = {"Innervated": BLUE, "Denervated": RED}

# TF family colours for the circuit diagram. All three families drive the
# fibrotic program, so they run red -> magenta -> violet; none may be blue,
# which would read as "regenerative" against the semantic palette above.
FAMILY_COLORS = {
    "AP-1": RED,
    "KLF": "#B04A7A",
    "NF-kB/Inflammatory": "#7B4F9E",
}


def pick_font() -> str:
    """First available of a preferred sans stack, falling back to DejaVu Sans."""
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in ("Segoe UI", "Calibri", "Helvetica Neue", "Arial", "DejaVu Sans"):
        if name in available:
            return name
    return "DejaVu Sans"


FONT = pick_font()


def apply_style(base: float = 17.0) -> None:
    """Figures are rendered at their final poster size, so point sizes here are
    literal poster point sizes."""
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": [FONT, "DejaVu Sans"],
        "font.size": base,
        "axes.labelsize": base,
        "axes.titlesize": base,
        "xtick.labelsize": base - 1,
        "ytick.labelsize": base - 1,
        "legend.fontsize": base - 1,
        "axes.edgecolor": INK_2,
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": INK_2,
        "ytick.color": INK_2,
        "axes.linewidth": 1.4,
        "xtick.major.width": 1.4,
        "ytick.major.width": 1.4,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.facecolor": "none",
        "axes.facecolor": "none",
        "savefig.facecolor": "none",
        "savefig.transparent": True,
        "svg.fonttype": "none",
    })


def halo(lw: float = 3.5):
    """White outline so direct labels stay readable over dense point clouds."""
    return [pe.withStroke(linewidth=lw, foreground="white")]


def save(fig, path, dpi: int = 300) -> None:
    fig.savefig(path, dpi=dpi, transparent=True, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    print(f"  saved {path}")
