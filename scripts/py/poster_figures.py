"""Regenerate every poster figure from source data.

Each figure is rendered at roughly the size it occupies on the 48x36 in poster,
so the point sizes in poster_style.py are literal poster point sizes. All output
is transparent, untitled, and uses the shared semantic palette.

Run:  uv run --python 3.12 --with anndata --with pandas --with scikit-learn \
          --with joblib --with scipy --with matplotlib python scripts/py/poster_figures.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch

sys.path.insert(0, str(Path(__file__).parent))
from poster_style import (  # noqa: E402
    apply_style, save, halo, CELL_COLORS, COND_COLORS, FAMILY_COLORS,
    BLUE, RED, INK, INK_2, GREY, GREY_L, GOLD,
)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "figures" / "poster"
OUT.mkdir(parents=True, exist_ok=True)

CELL_ORDER = ["TSPC", "Tenogenic-progenitor", "Stromal", "T-FAP"]
COND_MAP = {"TrkAWT": "Innervated", "TrkAF592A": "Denervated"}


# --------------------------------------------------------------------------
def fig1_umap():
    """Cherief cluster-8 sub-populations. Direct labels, no axes box, no title."""
    import anndata as ad
    a = ad.read_h5ad(ROOT / "data/Cherief_scRNA-seq/GSE244921_cluster8_sub.h5ad", backed="r")
    obs = a.obs[["cell_type"]].copy()
    xy = np.asarray(a.obsm["X_umap"])
    obs["x"], obs["y"] = xy[:, 0], xy[:, 1]

    fig, ax = plt.subplots(figsize=(12.0, 6.6))

    # Draw bystanders first so the two fate populations sit on top.
    for ct in ["Stromal", "Tenogenic-progenitor", "T-FAP", "TSPC"]:
        d = obs[obs.cell_type == ct]
        emph = ct in ("TSPC", "T-FAP")
        ax.scatter(d.x, d.y, s=14 if emph else 11, c=CELL_COLORS[ct],
                   alpha=0.95 if emph else 0.78, linewidths=0, zorder=3 if emph else 2)

    # Labels live in the margin outside the cloud, tied back with a leader line,
    # so nothing sits on top of the data.
    xmin, xmax = obs.x.min(), obs.x.max()
    ymin, ymax = obs.y.min(), obs.y.max()
    w, h = xmax - xmin, ymax - ymin
    ax.set_xlim(xmin - 0.32 * w, xmax + 0.34 * w)
    ax.set_ylim(ymin - 0.16 * h, ymax + 0.18 * h)

    # (label x, label y, target x, target y) as fractions of the data bounding box
    place = {
        "TSPC": (-0.30, 0.46, 0.06, 0.42),
        "Stromal": (0.16, 1.13, 0.44, 0.66),
        "Tenogenic-progenitor": (1.05, 0.94, 0.80, 0.90),
        "T-FAP": (1.10, 0.18, 0.90, 0.11),
    }
    for ct in CELL_ORDER:
        d = obs[obs.cell_type == ct]
        fx, fy, tx, ty = place[ct]
        colour = CELL_COLORS[ct] if ct in ("TSPC", "T-FAP") else INK_2
        ax.annotate(
            f"{ct}\nn = {len(d):,}",
            xy=(xmin + tx * w, ymin + ty * h),
            xytext=(xmin + fx * w, ymin + fy * h),
            ha="center", va="center", fontsize=21.3, fontweight="bold",
            color=colour, linespacing=1.25, zorder=6,
            arrowprops=dict(arrowstyle="-", color=colour, lw=1.6,
                            alpha=0.65, shrinkA=8, shrinkB=2),
        )

    # A small corner glyph stands in for the axes, which carry no units anyway.
    ax.set_axis_off()
    x0 = xmin - 0.28 * w
    y0 = ymin - 0.10 * h
    ln = 0.11 * w
    ax.annotate("", xy=(x0 + ln, y0), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=INK_2, lw=1.7),
                annotation_clip=False)
    ax.annotate("", xy=(x0, y0 + ln), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=INK_2, lw=1.7),
                annotation_clip=False)
    ax.text(x0 + ln * 1.15, y0, "UMAP1", fontsize=16.5, color=INK_2, va="center")
    ax.text(x0, y0 + ln * 1.15, "UMAP2", fontsize=16.5, color=INK_2,
            ha="center", va="bottom", rotation=90)
    save(fig, OUT / "fig1_umap_subclusters.png")


# --------------------------------------------------------------------------
def fig2_shift():
    """Slope chart: how each sub-population's share of cluster 8 changes when
    the tendon loses its nerve supply. A slope reads as *change*; paired bars
    make the reader do the subtraction."""
    import anndata as ad
    a = ad.read_h5ad(ROOT / "data/Cherief_scRNA-seq/GSE244921_cluster8_sub.h5ad", backed="r")
    obs = a.obs[["cell_type", "condition"]].copy()
    obs["Condition"] = obs.condition.map(COND_MAP)

    counts = obs.groupby(["Condition", "cell_type"], observed=True).size().unstack("cell_type")
    share = counts.div(counts.sum(axis=1), axis=0) * 100

    fig, ax = plt.subplots(figsize=(12.0, 6.4))
    xs = [0, 1]
    for ct in CELL_ORDER:
        emph = ct in ("TSPC", "T-FAP")
        ys = [share.loc["Innervated", ct], share.loc["Denervated", ct]]
        ax.plot(xs, ys, color=CELL_COLORS[ct] if emph else GREY,
                lw=6.5 if emph else 3.4, alpha=1.0 if emph else 0.85,
                marker="o", markersize=15 if emph else 10,
                markeredgecolor="white", markeredgewidth=2.5,
                zorder=4 if emph else 2, solid_capstyle="round")
        for i, (x, y) in enumerate(zip(xs, ys)):
            ax.text(x + (-0.075 if i == 0 else 0.075), y, f"{y:.0f}%",
                    ha="right" if i == 0 else "left", va="center",
                    fontsize=20.7 if emph else 15,
                    fontweight="bold" if emph else "normal",
                    color=CELL_COLORS[ct] if emph else INK_2,
                    path_effects=halo(4), zorder=5)

    # Name each line once, on the right, outside the plotting area.
    for ct in CELL_ORDER:
        emph = ct in ("TSPC", "T-FAP")
        y = share.loc["Denervated", ct]
        ax.text(1.30, y, ct, va="center", ha="left",
                fontsize=20.7 if emph else 15,
                fontweight="bold" if emph else "normal",
                color=CELL_COLORS[ct] if emph else INK_2)

    ax.set_xlim(-0.42, 2.15)
    ax.set_xticks(xs)
    ax.set_xticklabels(["Innervated", "Denervated"], fontsize=23.2, fontweight="bold")
    for tick, cond in zip(ax.get_xticklabels(), ["Innervated", "Denervated"]):
        tick.set_color(COND_COLORS[cond])
    ax.set_ylabel("Share of cluster-8 cells", fontsize=20.7)
    ax.set_ylim(0, 46)
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(axis="x", length=0, pad=12)
    ax.grid(axis="y", color=GREY_L, lw=1.0, alpha=0.6)
    ax.set_axisbelow(True)
    save(fig, OUT / "fig2_composition_shift.png")


# --------------------------------------------------------------------------
def fig3_regulon_scatter():
    """The hero figure. Each point is a TF regulon that is differentially active
    between TSPC and T-FAP in *both* datasets. Positive = T-FAP-associated.
    The upper-right quadrant fills up; the lower-left quadrant -- where a
    reproducible TSPC program would have to live -- is empty."""
    p = ROOT / "data/pyscenic"
    h_f = pd.read_csv(p / "harvey_diff_regulons_T-FAP.csv")
    h_t = pd.read_csv(p / "harvey_diff_regulons_TSPC.csv")
    c_f = pd.read_csv(p / "cherief_diff_regulons_T-FAP.csv")
    c_t = pd.read_csv(p / "cherief_diff_regulons_TSPC.csv")
    shared = pd.read_csv(p / "shared_diff_regulons.csv")
    final15 = set(shared.regulon)

    def signed(fap, tspc):
        s = {r["names"]: r["scores"] for _, r in fap.iterrows()}
        for _, r in tspc.iterrows():
            s.setdefault(r["names"], -r["scores"])
        return pd.Series(s)

    H, C = signed(h_f, h_t), signed(c_f, c_t)
    both = sorted(set(H.index) & set(C.index))
    df = pd.DataFrame({"harvey": H[both], "cherief": C[both]})
    df["name"] = [i.replace("(+)", "") for i in df.index]
    df["final"] = [i in final15 for i in df.index]

    n_tfap = int(((df.harvey > 0) & (df.cherief > 0)).sum())
    n_tspc = int(((df.harvey < 0) & (df.cherief < 0)).sum())
    print(f"  [fig3] {len(df)} regulons differential in both datasets | "
          f"T-FAP quadrant {n_tfap} | TSPC quadrant {n_tspc} | "
          f"passing full filter {int(df.final.sum())}")

    from adjustText import adjust_text

    # Deliberately wider than tall: the poster gives act 2 the widest column,
    # and a square render would leave it floating with large side margins.
    # Kept near 3:2 rather than stretched to the full column width: both axes
    # share the same +/-33 range, so strongly unequal scaling would misread.
    fig, ax = plt.subplots(figsize=(10.5, 6.2))
    lim = 33
    # Shade the two agreement quadrants. Explicit RGBA rather than the alpha
    # kwarg: adjustText forces a canvas draw that loses patch-level alpha.
    ax.add_patch(plt.Rectangle((0, 0), lim, lim, facecolor=(0.745, 0.227, 0.204, 0.09),
                               edgecolor="none", zorder=0))
    ax.add_patch(plt.Rectangle((-lim, -lim), lim, lim, facecolor=(0.055, 0.486, 0.420, 0.09),
                               edgecolor="none", zorder=0))
    ax.axhline(0, color=INK_2, lw=1.4, zorder=1)
    ax.axvline(0, color=INK_2, lw=1.4, zorder=1)

    disc = df[~((df.harvey > 0) & (df.cherief > 0))]
    ax.scatter(disc.harvey, disc.cherief, s=155, facecolor="white",
               edgecolor=GREY, linewidths=2.2, zorder=3,
               label="differential in one dataset only")
    agree_x = df[(df.harvey > 0) & (df.cherief > 0) & ~df.final]
    ax.scatter(agree_x.harvey, agree_x.cherief, s=175, facecolor="white",
               edgecolor=RED, linewidths=2.4, zorder=4,
               label="same direction, below rank cutoff")
    agree = df[df.final]
    ax.scatter(agree.harvey, agree.cherief, s=215, color=RED, alpha=0.92,
               edgecolor="white", linewidths=1.8, zorder=5,
               label="replicates as T-FAP-associated")

    # Name only the regulons that anchor the program (Stage 6: Junb/Jund/Klf9
    # supply most fate-driver genes). Labelling all 15 crowds the quadrant and
    # the circuit diagram names them anyway.
    # The whole point of the figure: one quadrant fills, the other stays empty.
    # Built before the labels so adjustText can be told to route around them.
    callout = [
        ax.text(lim * 0.99, lim * 0.86, "15", ha="right", va="center",
                fontsize=46, fontweight="bold", color=RED, zorder=6),
        ax.text(lim * 0.99, lim * 0.56, "regulons\nreplicate as\nfibrotic",
                ha="right", va="center", fontsize=17, color=RED,
                linespacing=1.28, fontweight="bold", zorder=6),
    ]

    # Only the three regulons that anchor the program: at this aspect ratio the
    # upper-right corner is crowded, and fig4 names all twelve anyway.
    KEY = {"Junb", "Jund", "Klf9"}
    texts = [
        ax.text(r.harvey, r.cherief, r["name"], fontsize=19.5, fontweight="bold",
                color=RED, path_effects=halo(4.5), zorder=7)
        for _, r in agree.iterrows() if r["name"] in KEY
    ]
    adjust_text(texts, ax=ax, objects=callout, expand=(1.3, 1.6),
                force_text=(0.4, 0.6), only_move={"text": "xy"},
                arrowprops=dict(arrowstyle="-", color=RED, lw=1.3, alpha=0.75))

    ax.text(-lim * 0.55, -lim * 0.34, "0", ha="center", va="center", fontsize=46,
            fontweight="bold", color=BLUE, zorder=6)
    ax.text(-lim * 0.55, -lim * 0.62, "replicate as\nregenerative",
            ha="center", va="center", fontsize=17, color=BLUE, linespacing=1.28,
            fontweight="bold", zorder=6)
    ax.text(-lim * 0.55, -lim * 0.85, "nothing lands in this quadrant",
            ha="center", va="center", fontsize=15, color=BLUE,
            style="italic", zorder=6)

    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_xlabel("Harvey 2019    ← TSPC      T-FAP →", fontsize=19.5)
    ax.set_ylabel("Cherief 2023    ← TSPC      T-FAP →", fontsize=19.5)
    for s in ("left", "bottom"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=4)
    leg = ax.legend(loc="lower right", frameon=False, fontsize=15.2,
                    scatterpoints=1, handletextpad=0.5, labelspacing=0.75,
                    borderpad=0.2)
    for t in leg.get_texts():
        t.set_color(INK_2)
    save(fig, OUT / "fig3_regulon_scatter.png")


# --------------------------------------------------------------------------
def fig4_circuit():
    """Upstream signal family -> TF regulon -> fibrotic fate program.
    Edge weight is the number of CellRank fate-driver genes each regulon
    contributes, so the diagram shows which TFs actually carry the program."""
    syn = pd.read_csv(ROOT / "data/mechanistic_synthesis/tf_signal_target_synthesis.csv")
    syn = syn[syn.n_cellrank_drivers > 0].copy()          # 12 of 15; 3 contribute none
    order = {"AP-1": 0, "KLF": 1, "NF-kB/Inflammatory": 2}
    syn["fo"] = syn.family.map(order)
    syn = syn.sort_values(["fo", "n_cellrank_drivers"], ascending=[True, False])

    # Three family columns rather than one tall stack of twelve: the poster
    # column is wide and short, and a 12-row stack renders too small to read.
    groups = [
        ("AP-1", "AP-1", "TGFβ / PDGF"),
        ("KLF", "KLF", "Mechanotransduction"),
        ("NF-kB/Inflammatory", "NF-κB / inflammatory", "TNF / IL-1 / Macrophage-Notch"),
    ]

    fig, ax = plt.subplots(figsize=(13.5, 6.3))
    ax.set_xlim(0, 13.5)
    ax.set_ylim(0, 6.3)
    ax.set_aspect("equal")          # keeps rounded corners circular, not oval
    ax.set_axis_off()

    mx = syn.n_cellrank_drivers.max()
    col_w, bar_max = 4.35, 2.00
    col_x = [0.25, 4.60, 8.95]
    y_top, step, ph = 4.78, 0.52, 0.42
    y_bar, bar_h = 0.62, 0.78          # the fate program spans the full width

    for (fam, fam_lab, sig), cx in zip(groups, col_x):
        rows = syn[syn.family == fam]
        col = FAMILY_COLORS[fam]
        ax.text(cx, 5.92, fam_lab, ha="left", va="center", fontsize=20.7,
                fontweight="bold", color=col)
        ax.text(cx, 5.48, sig, ha="left", va="center", fontsize=17.1,
                color=INK_2, style="italic")
        ax.plot([cx, cx + col_w - 0.30], [5.22, 5.22], color=col, lw=2.0, alpha=0.5)

        x_pill, pw = cx, 1.32
        for k, (_, r) in enumerate(rows.iterrows()):
            y = y_top - k * step
            ax.add_patch(FancyBboxPatch(
                (x_pill, y - ph / 2), pw, ph,
                boxstyle="round,pad=0,rounding_size=0.20",
                facecolor=col, edgecolor="white", lw=1.6, zorder=4))
            ax.text(x_pill + pw / 2, y, r.TF, ha="center", va="center",
                    fontsize=18.3, fontweight="bold", color="white", zorder=5)
            # Bar length encodes fate-driver count -- far easier to read at
            # poster distance than edge thickness.
            bl = bar_max * r.n_cellrank_drivers / mx
            ax.add_patch(FancyBboxPatch(
                (x_pill + pw + 0.16, y - 0.115), bl, 0.23,
                boxstyle="round,pad=0,rounding_size=0.10",
                facecolor=col, edgecolor="none", alpha=0.55, zorder=3))
            ax.text(x_pill + pw + 0.16 + bl + 0.16, y,
                    f"{int(r.n_cellrank_drivers)}", ha="left", va="center",
                    fontsize=17.1, fontweight="bold", color=col, zorder=5)

        # Short vertical drop into the fate bar; unequal lengths simply reflect
        # how many TFs each family contributes.
        y_last = y_top - (len(rows) - 1) * step
        ax.annotate("", xy=(cx + 1.55, y_bar + bar_h + 0.06),
                    xytext=(cx + 1.55, y_last - 0.36),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=2.8,
                                    alpha=0.6, shrinkA=0, shrinkB=0))

    ax.add_patch(FancyBboxPatch(
        (0.25, y_bar), 13.0, bar_h,
        boxstyle="round,pad=0,rounding_size=0.24",
        facecolor=RED, edgecolor="white", lw=2.0, zorder=4))
    ax.text(6.75, y_bar + bar_h / 2, "T-FAP  fibrotic  program", ha="center",
            va="center", fontsize=23.2, fontweight="bold", color="white", zorder=5)
    # The signal-to-TF-family links are bridged from the literature, not tested
    # in this project (progress.md, Stage 6 caveat) -- say so on the figure.
    ax.text(6.75, 0.16, "bar length = CellRank fate-driver genes contributed    ·    "
                        "italic = upstream signal inferred from literature, not tested here",
            ha="center", va="top", fontsize=15.5, color=INK_2, style="italic")
    save(fig, OUT / "fig4_circuit.png")


# --------------------------------------------------------------------------
def fig5_venn():
    """Three feature-selection methods with different modelling assumptions,
    and the 23 genes all three agree on."""
    g = pd.read_csv(ROOT / "data/feature_selection/gene_selection_by_method.csv")
    L, B, X = g.LASSO, g.Boruta, g.XGBoost
    r = {
        "L": int((L & ~B & ~X).sum()), "B": int((~L & B & ~X).sum()),
        "X": int((~L & ~B & X).sum()), "LB": int((L & B & ~X).sum()),
        "LX": int((L & ~B & X).sum()), "BX": int((~L & B & X).sum()),
        "LBX": int((L & B & X).sum()), "none": int((~L & ~B & ~X).sum()),
    }
    print(f"  [fig5] regions {r} | totals L={int(L.sum())} B={int(B.sum())} X={int(X.sum())}")

    fig, ax = plt.subplots(figsize=(6.65, 6.6))
    ax.set_xlim(-1.75, 1.75)
    ax.set_ylim(-1.62, 1.88)
    ax.set_aspect("equal")
    ax.set_axis_off()

    R = 0.86
    cen = {"L": (0.0, 0.50), "B": (-0.50, -0.36), "X": (0.50, -0.36)}
    # Boruta was a second blue, which collides with BLUE now that blue carries
    # semantic weight; violet keeps the three circles separable.
    col = {"L": BLUE, "B": "#7B4F9E", "X": GOLD}
    name = {"L": "LASSO", "B": "Boruta", "X": "XGBoost"}
    tot = {"L": int(L.sum()), "B": int(B.sum()), "X": int(X.sum())}

    for k, (cx, cy) in cen.items():
        ax.add_patch(Circle((cx, cy), R, facecolor=col[k], alpha=0.19,
                            edgecolor=col[k], lw=3.0, zorder=2))

    lab = {
        "L": (0.0, 1.06), "B": (-1.02, -0.72), "X": (1.02, -0.72),
        "LB": (-0.60, 0.36), "LX": (0.60, 0.36), "BX": (0.0, -0.74),
    }
    for k, (x, y) in lab.items():
        ax.text(x, y, str(r[k]), ha="center", va="center", fontsize=25.6,
                color=INK_2, zorder=5)

    # The unanimous core is the deliverable, so it gets the visual weight. Kept
    # neutral ink rather than red: the panel classifies both fates, and red is
    # reserved for "fibrotic" everywhere else on the poster.
    ax.add_patch(Circle((0.0, -0.08), 0.335, facecolor=INK, edgecolor="white",
                        lw=2.5, zorder=6))
    ax.text(0.0, -0.02, str(r["LBX"]), ha="center", va="center", fontsize=37.8,
            fontweight="bold", color="white", zorder=7)
    ax.text(0.0, -0.235, "genes", ha="center", va="center", fontsize=15.2,
            color="white", zorder=7)

    title_pos = {"L": (0.0, 1.60), "B": (-1.30, -1.28), "X": (1.30, -1.28)}
    for k, (x, y) in title_pos.items():
        ax.text(x, y, f"{name[k]}\n{tot[k]} genes", ha="center", va="center",
                fontsize=22, fontweight="bold", color=col[k], linespacing=1.25)

    ax.text(0, -1.58, f"from {len(g)} mechanism-derived candidates  "
                      f"·  {r['none']} selected by none",
            ha="center", va="center", fontsize=16.5, color=INK_2, style="italic")
    save(fig, OUT / "fig5_venn.png")


# --------------------------------------------------------------------------
def fig6_roc():
    """In-dataset cross-validation vs. the genuinely held-out test. The second
    curve is the one that matters: Cherief's labels were assigned independently
    and never seen during feature selection or training."""
    import anndata as ad
    import joblib
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import StratifiedKFold
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import roc_curve, roc_auc_score

    bundle = joblib.load(ROOT / "data/classifier/classifier_core_23.joblib")
    genes = list(bundle["genes"])

    # Harvey: reproduce the 10-fold CV to obtain out-of-fold scores for a curve.
    a = ad.read_h5ad(ROOT / "data/Harvey_scRNA-seq/harvey2019_processed.h5ad")
    m = a.obs.cell_type.isin(["TSPC", "T-FAP"]).values
    sub = a[m, genes]
    Xh = np.asarray(sub.X.todense() if hasattr(sub.X, "todense") else sub.X)
    yh = (sub.obs.cell_type.values == "T-FAP").astype(int)

    oof = np.zeros(len(yh))
    for tr, te in StratifiedKFold(10, shuffle=True, random_state=0).split(Xh, yh):
        sc = StandardScaler().fit(Xh[tr])
        clf = LogisticRegression(max_iter=2000, class_weight="balanced")
        clf.fit(sc.transform(Xh[tr]), yh[tr])
        oof[te] = clf.predict_proba(sc.transform(Xh[te]))[:, 1]
    auc_h = roc_auc_score(yh, oof)

    # Cherief: scores already produced by the Harvey-trained model.
    ch = pd.read_csv(ROOT / "data/classifier/cherief_healing_index_scores.csv", index_col=0)
    ch = ch[ch.cell_type.isin(["TSPC", "T-FAP"])]
    yc = (ch.cell_type.values == "T-FAP").astype(int)
    auc_c = roc_auc_score(yc, ch.core_23.values)
    print(f"  [fig6] Harvey 10-fold CV AUC {auc_h:.3f} | Cherief held-out AUC {auc_c:.3f}")

    fig, ax = plt.subplots(figsize=(6.65, 6.3))
    ax.plot([0, 1], [0, 1], color=GREY, lw=1.6, ls=(0, (4, 4)), zorder=1)
    fh, th, _ = roc_curve(yh, oof)
    fc, tc, _ = roc_curve(yc, ch.core_23.values)
    ax.plot(fh, th, color=GREY, lw=4.0, zorder=3,
            label=f"Harvey 2019, 10-fold CV\n(in-dataset)  AUC {auc_h:.3f}")
    ax.plot(fc, tc, color=RED, lw=5.0, zorder=4,
            label=f"Cherief 2023, held out\n(independent labels)  AUC {auc_c:.3f}")
    ax.set_xlabel("False positive rate", fontsize=18.3)
    ax.set_ylabel("True positive rate", fontsize=18.3)
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    ax.set_xticks([0, 0.5, 1.0])
    ax.set_yticks([0, 0.5, 1.0])

    # Carries the headline number, so the poster needs no separate metric tile.
    ax.text(0.97, 0.60, f"{auc_c:.3f}", ha="right", va="center", fontsize=46,
            fontweight="bold", color=RED)
    ax.text(0.97, 0.47, "held-out ROC-AUC", ha="right", va="center",
            fontsize=17, color=RED, fontweight="bold")
    leg = ax.legend(loc="lower right", frameon=False, fontsize=15.2,
                    handlelength=1.5, labelspacing=0.9, borderpad=0.2)
    for t in leg.get_texts():
        t.set_linespacing(1.25)
    save(fig, OUT / "fig6_roc.png")


# --------------------------------------------------------------------------
def fig7_healing_index():
    """The score itself: distribution by innervation status, and by the cell
    identities it was never trained to rank."""
    from scipy.stats import gaussian_kde
    hi = pd.read_csv(ROOT / "data/healing_index/cherief_healing_index.csv", index_col=0)

    fig, axes = plt.subplots(1, 2, figsize=(13.5, 6.2), width_ratios=[1.05, 1.0])

    # -- left: the two conditions as a ridgeline. Overlaying them muddies the
    # fills, and the point is that the whole distribution slides down.
    ax = axes[0]
    grid = np.linspace(0, 100, 400)
    base = {"Innervated": 1.15, "Denervated": 0.0}
    for cond in ["Innervated", "Denervated"]:
        v = hi.loc[hi.condition == cond, "healing_index"].values
        d = gaussian_kde(v, bw_method=0.28)(grid)
        d = d / d.max()
        b = base[cond]
        ax.fill_between(grid, b, b + d, color=COND_COLORS[cond], alpha=0.30, zorder=2)
        ax.plot(grid, b + d, color=COND_COLORS[cond], lw=4.0, zorder=3)
        ax.plot([0, 100], [b, b], color=COND_COLORS[cond], lw=1.4, alpha=0.55, zorder=2)
        mean = v.mean()
        # Stop the mean line at the curve so it reads as a marker on the
        # distribution rather than a stray tick above it.
        top = b + float(np.interp(mean, grid, d))
        ax.plot([mean, mean], [b, top], color="white", lw=4.2, zorder=4)
        ax.plot([mean, mean], [b, top], color=COND_COLORS[cond], lw=2.4,
                ls=(0, (3, 2.5)), zorder=5)
        ax.scatter([mean], [b], s=115, color=COND_COLORS[cond], zorder=6,
                   edgecolor="white", linewidths=1.7)
        ax.text(mean + 5.0, b + 0.78, f"{cond}\nmean {mean:.1f}", fontsize=18.9,
                fontweight="bold", color=COND_COLORS[cond], va="center",
                linespacing=1.25, zorder=7)
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.06, 2.32)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("Healing Index   (0–100, higher = regenerative)", fontsize=18.3)

    # -- right: by sub-population, ordered by median
    ax = axes[1]
    order = ["TSPC", "Stromal", "Tenogenic-progenitor", "T-FAP"]
    rng = np.random.default_rng(1)
    for i, ct in enumerate(order):
        v = hi.loc[hi.cell_type == ct, "healing_index"].values
        y = len(order) - 1 - i
        emph = ct in ("TSPC", "T-FAP")
        ax.scatter(v, y + rng.uniform(-0.20, 0.20, len(v)), s=7,
                   color=CELL_COLORS[ct], alpha=0.30 if emph else 0.42,
                   linewidths=0, zorder=2)
        bp = ax.boxplot([v], positions=[y], orientation="horizontal", widths=0.46,
                        showfliers=False, patch_artist=True, zorder=4)
        for box in bp["boxes"]:
            box.set(facecolor="white", edgecolor=CELL_COLORS[ct], linewidth=2.6, alpha=0.95)
        for el in ("whiskers", "caps", "medians"):
            for it in bp[el]:
                it.set(color=CELL_COLORS[ct], linewidth=2.6)
        ax.text(103, y, f"{np.mean(v):.1f}", va="center", ha="left", fontsize=18.9,
                fontweight="bold", color=CELL_COLORS[ct] if emph else INK_2)
    ax.text(103, len(order) - 0.42, "mean", va="center", ha="left", fontsize=15.9,
            color=INK_2, style="italic")
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels(order[::-1], fontsize=18.3)
    for tick, ct in zip(ax.get_yticklabels(), order[::-1]):
        tick.set_color(CELL_COLORS[ct] if ct in ("TSPC", "T-FAP") else INK_2)
        if ct in ("TSPC", "T-FAP"):
            tick.set_fontweight("bold")
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.62, len(order) - 0.30)
    ax.set_xlabel("Healing Index", fontsize=18.3)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.subplots_adjust(wspace=0.46)
    save(fig, OUT / "fig7_healing_index.png")


if __name__ == "__main__":
    apply_style()
    print("Building poster figures ->", OUT)
    for fn in (fig1_umap, fig2_shift, fig3_regulon_scatter, fig4_circuit,
               fig5_venn, fig6_roc, fig7_healing_index):
        fn()
    print("done")
