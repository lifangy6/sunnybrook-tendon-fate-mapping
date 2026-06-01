import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUTPUT = r'c:\Users\fangy\OneDrive\Desktop\sunnybrook-tendon-fate-mapping\figures\pipeline_flowchart.png'

fig, ax = plt.subplots(figsize=(13, 17))
ax.set_xlim(0, 15)
ax.set_ylim(0, 17)
ax.axis('off')
fig.patch.set_facecolor('white')

C = {
    'blue':        '#2471A3',
    'blue_light':  '#D6EAF8',
    'blue_edge':   '#1A5276',
    'green':       '#1E8449',
    'green_light': '#D5F5E3',
    'green_edge':  '#145A32',
    'purple':      '#7D3C98',
    'purple_edge': '#512E5F',
    'gold':        '#D4AC0D',
    'gold_light':  '#FEF9E7',
    'dark':        '#17202A',
    'arrow':       '#2C3E50',
}


def box(cx, cy, w, h, fc, ec, text, fs=10, tc='white', lw=1.8):
    ax.add_patch(FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle='round,pad=0.1',
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3
    ))
    ax.text(cx, cy, text, ha='center', va='center',
            fontsize=fs, color=tc, fontweight='bold',
            multialignment='center', zorder=4, linespacing=1.45)


def arr(x1, y1, x2, y2, dashed=False, color=None, lw=1.8, label='', label_dx=0.3):
    color = color or C['arrow']
    ls = '--' if dashed else '-'
    ax.add_patch(FancyArrowPatch(
        posA=(x1, y1), posB=(x2, y2),
        arrowstyle='->', linestyle=ls,
        color=color, lw=lw, mutation_scale=14, zorder=2
    ))
    if label:
        mx = (x1 + x2) / 2 + label_dx
        my = (y1 + y2) / 2
        ax.text(mx, my, label, fontsize=8.5, color=color,
                style='italic', ha='left', va='center')


# ── Inputs ───────────────────────────────────────────────────────────────────
box(4.5, 16.0, 5.0, 1.0, C['blue'], C['blue_edge'],
    'Cherief 2023  (GSE244921)\nAchilles tendon  |  Innervated vs. Denervated\nn = 3 mice/condition  |  22,615 cells post-QC')

box(12.2, 16.0, 4.0, 1.0, C['green'], C['green_edge'],
    'Harvey 2019  (PRJNA506218)\nPatellar tendon  |  Uninjured\n~2,491 cells  |  8 clusters')

# ── Cherief preprocessing ────────────────────────────────────────────────────
box(4.5, 14.2, 5.0, 0.9, C['blue_light'], C['blue'],
    'Preprocessing & Clustering  (scanpy)\nQC filtering  ·  Normalization  ·  HVG  ·  PCA  ·  Leiden',
    tc=C['dark'])
arr(4.5, 15.5, 4.5, 14.65)

box(4.5, 12.7, 5.0, 0.9, C['blue_light'], C['blue'],
    'PDGFRα⁺  Sub-clustering  ✓\nTSPC  ·  T-FAP  ·  Tenogenic progenitor  ·  Mixed stromal',
    tc=C['dark'])
arr(4.5, 13.75, 4.5, 13.15)

# ── Harvey: Cell Ranger ──────────────────────────────────────────────────────
box(12.2, 12.7, 4.0, 1.4, C['green_light'], C['green'],
    'Cell Ranger  (10x Genomics)\nHarvey 2019 FASTQs → count matrix\nGround-truth TSPC / T-FAP labels',
    tc=C['dark'])
arr(12.2, 15.5, 12.2, 13.4)

# ── Three parallel branches ───────────────────────────────────────────────────
box(1.8, 9.5, 2.8, 2.2, C['blue_light'], C['blue'],
    'pySCENIC\nTF Regulon Inference\nGRNBoost2 → cisTarget\n→ AUCell\nTSPC vs. T-FAP\nspecific regulons',
    fs=9, tc=C['dark'])

box(5.2, 9.5, 2.8, 2.2, C['blue_light'], C['blue'],
    'CellRank 2\nFate Trajectory\n(WOT kernel)\nRoot: PDGFRα⁺\nprogenitors\n→ Driver genes',
    fs=9, tc=C['dark'])

box(8.4, 9.5, 2.8, 2.2, C['blue_light'], C['blue'],
    'LIANA\nCell-Cell Comm.\nInnervated vs.\nDenervated\nNGF · TGFβ · PDGF\n→ Disrupted axes',
    fs=9, tc=C['dark'])

# sub-clustering → three branches
arr(3.1, 12.25, 2.2, 10.6)
arr(4.8, 12.25, 5.0, 10.6)
arr(6.1, 12.25, 8.0, 10.6)

# ── Feature Selection ────────────────────────────────────────────────────────
box(4.3, 6.8, 6.5, 1.6, C['purple'], C['purple_edge'],
    'Mechanism-Informed Feature Selection\nCandidate space:  pySCENIC targets  ∪  CellRank drivers\n'
    'LASSO  ·  Boruta  ·  XGBoost/SHAP  →  Consensus ≥ 2/3\nMinimal gene panel  (10–30 genes)')
arr(1.8, 8.4, 2.7, 7.6)
arr(5.2, 8.4, 5.0, 7.6)

# ── Classifier ───────────────────────────────────────────────────────────────
box(7.8, 4.5, 9.5, 1.6, C['purple'], C['purple_edge'],
    'Classifier Training & Validation\nTrained on Harvey 2019 TSPC / T-FAP labels\n'
    'Validated on Cherief 2023 held-out set  |  AUROC  ·  Brier score',
    fs=11)
arr(5.5, 6.0, 6.2, 5.3)
arr(12.2, 12.0, 12.2, 5.3)

# dashed LIANA → classifier
arr(8.4, 8.4, 9.5, 5.3,
    dashed=True, color=C['purple'], label='signaling\ncontext', label_dx=0.25)

# ── Output ───────────────────────────────────────────────────────────────────
box(7.8, 2.4, 9.5, 1.2, C['gold_light'], C['gold'],
    'Healing Index Score\n'
    '0  (fibrotic)  ──────────────────────  1  (regenerative)\n'
    'Continuous probabilistic output  |  Applicable to any tendon scRNA-seq dataset',
    fs=10, tc=C['dark'])
arr(7.8, 3.7, 7.8, 3.0)

# ── Legend ───────────────────────────────────────────────────────────────────
ax.legend(handles=[
    mpatches.Patch(fc=C['blue'],   ec='white', label='Cherief 2023 pipeline'),
    mpatches.Patch(fc=C['green'],  ec='white', label='Harvey 2019 pipeline'),
    mpatches.Patch(fc=C['purple'], ec='white', label='Integration & Classification'),
    mpatches.Patch(fc=C['gold'],   ec=C['gold'], label='Output'),
], loc='lower left', fontsize=10, framealpha=0.9,
   edgecolor='#bbbbbb', bbox_to_anchor=(0.01, 0.01))

ax.set_title(
    'Analytical Pipeline: Mechanism-Informed Gene Signature for Tendon Healing',
    fontsize=13, fontweight='bold', color=C['dark'], pad=14)

plt.tight_layout(pad=0.4)
plt.savefig(OUTPUT, dpi=600, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()
print(f'Saved: {OUTPUT}')
