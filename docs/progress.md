# Project Progress

**Project:** A Mechanism-Informed Gene Signature for Regenerative vs. Fibrotic Tendon Healing  
**Last updated:** 2026-06-01

---

## Status at a Glance

| Stage | Task | Status |
|---|---|---|
| 0 | Define project scope & research questions | Done ✓ |
| 0 | Literature review (Harvey, Cherief, Howell, Kaji, Moser) | Done ✓ |
| 1a | Download & QC Cherief 2023 scRNA-seq (GSE244921) | Done ✓ |
| 1b | Clustering & cell-type annotation (Cherief 2023) | Done ✓ |
| 1c | Sub-cluster cluster 8 → TSPC / T-FAP separation | Done ✓ |
| 2 | Obtain Harvey 2019 count matrix (Cell Ranger on FASTQs) | **Blocked** |
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

### Harvey 2019 — preliminary exploration
- Inspected available Harvey 2019 data files via `scripts/inspect_harvey_rda.R`
- Confirmed count matrix is **not publicly deposited**; raw FASTQs exist under SRA accession PRJNA506218 / SRR9087252

### Other outputs
- Pipeline flowchart (`figures/pipeline_flowchart.png`) drawn via `scripts/draw_pipeline.py`

---

## Currently Blocked

### Stage 2 — Harvey 2019 Cell Ranger
**Blocker:** Cell Ranger requires Linux/WSL2, ~32–64 GB RAM, ~100 GB storage, ~4–8 hours compute. Cannot be run on Windows natively.

**What's needed to unblock:**
- Access to a Linux machine or WSL2 environment
- Download SRR9087252 FASTQs (~23.2 GB) via `fastq-dump` or `fasterq-dump`
- Run Cell Ranger `count` with mm10 reference genome
- Alternative: contact Harvey lab directly to request the count matrix

**Why it matters:** Harvey 2019 provides the only explicitly validated TSPC/T-FAP cluster labels — needed for pySCENIC TF inference (Stage 3a) and classifier training (Stage 8). Without it, both arms rely solely on the sub-clustered Cherief 2023 cluster 8.

---

## Next Steps (in order)

### Immediate — while Harvey 2019 is blocked

1. **Stage 3a — pySCENIC on Cherief 2023 sub-clusters**
   - Run pySCENIC on the TSPC and T-FAP sub-clusters already identified in cluster 8
   - Requires ≥300–500 cells per population — verify counts first
   - Output: ranked TF regulons specific to each fate

2. **Stage 4 — CellRank fate trajectory**
   - Model pseudotime from PDGFRα+ progenitor → TSPC vs. T-FAP terminal states
   - Identify driver genes along each fate branch
   - Cross-reference with pySCENIC regulons to find TFs active at the fate branch point

3. **Stage 5 — LIANA cell-cell communication**
   - Compare ligand-receptor interactions in innervated vs. denervated conditions
   - Focus on NGF, TGFβ, PDGF signaling axes

### Once Harvey 2019 is unblocked

4. **Stage 3b — Label transfer**
   - Transfer Harvey 2019 TSPC/T-FAP labels onto Cherief 2023 cluster 8 sub-clusters using Seurat/scVI
   - Use as secondary confirmation of sub-cluster identities

5. **Stage 6 — Mechanistic synthesis**
   - Integrate pySCENIC regulons + CellRank branch drivers + LIANA signals
   - Write up regulatory circuit: what TFs govern each fate, what upstream signals activate them, how denervation disrupts balance

### Final stages (depends on Stages 3–5)

6. **Stage 7 — Feature selection**
   - Use pySCENIC gene sets + CellRank driver genes as candidate feature space
   - Apply LASSO, Boruta, XGBoost; take intersection of ≥2 methods

7. **Stage 8 — Classifier training & validation**
   - Train on Harvey 2019 TSPC/T-FAP; validate on Cherief 2023 innervated vs. denervated

8. **Stage 9 — Healing index score**
   - Convert classifier to continuous score; apply to new tendon scRNA-seq datasets

---

## Key Files

| File | Purpose |
|---|---|
| `data/Cherief_scRNA-seq/GSE244921_processed.h5ad` | Processed Cherief 2023 AnnData object |
| `scripts/ipynb/01_explore_GSE244921.ipynb` | Initial QC, clustering, annotation |
| `scripts/ipynb/02_subcluster_cluster8.ipynb` | Cluster 8 sub-clustering → TSPC/T-FAP |
| `scripts/r/inspect_harvey_rda.R` | Harvey 2019 data inspection |
| `scripts/py/draw_pipeline.py` | Pipeline flowchart generation |
| `scripts/js/create_proposal_docx.js` | Proposal Word document generation |
| `figures/Cherief_scRNA-seq/` | All Cherief 2023 analysis figures |
| `figures/pipeline_flowchart.png` | Full analysis pipeline diagram |
| `docs/research-plan.md` | Detailed scientific rationale and pipeline |
