# Project Progress

**Project:** A Mechanism-Informed Gene Signature for Regenerative vs. Fibrotic Tendon Healing  
**Last updated:** 2026-06-29

---

## Status at a Glance

| Stage | Task | Status |
|---|---|---|
| 0 | Define project scope & research questions | Done ✓ |
| 0 | Literature review (Harvey, Cherief, Howell, Kaji, Moser) | Done ✓ |
| 1a | Download & QC Cherief 2023 scRNA-seq (GSE244921) | Done ✓ |
| 1b | Clustering & cell-type annotation (Cherief 2023) | Done ✓ |
| 1c | Sub-cluster cluster 8 → TSPC / T-FAP separation | Done ✓ |
| 2 | Obtain Harvey 2019 count matrix (Cell Ranger on FASTQs) | Done ✓ |
| 3a | pySCENIC — TF network inference on TSPC / T-FAP | Done ✓ |
| 3b | Label transfer Harvey 2019 → Cherief 2023 cluster 8 | On hold |
| 4 | CellRank — fate trajectory from PDGFRα+ progenitor | Done ✓ (pseudotime caveat) |
| 5 | LIANA — cell-cell communication (innervated vs. denervated) | Done ✓ |
| 6 | Mechanistic summary (TF regulons + upstream signals) | Not started ← next |
| 7 | Feature selection (LASSO + Boruta + XGBoost) | Not started |
| 8 | Classifier training & validation | Not started |
| 9 | Continuous healing index score | Not started |

---

## Stage 0 — Project Setup & Literature ✓

**Goal:** Define the two-arm project structure and establish biological context from key papers.

Two linked arms:
- **Mechanistic arm** — identify TF networks and upstream signals governing the TSPC vs. T-FAP fate decision
- **Applied arm** — compress mechanism-derived gene programs into a minimal classifier (~10–30 genes) for regenerative vs. fibrotic tendon healing

Key papers reviewed: Harvey 2019 (*Nat Cell Biol*) — defines TSPC/T-FAP; Cherief 2023 (*Sci Transl Med*) — innervation/denervation control of healing; Howell 2017, Kaji 2020, Moser 2021 — supporting context on TGFβ, ECM remodelling, and progenitor biology.

---

## Stage 1 — Cherief 2023 scRNA-seq Processing ✓

**Dataset:** GSE244921 — mouse Achilles tendon, day 14 post-injury, innervated (TrkAWT) vs. denervated (TrkAF592A).  
**Scripts:** `scripts/ipynb/01_cherief2023_qc_clustering.ipynb`, `02_cherief2023_subcluster_tspc_tfap.ipynb`

### 1a/1b — QC, clustering & annotation (22,615 cells)

QC filters removed low-quality cells; 22,615 cells retained. Leiden clustering (resolution 0.5) produced 17 clusters annotated by marker expression. The PDGFRα+ stromal population (cluster 8, 3,900 cells) is the focal population — it contains TSPCs and T-FAPs mixed together.

![Cherief 2023 — UMAP coloured by marker genes](../figures/Cherief_scRNA-seq/umap_markers.png)

### 1c — Sub-clustering cluster 8: TSPC / T-FAP separation

Higher-resolution Leiden (resolution sweep 0.8–1.5) restricted to cluster 8 resolved four sub-populations:

| Sub-cluster | Label | n cells | Key markers |
|---|---|---|---|
| 0 | Stromal | 1,388 | Plagl1, Mest, H19 (imprinted gene signature) |
| 1 | T-FAP | 1,245 | Pi16=1.63, Sfrp2=1.35, Pdgfra=1.48; complement (C3, C4b) |
| 2 | Tenogenic-progenitor | 816 | Thbs4, Kera, Col11a1 |
| 3 | TSPC | 451 | Tppp3=1.76, Prg4 co-elevated; Sfrp2 near-absent |

TSPC are **2.4× enriched in innervated**; T-FAP are **1.46× enriched in denervated** — consistent with the paper's claim that innervation supports regenerative progenitor expansion.

![Sub-cluster marker gene overlays](../figures/Cherief_scRNA-seq/umap_sub8_gene_overlays.png)

![Condition proportions across sub-clusters](../figures/Cherief_scRNA-seq/sub8_condition_proportions.png)

---

## Stage 2 — Harvey 2019 Count Matrix ✓

