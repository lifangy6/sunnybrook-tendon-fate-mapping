# Project Progress

**Project:** A Mechanism-Informed Gene Signature for Regenerative vs. Fibrotic Tendon Healing  
**Last updated:** 2026-06-05

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
| 3a | pySCENIC — TF network inference on TSPC / T-FAP | Not started |
| 3b | Label transfer Harvey 2019 → Cherief 2023 cluster 8 | Not started |
| 4 | CellRank — fate trajectory from PDGFRα+ progenitor | Not started |
| 5 | LIANA — cell-cell communication (innervated vs. denervated) | Not started |
| 6 | Mechanistic summary (TF regulons + upstream signals) | Not started |
| 7 | Feature selection (LASSO + Boruta + XGBoost) | Not started |
| 8 | Classifier training & validation | Not started |
| 9 | Continuous healing index score | Not started |

---

## Done

### Project setup & literature
- Defined the two-arm project structure: mechanistic arm (TF networks) + applied arm (gene signature classifier)
- Reviewed key papers: Harvey 2019 (*Nat Cell Biol*), Cherief 2023 (*Sci Transl Med*), Howell 2017, Kaji 2020, Moser 2021
- Wrote research plan (`docs/research-plan.md`) and project rubric materials

### Cherief 2023 scRNA-seq — initial processing (`scripts/ipynb/01_explore_GSE244921.ipynb`)
- Downloaded GSE244921 from GEO; stored at `data/Cherief_scRNA-seq/GSE244921_processed.h5ad`
- QC: filtered low-quality cells; retained **22,615 cells**
- Ran PCA → UMAP → Leiden clustering (resolution = 0.5); identified 8 clusters
- Annotated clusters by marker expression: tenocytes (Scx+, Tnmd+), macrophage subtypes (clusters 0, 1, 2, 13), PDGFRα+ stromal population (cluster 8)
- Confirmed clear condition separation between innervated and denervated cells on UMAP
- Produced: `figures/Cherief_scRNA-seq/umap_clusters.png`, `umap_condition.png`, `umap_markers.png`, `dotplot__markers.png`, QC plots

### Cluster 8 sub-clustering — TSPC / T-FAP separation (`scripts/ipynb/02_subcluster_cluster8.ipynb`)
- Swept Leiden resolutions (0.8–1.5) on cluster 8 cells only → `umap_sub8_resolution_sweep.png`
- Selected optimal resolution; confirmed TSPC sub-cluster (Tppp3+) and T-FAP sub-cluster (Pdgfra+/Tppp3−)
- Ran differential expression between TSPC and T-FAP sub-clusters
- Checked condition (innervated vs. denervated) proportions across sub-clusters → `sub8_condition_proportions.png`
- Produced: `umap_sub8_annotated.png`, `umap_sub8_chosen.png`, `umap_sub8_condition.png`, `umap_sub8_gene_overlays.png`, `dotplot__sub8_markers.png`, `dotplot__sub8_top_degs.png`, `umap_sub8_sanity.png`

### Harvey 2019 — download, Cell Ranger & QC (`scripts/ipynb/03_harvey2019_qc_clustering.ipynb`)

- Downloaded SRR9087252 FASTQs (~23.2 GB) from SRA on HPC cluster via `scripts/sh/download_harvey.sh` / `fasterq_harvey.sh`
- Ran Cell Ranger 10 `count` against mm10 reference on HPC (64 GB RAM, 16 cores, ~12 h) via `scripts/sh/cellranger_harvey.sh`; Cell Ranger estimated **8,484 cells**
- QC-filtered to biologically relevant population: min 700 genes, <15% MT reads, <5,000 genes → reduced to ~2,491 cells, matching Harvey 2019 paper
- Normalized (scran 10k), log-transformed, selected 2,000 HVGs, PCA → UMAP → Leiden clustering (resolution = 0.5)
- Plotted key fate markers: Tppp3, Pi16, Sfrp2, Pdgfra, Tnmd, Scx; produced dotplot and per-cluster mean expression table to guide TSPC/T-FAP annotation
- Saved processed object: `data/Harvey_scRNA-seq/harvey2019_processed.h5ad`
- **Pending:** fill in `cluster_annotation` dict in notebook section 8 after inspecting marker dotplot outputs

