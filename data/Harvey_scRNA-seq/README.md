# Harvey et al. 2019 — scRNA-seq Data Summary

**Paper:** Harvey et al. (2019) *A Tppp3+Pdgfra+ tendon stem cell population contributes to regeneration and reveals a shared role for PDGF signalling in regeneration and fibrosis.* Nature Cell Biology.

**SRA accession:** PRJNA506218 / SRR9087252 (raw FASTQs, 23.2 Gb, not downloaded)
**GitHub repo:** tyharve/fan-2019-tendon

---

## Data

- **Platform:** 10x Genomics Chromium Single Cell 3′ (NextSeq 500)
- **Sample:** TH1 — uninjured adult male mouse Patellar tendon (~2,491 cells)
- **Processing:** Cell Ranger → count matrix at `/mnt/sequence/10x/TH1_count/outs/filtered_gene_bc_matrices/mm10` (institutional server, not public)

### Files in `10x/`

| File | Contents |
|---|---|
| `tharvey-10x.Rmd` | Initial exploratory analysis (Frederick Tan, Mar 2018) |
| `tharvey-10x-24.Rmd` | Revised trajectory analysis (Tyler Harvey, Apr 2018) |
| `tharvey-10x.nb.html` / `.html` | Rendered output of initial analysis |
| `tharvey-10x-24.nb.html` / `.html` | Rendered output of trajectory analysis |
| `monocle.Rmd` / `monocle.nb.html` | Monocle pseudotime analysis |
| `TH1_24_clustering_DEG_genes.Rda` / `.csv` | Monocle DEG table (11,206 genes × 7 cols) — **not a count matrix** |
| `web_summary_10x.html` | Cell Ranger QC report |

> The raw count matrices (matrix.mtx, barcodes.tsv, genes.tsv) were never deposited — only analysis scripts and DEG results are publicly available.

---

## Cell Ranger Clusters (all 2,491 cells)

| Cluster | Identity | Key markers |
|---|---|---|
| 2 | TSPC / sheath | `Tppp3+`, `Pdgfra+` |
| 3 | T-FAP | `Pdgfra+` only |
| 4 | Tenocyte | `Scx+`, `Mkx+` |
| others | Immune, endothelial, etc. | — |

---

## Analysis Scripts — What Each Does

### `tharvey-10x.Rmd` (Frederick Tan — exploratory draft)

- Loads Cell Ranger output via `cellrangerRkit` and `Seurat`
- Visualizes Cell Ranger graph-based clusters on tSNE
- Subsets **clusters 2, 3, and 4** (TSPC + T-FAP + tenocyte) into `TH1_234`
- Runs Monocle sub-clustering and basic trajectory
- Tracks markers: `Tppp3`, `Scx`, `Mkx`, `Pdgfra`, `Acta2`
- Tabulates `Acta2+Tppp3` double-positive cells per cluster

### `tharvey-10x-24.Rmd` (Tyler Harvey — final analysis)

- Same data loading as above
- **Drops cluster 3 (T-FAP)** — subsets only clusters **2 and 4** into `TH1_24`
- Runs Monocle DDRTree trajectory → **5 pseudotime states**
- BEAM branching analysis at branch points 1 and 2
- Tracks three marker gene sets:
  - `goi`: Tppp3, Scx, Mkx, Pdgfra
  - `goi2`: Tppp3, Pdgfra, Scx, Fmod
  - `goi3`: Mkx, Pdgfrl, Tnc, Tnmd, Ly6e
- Tabulates co-expression: `Tppp3+Pdgfra`, `Tppp3+Scx`, `Tppp3+Pdgfra+Scx`, `Scx+Mkx`
- Saves per-state DEG lists: `state1–5.csv`, `TH1_24_markers_state.csv`
- Saves branching heatmap as `TH_24_BEAMbranch1.pdf`

### `monocle.Rmd`

- Downstream Monocle trajectory analysis building on `TH1_24`

---

## Key Biological Conclusions

1. **Cluster 2 (Tppp3+Pdgfra+)** = TSPCs: confirmed as stem/progenitor cells sitting at the base of the TSPC → tenocyte trajectory
2. **Cluster 4 (Scx+Mkx+Tnmd+)** = mature tenocytes: the differentiated endpoint of the trajectory
3. **Pseudotime trajectory** (5 states) maps the TSPC-to-tenocyte differentiation axis; BEAM identifies genes that bifurcate at each branch point
4. **Cluster 3 (T-FAP, Pdgfra+ only)** was deliberately excluded from trajectory analysis — its relationship to the TSPC fate is uncharacterized in this dataset

---

## Relevance to This Project

The T-FAP cluster (cluster 3) was set aside in Harvey 2019's own analysis. Our project targets exactly this gap: the TSPC vs. T-FAP fate decision. To use this dataset we need the full count matrix (all clusters including cluster 3), which requires downloading SRR9087252 from SRA and running Cell Ranger, or locating a GEO accession with pre-processed matrices.