**Dataset:** PRJNA506218 / SRR9087252 — mouse patellar tendon, uninjured adult.  
**Script:** `scripts/ipynb/03_harvey2019_qc_clustering.ipynb`; Cell Ranger job: `scripts/sh/cellranger_harvey.sh`

Raw FASTQs (23.2 GB) downloaded from SRA on HPC, aligned with Cell Ranger 10 against mm10. After QC filtering (min 700 genes, <15% MT, <5,000 genes), **4,069 cells** retained across 12 clusters. TSPC (Tppp3+, clusters 2 & 8) and T-FAP (Ly6a+/Pi16+, clusters 3 & 11) annotated by marker expression and validated with Wilcoxon DEG analysis.

Harvey 2019 provides ground-truth TSPC/T-FAP labels for both pySCENIC input and future classifier training — it is the only dataset where both populations are explicitly characterised in an uninjured, homeostatic context.

![Harvey 2019 — annotated UMAP](../figures/Harvey_scRNA-seq/umap_annotated.png)

---

## Stage 3A — pySCENIC TF Network Inference ✓

**Goal:** Identify transcription factor regulons enriched in TSPC vs. T-FAP in both datasets independently, then find cross-dataset consistent TFs.  
**Scripts:** `scripts/sh/pyscenic_*.sh` (HPC), `scripts/ipynb/04_pyscenic_analysis.ipynb`

Pipeline run on Alliance Canada HPC (NIBI): GRNBoost2 → cisTarget motif pruning → AUCell scoring. Produced **471 Harvey** and **417 Cherief** regulons. AUCell scores compared between TSPC and T-FAP by Wilcoxon test; cross-dataset direction filter retained only regulons with positive Wilcoxon score in both datasets.

**Result: 15 T-FAP regulons consistent across both datasets; 0 TSPC regulons.**

| Group | Regulons |
|---|---|
| AP-1 family | Fos, Fosb, Jun, Junb, Jund, Atf3 |
| KLF family | Klf6, Klf9 |
| Inflammatory TFs | Nfkb1, Irf1, Egr1, Cebpd |
| Other | Pbx1, Prdm16, Zfp369 |

These form a coherent **pro-fibrotic / activated-fibroblast** program. TSPC-specific TFs in Harvey (E2f1, Fli1, Arnt2 — cell cycle / ETS / progenitor programs) are reversed or absent in injured Cherief tendons, reflecting the homeostatic vs. post-injury context difference.

![Regulon activity heatmap — Harvey](../figures/pyscenic/matrixplot__heatmap_harvey.png)

![Regulon activity heatmap — Cherief](../figures/pyscenic/matrixplot__heatmap_cherief.png)

**Implication for classifier:** T-FAP regulon AUC scores as positive fibrotic features; TSPC identified by expression markers (Tppp3, Prg4) since consistent TF regulons are absent.

---

## Stage 3B — Label Transfer (On Hold)

**Plan:** Transfer Harvey 2019 TSPC/T-FAP labels onto Cherief 2023 cluster 8 via Seurat/scVI to provide independent confirmation of sub-cluster identities.

**Status:** Not urgently needed — sub-cluster identities are already well-supported by marker expression and pySCENIC regulon profiles. Can be done later as a validation step.

---

## Stage 4 — CellRank Fate Trajectory ✓ (with caveats)

**Dataset:** Cherief 2023 cluster 8 sub-clustered AnnData (3,900 cells).  
**Script:** `scripts/ipynb/05_cellrank_fate_trajectory.ipynb`

**Approach:** CellRank 2 PseudotimeKernel (DPT, no RNA velocity — Cherief GEO deposit has no spliced/unspliced counts). Root = Stromal sub-cluster (min DC1). GPCCA with n_states=5 recovered all four cell types as distinct macrostates.

**Caveat — pseudotime ordering:** DPT ranked Tenogenic-progenitor as most progenitor-like (mean DPT 0.18) rather than Stromal (0.29), which is biologically incorrect: Stromal has the imprinted gene signature (Plagl1, Mest, H19) marking undifferentiated state. The DPT is rooted at Stromal but diffusion components place Tenogenic-progenitor cells close to the root in PC space. This makes trajectory ordering unreliable; fate probabilities are still interpretable as a soft classification rather than a mechanistic trajectory.

**Fate probabilities by condition:**

| Condition | TSPC | T-FAP (total) |
|---|---|---|
| Innervated (TrkAWT) | 0.826 | 0.172 |
| Denervated (TrkAF592A) | 0.710 | 0.289 |

