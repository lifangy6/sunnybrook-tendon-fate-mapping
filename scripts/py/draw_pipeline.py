"""Draw the Stage 0-9 analysis pipeline as it was actually run.

Documentation art: nothing is read from data/, so the figure is only as current
as the labels below. Every number here is transcribed from docs/progress.md.

Palette matches scripts/py/poster_style.py: blue = regenerative / TSPC /
innervated, red = fibrotic / T-FAP / denervated. Those two are reserved for the
biology; the pipeline itself is drawn in neutral slate so a reader never has to
wonder whether a box colour means a cell type.

Run:  python scripts/py/draw_pipeline.py
"""
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.font_manager import fontManager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / 'figures' / 'pipeline_flowchart.png'

# --- palette (mirrors poster_style.py) --------------------------------------
BLUE = '#1F6FA8'      # regenerative / TSPC / innervated
RED = '#BE3A34'       # fibrotic / T-FAP / denervated
INK = '#16202A'       # primary text, source datasets
INK_2 = '#5C6B7A'     # secondary text, arrows
GREY = '#93A3B2'      # process box border
GREY_L = '#C2CBD4'
GOLD = '#C8892B'      # deliverables and audit re-runs
PANEL = '#F4F6F7'     # process box fill
HPC = '#EAF0F4'       # cluster-job fill
AUDIT = '#FBF4E8'     # stress-test badge fill


def pick_font():
    available = {f.name for f in fontManager.ttflist}
    for name in ('Segoe UI', 'Calibri', 'Helvetica Neue', 'Arial', 'DejaVu Sans'):
        if name in available:
            return name
    return 'DejaVu Sans'


plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': [pick_font(), 'DejaVu Sans'],
    'text.color': INK,
})

fig, ax = plt.subplots(figsize=(11.5, 17.5))
ax.set_xlim(0, 12)
ax.set_ylim(0, 19)
ax.axis('off')
fig.patch.set_facecolor('white')


def box(cx, cy, w, h, *, fc, ec, lw=1.3, z=3):
    ax.add_patch(FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle='round,pad=0.06,rounding_size=0.12',
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=z))


def title(cx, cy, text, fs=10.5, color=INK):
    ax.text(cx, cy, text, ha='center', va='center', fontsize=fs,
            fontweight='bold', color=color, zorder=5)


def body(cx, cy, text, fs=8.4, color=INK_2):
    ax.text(cx, cy, text, ha='center', va='top', fontsize=fs, color=color,
            zorder=5, linespacing=1.55, multialignment='center')


def chip(x, y, label, fc=INK, tc='white', fs=7.4):
    """Small tag naming the notebook or script that runs this step."""
    w = 0.1 + 0.17 * len(label)
    ax.add_patch(FancyBboxPatch(
        (x, y - 0.16), w, 0.32,
        boxstyle='round,pad=0.04,rounding_size=0.08',
        facecolor=fc, edgecolor='none', zorder=6))
    ax.text(x + w / 2, y, label, ha='center', va='center',
            fontsize=fs, color=tc, fontweight='bold', zorder=7)


def arrow(x1, y1, x2, y2, color=INK_2, lw=1.5):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2), arrowstyle='-|>', mutation_scale=13,
        color=color, lw=lw, shrinkA=0, shrinkB=0, zorder=2))


def badge(cx, cy, w, mark, text):
    """Audit re-run verdict. Carried by the words, with the mark as reinforcement
    only -- never by colour alone."""
    box(cx, cy, w, 0.52, fc=AUDIT, ec=GOLD, lw=1.0)
    ax.text(cx - w / 2 + 0.24, cy, mark, ha='left', va='center',
            fontsize=9.5, fontweight='bold', color=GOLD, zorder=5)
    ax.text(cx - w / 2 + 0.62, cy, text, ha='left', va='center',
            fontsize=8.0, color=INK, zorder=5)


# ── title ────────────────────────────────────────────────────────────────────
ax.text(6.0, 18.55, 'A Mechanism-Informed Gene Signature for Tendon Healing',
        ha='center', va='center', fontsize=15, fontweight='bold', color=INK)
ax.text(6.0, 18.13,
        'Analysis pipeline, Stages 1–9   ·   numbered tags = notebooks in scripts/ipynb/,   '
        'sh / py = scripts in scripts/sh/ and scripts/py/',
        ha='center', va='center', fontsize=8.8, color=INK_2)

# ── 1. source datasets ───────────────────────────────────────────────────────
box(3.25, 17.15, 5.4, 1.05, fc=INK, ec=INK)
title(3.25, 17.45, 'Cherief 2023  ·  GSE244921', fs=10, color='white')
body(3.25, 17.26,
     'Mouse Achilles tendon, day 14 post-injury\n'
     'Innervated (TrkA$^{WT}$)  vs.  denervated (TrkA$^{F592A}$)',
     fs=8.2, color='#D7DEE4')