### Other outputs
- Pipeline flowchart (`figures/pipeline_flowchart.png`) drawn via `scripts/draw_pipeline.py`

---

## Next Steps (in order)

1. **Finish Harvey 2019 cluster annotation** (notebook section 8)
   - Inspect marker dotplot and `cluster_means` output
   - Fill in `cluster_annotation` dict to label TSPC, T-FAP, tenocyte, etc.
   - Re-run notebook to save annotated `cell_type` column to `harvey2019_processed.h5ad`

2. **Stage 3a — pySCENIC on Cherief 2023 sub-clusters**
   - Run pySCENIC on the TSPC and T-FAP sub-clusters already identified in cluster 8
   - Requires ≥300–500 cells per population — verify counts first
   - Output: ranked TF regulons specific to each fate

3. **Stage 3b — Label transfer Harvey 2019 → Cherief 2023 cluster 8**
   - Transfer Harvey 2019 TSPC/T-FAP labels onto Cherief 2023 cluster 8 sub-clusters using Seurat/scVI
   - Use as secondary confirmation of sub-cluster identities

4. **Stage 4 — CellRank fate trajectory**
   - Model pseudotime from PDGFRα+ progenitor → TSPC vs. T-FAP terminal states
   - Identify driver genes along each fate branch
   - Cross-reference with pySCENIC regulons to find TFs active at the fate branch point

5. **Stage 5 — LIANA cell-cell communication**
   - Compare ligand-receptor interactions in innervated vs. denervated conditions
   - Focus on NGF, TGFβ, PDGF signaling axes

6. **Stage 6 — Mechanistic synthesis**
   - Integrate pySCENIC regulons + CellRank branch drivers + LIANA signals
   - Write up regulatory circuit: what TFs govern each fate, what upstream signals activate them, how denervation disrupts balance

7. **Stage 7 — Feature selection**
   - Use pySCENIC gene sets + CellRank driver genes as candidate feature space
   - Apply LASSO, Boruta, XGBoost; take intersection of ≥2 methods

8. **Stage 8 — Classifier training & validation**
   - Train on Harvey 2019 TSPC/T-FAP; validate on Cherief 2023 innervated vs. denervated

9. **Stage 9 — Healing index score**
   - Convert classifier to continuous score; apply to new tendon scRNA-seq datasets

---

## Key Files

| File | Purpose |
|---|---|
| `data/Cherief_scRNA-seq/GSE244921_processed.h5ad` | Processed Cherief 2023 AnnData object |
| `data/Harvey_scRNA-seq/harvey2019_processed.h5ad` | Processed Harvey 2019 AnnData object |
| `scripts/ipynb/01_cherief2023_qc_clustering.ipynb` | Cherief 2023 — QC, clustering, annotation |
| `scripts/ipynb/02_cherief2023_subcluster_tspc_tfap.ipynb` | Cluster 8 sub-clustering → TSPC/T-FAP |
| `scripts/ipynb/03_harvey2019_qc_clustering.ipynb` | Harvey 2019 — QC, clustering, marker annotation |
| `scripts/sh/download_harvey.sh` | SRA prefetch of SRR9087252 FASTQs (HPC) |
| `scripts/sh/fasterq_harvey.sh` | fasterq-dump + gzip of Harvey FASTQs (HPC) |
| `scripts/sh/cellranger_harvey.sh` | Cell Ranger count job on HPC (mm10, 16 cores) |
| `scripts/py/draw_pipeline.py` | Pipeline flowchart generation |
| `scripts/js/create_proposal_docx.js` | Proposal Word document generation |
| `figures/Cherief_scRNA-seq/` | All Cherief 2023 analysis figures |
| `figures/Harvey_scRNA-seq/` | Harvey 2019 QC and clustering figures |
| `figures/pipeline_flowchart.png` | Full analysis pipeline diagram |
| `docs/research-plan.md` | Detailed scientific rationale and pipeline |