Direction is consistent with LIANA: denervation shifts progenitor fate allocation toward T-FAP.

**Top lineage driver genes:**

| Fate | Top drivers (by correlation) |
|---|---|
| TSPC | Igfbp6, Sema3c, Cd55, Crip1, Axl, S100a10, Emp3, Cd34, Tppp3 |
| T-FAP_1 | Gdf10, Fmo2, Abcc9, Ccl11, Il6, C2, Steap4, Junb |
| T-FAP_2 | Cxcl14, Hp, Gas6, Sfrp1, Angptl4, Cxcl12, C3, Sfrp2, Hif1a |

T-FAP_2 drivers (Sfrp1/2, C3, Hif1a) overlap strongly with the complement/hypoxia signature seen in DEG analysis. TSPC drivers include Sema3c, consistent with LIANA finding that attractive semaphorins are enriched in the innervated niche.

**pySCENIC × CellRank overlap** (`data/cellrank/pyscenic_cellrank_tfap_overlap.csv`): 119 genes are both CellRank T-FAP lineage drivers (top 200, union of T-FAP_1 and T-FAP_2) and targets of one or more of the 15 consistent pySCENIC T-FAP regulons. Top genes: Gdf10 (Junb/Klf9), Il6 (Junb), Steap4 (Egr1/Junb), Angptl4 (Junb), Sfrp1 (Fosb), C3 (Junb), Sfrp2 (Jun), Vcam1 (Nfkb1). Most are targets of AP-1 (Junb/Jund/Fos) and KLF (Klf9/Klf6) regulons — consistent with the pySCENIC result. These 119 genes form the mechanism-informed candidate feature set for Stage 7.

---

## Stage 5 — LIANA Cell-Cell Communication ✓

**Goal:** Identify which ligand-receptor signals arriving at TSPC and T-FAP differ between innervated and denervated conditions.  
**Script:** `scripts/ipynb/06_liana_cellcell_communication.ipynb`

`rank_aggregate` (6 methods — CellPhoneDB, Connectome, log2FC, NATMI, SingleCellSignalR, CellChat; mouse consensus LR database) run separately on innervated (11,478 cells) and denervated (8,569 cells) subsets of the full annotated dataset. Differential metric: **`delta_rank = rank_denervated − rank_innervated`** (positive = stronger in innervated; negative = stronger in denervated).

52,646 LR pairs detected in both conditions; 11,669 with TSPC or T-FAP as receiver.

![Differential LR interactions at TSPC/T-FAP](../figures/liana/barplot_differential_stromal.png)

**Signals STRONGER in innervated (positive delta_rank — lost upon denervation):**

| Signal | Sender → Receiver | delta_rank | Interpretation |
|---|---|---|---|
| Efna1 → Epha3 | Stromal_other → T-FAP | +0.94 | Strongest differential signal overall; ephrin-A/EphA3 at T-FAPs in innervated niche |
| Sema4a → Plxnd1 | Stromal_other → T-FAP | +0.86 | Class 4 semaphorin — repulsive axon guidance cue present in innervated niche |
| Bmp3 → Bmpr1b | TSPC → TSPC | +0.79 | Anti-fibrotic autocrine BMP signalling |
| Sema3d → Nrp/Plxna | Multiple → T-FAP | +0.80–0.88 | Attractive class 3 semaphorin; strongest at T-FAP via Nrp1/2_Plxna2 |
| Wnt5a → Fzd4 | Smooth_muscle → TSPC | +0.75 | Non-canonical Wnt progenitor maintenance |
| Sema3c → Nrp2_Plxna1 | Tenogenic-progenitor → TSPC | +0.74 | Attractive semaphorin at TSPC; same ligand acts oppositely at T-FAP (see denervated) |
| Pdgfc → Pdgfra | Stromal → TSPC | +0.71 | Strongest growth-factor signal lost at TSPCs; innervation maintains stromal PDGF-C |
| Tgfb1/3 → Itgb3 | Endothelial, Tenocyte → T-FAP | +0.52–0.66 | TGFβ-integrin signalling at T-FAPs is higher in innervated — likely controlled matrix remodelling rather than pathological fibrosis |
| Bdnf/Ngf → Erbb2 | Multiple → TSPC | +0.26–0.43 | Neurotrophin-receptor axis confirming direct innervation-dependent signalling |