box(8.75, 17.15, 5.4, 1.05, fc=INK, ec=INK)
title(8.75, 17.45, 'Harvey 2019  ·  SRR9087252', fs=10, color='white')
body(8.75, 17.26,
     'Mouse patellar tendon, uninjured\n'
     'Raw FASTQs (23.2 GB) → Cell Ranger 10, mm10',
     fs=8.2, color='#D7DEE4')

arrow(3.25, 16.62, 3.25, 16.06)
arrow(8.75, 16.62, 8.75, 16.06)

# ── 2. preprocessing and annotation ──────────────────────────────────────────
box(3.25, 15.31, 5.4, 1.42, fc=PANEL, ec=GREY)
chip(0.72, 15.85, '01')
chip(1.32, 15.85, '02')
title(3.45, 15.85, 'QC, clustering, sub-clustering', fs=9.8)
body(3.25, 15.62,
     '22,615 cells  →  17 Leiden clusters\n'
     'PDGFRα⁺ cluster 8 (3,900 cells) resolved into\n'
     'TSPC 451 · T-FAP 1,245 · Tenogenic 816 · Stromal 1,388',
     fs=8.2)

box(8.75, 15.31, 5.4, 1.42, fc=PANEL, ec=GREY)
chip(6.22, 15.85, '03')
chip(6.82, 15.85, 'sh', fc=BLUE)
title(9.05, 15.85, 'QC, clustering, annotation', fs=9.8)
body(8.75, 15.62,
     '4,069 cells  →  12 clusters\n'
     'Ground-truth labels for training:\n'
     'TSPC 266 · T-FAP 433',
     fs=8.2)

arrow(3.25, 14.60, 3.25, 13.98)
arrow(8.75, 14.60, 8.75, 13.98)

# ── 3. pySCENIC on the cluster ───────────────────────────────────────────────
box(6.0, 13.42, 11.2, 1.1, fc=HPC, ec=BLUE, lw=1.2)
chip(0.72, 13.72, 'sh', fc=BLUE)
chip(1.32, 13.72, 'py', fc=BLUE)
title(6.35, 13.72, 'pySCENIC  ·  Alliance Canada HPC', fs=9.8, color=BLUE)
body(6.0, 13.50,
     'GRNBoost2  →  cisTarget motif pruning  →  AUCell            471 Harvey / 417 Cherief regulons',
     fs=8.2)

arrow(2.35, 12.87, 2.35, 12.42)
arrow(6.00, 12.87, 6.00, 12.42)
arrow(9.65, 12.87, 9.65, 12.42)

# ── 4. three mechanistic analyses ────────────────────────────────────────────
for cx in (2.35, 6.0, 9.65):
    box(cx, 11.485, 3.5, 1.78, fc=PANEL, ec=GREY)

chip(0.78, 12.12, '04')
title(2.55, 12.12, 'Regulon activity', fs=9.5)
body(2.35, 11.90,
     'Wilcoxon, TSPC vs. T-FAP,\nboth datasets\n\n'
     '15 consistent T-FAP regulons\n(AP-1 · KLF · NF-κB)\n'
     '0 consistent TSPC regulons',
     fs=8.0)

chip(4.43, 12.12, '05')
title(6.20, 12.12, 'Fate trajectory', fs=9.5)
body(6.0, 11.90,
     'CellRank 2 PseudotimeKernel\n(DPT — no RNA velocity\navailable)  ·  GPCCA\n\n'
     'T-FAP fate 17.2% → 28.9%\ninnervated → denervated',
     fs=8.0)

chip(8.08, 12.12, '06')
title(9.85, 12.12, 'Cell–cell signalling', fs=9.5)
body(9.65, 11.90,
     'LIANA rank_aggregate\n6 methods, mouse consensus\n\n'
     '52,646 LR pairs;  11,669\nwith TSPC or T-FAP as\nreceiver',
     fs=8.0)

badge(2.35, 10.22, 3.5, r'$\checkmark$', '04b  power-matched: holds')
badge(6.00, 10.22, 3.5, '≈', '05b  root swap: 94% stable')
badge(9.65, 10.22, 3.5, '!', '06b  permutation: 3/7 hold')

arrow(2.35, 9.96, 2.35, 9.33)
arrow(6.00, 9.96, 6.00, 9.33)
arrow(9.65, 9.96, 9.65, 9.33)

# ── 5. synthesis ─────────────────────────────────────────────────────────────
box(6.0, 8.72, 11.2, 1.15, fc=PANEL, ec=GREY)
chip(0.72, 9.03, '07')
title(6.30, 9.03, 'Mechanistic synthesis  —  TF regulons × fate drivers × signalling', fs=9.8)
body(6.0, 8.80,
     'Junb (35 genes) · Jund (31) · Klf9 (28) anchor the fate program;   '
     'Pbx1 / Prdm16 / Zfp369 contribute none',
     fs=8.2)