**Signals STRONGER in denervated (negative delta_rank — gained upon denervation):**

| Signal | Sender → Receiver | delta_rank | Interpretation |
|---|---|---|---|
| Sema3f → Nrp2_Plxna1 | TSPC → TSPC | −0.82 | Repulsive semaphorin — autocrine TSPC suppression |
| Tnf → Notch1 | Macrophage → TSPC | −0.74 | Inflammatory Notch activation reduces tenogenic differentiation |
| Sema3c → Nrp1_Nrp2_Plxnd1 | Multiple → T-FAP | −0.66 to −0.70 | Same ligand as innervated TSPC signal but different receptor complex; promotes T-FAP in denervated |
| Rtn4 → Rtn4rl1 | Multiple → TSPC | −0.70 to −0.73 | Nogo/axon-repulsion factor elevated without innervation |
| Lama4/Lamb1 → Itga9_Itgb1 | Multiple → T-FAP | −0.70 to −0.73 | Laminin-integrin ECM route driving T-FAP expansion |

Bubble plots below confirm the overall pattern: innervated niche signals are enriched at both TSPC (growth factors, Wnt, BMP, neurotrophin) and T-FAP (ephrin-A, Sema4a, Sema3d); denervated niche gains inflammatory (TNF-Notch), repulsive (Sema3f, Rtn4), and fibrotic matrix (laminin-integrin) signals.

![Top 25 interactions → TSPC / T-FAP (innervated)](../figures/liana/dotplot_innervated_stromal.png)

![Top 25 interactions → TSPC / T-FAP (denervated)](../figures/liana/dotplot_denervated_stromal.png)

---

## Stage 6 — Mechanistic Synthesis ← Next

**Goal:** Integrate pySCENIC TF regulons (Stage 3A), CellRank fate drivers (Stage 4), and LIANA upstream signals (Stage 5) into a single regulatory circuit explaining the TSPC vs. T-FAP fate decision.

Draft circuit:
- **Innervated → TSPC fate:** PDGF-C/Wnt5a/BMP3 niche signals (LIANA) → progenitor pool biased toward TSPC (CellRank: 82.6% TSPC fate probability) → suppression of AP-1/KLF/NF-κB TF program → Tppp3+/Igfbp6+/Sema3c+ TSPC maintenance
- **Denervated → T-FAP fate:** Loss of PDGF-C/Wnt5a; TNF → NF-κB (Nfkb1) + Macrophage-Notch suppresses TSPC; laminin-integrin (Lama4/Lamb1 → Itga9/Itgb1) + TGFβ → AP-1/ATF3/KLF activation (Klf6/Klf9/Cebpd/Irf1/Egr1 regulons) → T-FAP program (CellRank: T-FAP fate rises from 17% to 29%); T-FAP drivers Sfrp1/2 (Wnt antagonists), Hif1a (hypoxia), Il6 (JAK-STAT), C3 (complement) reinforce fibrotic identity

Additional threads from Stage 4:
- **Sema3c** is both a LIANA innervated signal (attractive semaphorin lost upon denervation) and a CellRank TSPC lineage driver — strongest cross-stage convergence point for TSPC maintenance
- **Sfrp1/2** appear as T-FAP_2 CellRank drivers and Fosb/Jun targets — Wnt antagonism as a T-FAP self-reinforcing mechanism
- **119-gene pySCENIC × CellRank overlap** (dominated by Junb/Jund/Klf9/Klf6 targets) represents the mechanism-informed candidate feature set for Stage 7

Signal-to-TF links are literature-bridged (TNF → NF-κB; TGFβ → AP-1/ATF3; PDGF → MEK/ERK → AP-1) — can be strengthened by querying GRNBoost2 adjacency tables from Stage 3A.

---

## Stage 7 — Feature Selection (Not Started)

Candidate feature space (ready): **119 genes** from the pySCENIC × CellRank T-FAP overlap (`data/cellrank/pyscenic_cellrank_tfap_overlap.csv`) plus TSPC marker genes (Tppp3, Prg4, Igfbp6, Sema3c, Cd34). Apply LASSO, Boruta, and XGBoost independently on Harvey 2019 TSPC/T-FAP clusters; take the intersection of genes selected by ≥2 methods. Target: minimal panel of ~10–30 genes.

---

## Stage 8 — Classifier Training & Validation (Not Started)

Train on Harvey 2019 TSPC/T-FAP clusters. Validate generalization on Cherief 2023 innervated vs. denervated — a well-calibrated classifier should shift toward the fibrotic end of the score distribution in denervated samples.

---

## Stage 9 — Continuous Healing Index Score (Not Started)

Convert binary classifier to a continuous score using predicted class probabilities. Apply to new tendon scRNA-seq datasets from the lab.

---

## Key Files

| File | Purpose |
|---|---|
| `data/Cherief_scRNA-seq/GSE244921_processed.h5ad` | Processed Cherief 2023 AnnData (22,615 cells) |
| `data/Cherief_scRNA-seq/GSE244921_cluster8_sub.h5ad` | Cluster 8 sub-clustered AnnData (TSPC/T-FAP/Tenogenic-progenitor/Stromal) |
| `data/Harvey_scRNA-seq/harvey2019_processed.h5ad` | Processed Harvey 2019 AnnData (4,069 cells) |
| `data/pyscenic/harvey_aucell.loom` | pySCENIC AUCell output — Harvey (471 regulons) |
| `data/pyscenic/cherief_aucell.loom` | pySCENIC AUCell output — Cherief (417 regulons) |
| `data/pyscenic/shared_diff_regulons.csv` | 15 cross-dataset T-FAP regulons (consistent direction) |
| `data/liana/liana_innervated.csv` | Full LIANA result — innervated (56,701 LR pairs) |
| `data/liana/liana_denervated.csv` | Full LIANA result — denervated (57,233 LR pairs) |
| `data/liana/liana_differential_stromal_receivers.csv` | Delta_rank filtered to TSPC/T-FAP receivers (11,669 pairs) |
| `data/cellrank/pyscenic_cellrank_tfap_overlap.csv` | 119-gene pySCENIC × CellRank T-FAP overlap — mechanism-informed feature candidates for Stage 7 |
| `data/cellrank/lineage_drivers_TSPC.csv` | CellRank TSPC lineage drivers (7,000 significant genes) |
| `data/cellrank/lineage_drivers_T-FAP_1.csv` | CellRank T-FAP_1 lineage drivers (7,223 significant genes) |
| `data/cellrank/lineage_drivers_T-FAP_2.csv` | CellRank T-FAP_2 lineage drivers (4,449 significant genes) |
| `data/Cherief_scRNA-seq/GSE244921_cluster8_cellrank.h5ad` | Cluster 8 AnnData with fate probabilities added (from CellRank) |
| `scripts/ipynb/01_cherief2023_qc_clustering.ipynb` | Cherief 2023 — QC, clustering, annotation |
| `scripts/ipynb/02_cherief2023_subcluster_tspc_tfap.ipynb` | Cluster 8 sub-clustering → TSPC/T-FAP |
| `scripts/ipynb/03_harvey2019_qc_clustering.ipynb` | Harvey 2019 — QC, clustering, marker annotation |
| `scripts/ipynb/04_pyscenic_analysis.ipynb` | pySCENIC AUCell analysis — UMAP, differential regulons, cross-dataset comparison |
| `scripts/ipynb/05_cellrank_fate_trajectory.ipynb` | CellRank fate trajectory — DPT, macrostates, fate probabilities, lineage drivers |
| `scripts/ipynb/06_liana_cellcell_communication.ipynb` | LIANA CCC — annotation, rank_aggregate, differential, visualisation |
| `scripts/sh/pyscenic_00_setup.sh` | HPC environment setup (patched pySCENIC 0.12.0) |
| `scripts/sh/pyscenic_03_grn.sh` | SLURM: GRNBoost2 TF-gene co-expression |
| `scripts/sh/pyscenic_04_ctx.sh` | SLURM: cisTarget motif pruning |
| `scripts/sh/pyscenic_05_aucell.sh` | SLURM: AUCell regulon scoring |
| `scripts/sh/cellranger_harvey.sh` | Cell Ranger count job on HPC (mm10, 16 cores) |
| `figures/Cherief_scRNA-seq/` | All Cherief 2023 analysis figures |
| `figures/Harvey_scRNA-seq/` | Harvey 2019 QC and clustering figures |
| `figures/pyscenic/` | pySCENIC regulon UMAP and heatmap figures |
| `figures/liana/` | LIANA differential and bubble plot figures |
| `figures/pipeline_flowchart.png` | Full analysis pipeline diagram |
| `docs/research-plan.md` | Detailed scientific rationale and pipeline |