badge(6.0, 7.85, 11.2, r'$\times$',
      '07b  receptor-feedback claim tested by hypergeometric enrichment — not significant, retracted from the narrative')

arrow(6.0, 7.59, 6.0, 7.22)

# ── 6. candidate feature set ─────────────────────────────────────────────────
box(6.0, 6.88, 8.8, 0.68, fc='white', ec=GOLD, lw=1.4)
ax.text(6.0, 6.88,
        '124 mechanism-informed candidates   =   119 (pySCENIC targets  ∩  CellRank T-FAP drivers)  +  5 TSPC markers',
        ha='center', va='center', fontsize=8.6, color=INK, zorder=5)

arrow(6.0, 6.54, 6.0, 6.20)

# ── 7. feature selection ─────────────────────────────────────────────────────
box(6.0, 5.62, 11.2, 1.15, fc=PANEL, ec=GREY)
chip(0.72, 5.93, '08')
title(6.30, 5.93, 'Feature selection on Harvey TSPC vs. T-FAP', fs=9.8)
body(6.0, 5.70,
     'LASSO  ·  Boruta  ·  XGBoost (gain), run independently          '
     '≥2/3 methods → 44 genes          3/3 unanimous → 23 genes',
     fs=8.2)

arrow(6.0, 5.04, 6.0, 4.62)

# ── 8. classifier ────────────────────────────────────────────────────────────
box(6.0, 3.92, 11.2, 1.35, fc=PANEL, ec=GREY)
chip(0.72, 4.33, '09')
title(6.30, 4.33, 'Classifier  —  logistic regression (L2, class-balanced)', fs=9.8)
body(6.0, 4.10,
     '23-gene panel —  Harvey, 10-fold CV:  ROC-AUC 0.993          '
     'held-out Cherief:  ROC-AUC 0.989 · balanced accuracy 88.3%\n'
     'Standing weak point: TSPC recall 77–78% vs. T-FAP 98–99% — better at flagging fibrotic drift '
     'than confirming regeneration',
     fs=8.2)

arrow(6.0, 3.24, 6.0, 2.82)

# ── 9. healing index ─────────────────────────────────────────────────────────
box(6.0, 1.95, 11.2, 1.7, fc='white', ec=GOLD, lw=1.6)
chip(0.72, 2.52, '10', fc=GOLD)
title(6.30, 2.52, 'Healing Index  —  continuous 0–100 score, percentile-calibrated log-odds', fs=10.2)

cmap = LinearSegmentedColormap.from_list('hi', [RED, '#D8D2CB', BLUE])
ax.imshow(np.linspace(0, 1, 256).reshape(1, -1),
          extent=(3.25, 8.75, 1.98, 2.20), aspect='auto', cmap=cmap, zorder=4)
ax.add_patch(FancyBboxPatch((3.25, 1.98), 5.5, 0.22, boxstyle='square,pad=0',
                            facecolor='none', edgecolor=GREY_L, lw=0.8, zorder=5))
ax.text(3.15, 2.09, '0  ·  fibrotic (T-FAP)', ha='right', va='center',
        fontsize=8.0, color=RED, fontweight='bold', zorder=5)
ax.text(8.85, 2.09, 'regenerative (TSPC)  ·  100', ha='left', va='center',
        fontsize=8.0, color=BLUE, fontweight='bold', zorder=5)

body(6.0, 1.82,
     'Cherief cluster 8:  innervated 25.2  vs.  denervated 15.5          '
     'Cross-check vs. CellRank fate probability:  Spearman ρ = 0.656\n'
     'score_new_dataset() scores any new .h5ad against the same fixed Harvey reference',
     fs=8.2)

# ── footer: the standing limitation ──────────────────────────────────────────
ax.text(6.0, 0.74,
        'Neither dataset has biological replicates — one pooled sample per condition. '
        'Every validation above is a within- or cross-dataset check, never cross-animal.',
        ha='center', va='center', fontsize=8.4, color=INK_2, style='italic')

# ── legend ───────────────────────────────────────────────────────────────────
handles = [
    mpatches.Patch(fc=INK, ec=INK, label='Source dataset'),
    mpatches.Patch(fc=PANEL, ec=GREY, label='Local analysis'),
    mpatches.Patch(fc=HPC, ec=BLUE, label='Cluster job (Alliance Canada)'),
    mpatches.Patch(fc=AUDIT, ec=GOLD, label='Audit re-run (stress test)'),
    mpatches.Patch(fc='white', ec=GOLD, label='Deliverable'),
]
ax.legend(handles=handles, loc='lower center', bbox_to_anchor=(0.5, -0.008),
          ncol=5, fontsize=7.8, framealpha=1.0, edgecolor=GREY_L,
          handlelength=1.3, columnspacing=1.2, borderpad=0.6)

fig.savefig(OUTPUT, dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none', pad_inches=0.25)
plt.close(fig)
print(f'Saved: {OUTPUT}')
