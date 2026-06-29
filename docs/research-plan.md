# Research Plan

## A Mechanism-Informed Gene Signature for Regenerative vs. Fibrotic Tendon Healing

---

## 1. Scientific Background

Tendons heal in one of two fundamentally different ways: **regeneration** (restoring tendon architecture and mechanical function) or **fibrosis** (forming a permanent collagen scar with impaired function). Two cell populations in the tendon sheath drive each outcome:

- **TSPCs** — Tendon Stem/Progenitor Cells (Tppp3+, PDGFRα+): proliferate, infiltrate injury sites, and give rise to aligned tenocyte-like progeny → **regeneration**
- **T-FAPs** — Tendon Fibro/Adipogenic Progenitors (Tppp3−, PDGFRα+): activated by injury and give rise to fibrotic scar cells → **fibrosis**

Both populations occupy the same PDGFRα+ niche in the tendon sheath. The critical unanswered question is: **what decides whether a progenitor becomes a TSPC or a T-FAP?**

Sensory innervation adds a layer to this question. Cherief et al. (2023) showed that TrkA/NGF-mediated reinnervation of the injury site is required for TSPC expansion and functional repair. Denervation shifts healing toward fibrosis, providing a direct experimental handle on the regeneration/fibrosis axis and implicating NGF, TGFβ, and PDGF signaling as candidate upstream regulators.

---

## 2. Research Questions

**Primary (mechanistic — from Project A):** Which transcription factor networks govern the TSPC vs. T-FAP fate decision, and which injury signals (NGF, TGFβ, PDGF) shift the balance?

**Secondary (applied — from Project C):** Can the mechanism-derived gene programs be compressed into a minimal panel (~10–30 genes) that classifies regenerative vs. fibrotic healing in any tendon scRNA-seq dataset?

The two questions are linked: the TF regulons from the mechanistic analysis serve as a biologically grounded prior for feature selection in the classifier, producing a *mechanism-informed* gene signature rather than a purely data-driven one.

---

## 3. Datasets

### Primary — Cherief et al. (2023)

| Field | Detail |
|---|---|
| Paper | Cherief et al., *Science Translational Medicine*, 2023 |
| DOI | [10.1126/scitranslmed.ade4619](https://doi.org/10.1126/scitranslmed.ade4619) |
| GEO accession | GSE244921 |
| Processed file | `data/Cherief_scRNA-seq/GSE244921_processed.h5ad` |
| Tissue | Mouse Achilles tendon |
| Condition | Innervated (normal healing) vs. denervated (impaired healing) |
| Cells after QC | 22,615 |
| Figures | `figures/Cherief_scRNA-seq/` |

**Why this dataset is central:**
Cherief 2023 provides the innervation/denervation contrast that anchors the mechanistic and applied arms. The PDGFRα+ stromal cluster (cluster 8, sub-clustered into TSPC/T-FAP/Tenogenic-progenitor/Stromal) is the focal population for pySCENIC, CellRank, and LIANA analyses. The innervated vs. denervated split serves as the held-out test set for the classifier.

---

### Secondary — Harvey et al. (2019)

| Field | Detail |
|---|---|
| Paper | Harvey et al., *Nature Cell Biology*, 2019 |
| DOI | [10.1038/s41556-019-0417-z](https://doi.org/10.1038/s41556-019-0417-z) |
| SRA accession | PRJNA506218 / SRR9087252 (raw FASTQs, 23.2 GB) |
| Tissue | Mouse patellar tendon (uninjured adult) |
| Processed file | `data/Harvey_scRNA-seq/harvey2019_processed.h5ad` |
| Cells after QC | 4,069 |
| Figures | `figures/Harvey_scRNA-seq/` |

**Why this dataset is essential:**
Harvey 2019 is the paper that defined and named TSPCs and T-FAPs. Its clusters are the ground-truth labels for:
- Seeding TF inference with confirmed TSPC/T-FAP identities (mechanistic arm)
- Training the TSPC/T-FAP classifier (applied arm)

---

## 4. Analysis Pipeline

The pipeline is ordered by dependency. Each stage feeds the next.

```
[1] Sub-cluster cluster 8 (Cherief 2023)
         │
         ▼
[2] Obtain Harvey 2019 count matrix (Cell Ranger)
         │
         ├──────────────────────────────┐
         ▼                              ▼
[3A] pySCENIC — TF network         [3B] Cross-dataset label transfer
     inference on TSPC/T-FAP            Harvey → Cherief cluster 8
     sub-clusters
         │
         ▼
[4] CellRank — fate trajectory
    from shared PDGFRα+ ancestor
         │
         ▼
[5] LIANA — cell-cell communication
    innervated vs. denervated
    (NGF, TGFβ, PDGF ligand-receptor)
         │
         ▼
[6] Mechanism summary: TF regulons +
    upstream signals driving fate fork
         │
         ▼
[7] Feature selection from mechanism-derived
    candidate gene set (LASSO + Boruta + XGBoost)
         │
         ▼
[8] Minimal gene panel (~10–30 genes)
    validated on Cherief 2023
    innervated vs. denervated held-out test
         │
         ▼
[9] Continuous "healing index score"
    applicable to any tendon scRNA-seq
```

### Stage details

**Stage 1 — Sub-cluster cluster 8**
Re-run Leiden at higher resolution (0.8–1.2) restricted to cluster 8 cells. Confirm TSPC sub-cluster by Tppp3 expression; confirm T-FAP sub-cluster by Pdgfra+/Tppp3− co-expression. This is the foundation — if the two populations cannot be cleanly separated, the project scope must be reconsidered.

**Stage 2 — Harvey 2019 Cell Ranger**
One-time compute job on HPC. Produces count matrix for the only dataset with explicitly validated TSPC/T-FAP cluster annotations. Unblocks all downstream steps in both arms.

**Stage 3A — pySCENIC TF inference**
Run on TSPC and T-FAP sub-clusters from both Harvey 2019 and Cherief 2023. GRNBoost2 → cisTarget → AUCell pipeline on Alliance Canada HPC. Cross-dataset direction filter to identify TF regulons with consistent TSPC or T-FAP enrichment in both datasets independently.

**Stage 3B — Label transfer**
Use Seurat/scVI to transfer Harvey 2019 TSPC/T-FAP labels onto Cherief 2023 cluster 8 sub-clusters. Provides a secondary confirmation of sub-cluster identities beyond marker expression alone.

**Stage 4 — CellRank trajectory**
Model pseudotime from the shared PDGFRα+ progenitor pool toward TSPC and T-FAP terminal states. Use PseudotimeKernel (DPT) since GEO deposit has no spliced/unspliced counts. Compute fate probabilities per cell and lineage driver genes correlated with each fate. Cross-reference drivers with pySCENIC regulon target genes to produce a mechanism-informed candidate feature set.

**Stage 5 — LIANA cell-cell communication**
Run `rank_aggregate` (6 methods, mouse consensus LR database) on innervated and denervated subsets separately. Differential metric: `delta_rank = rank_denervated − rank_innervated`. Identifies which ligand-receptor signals arriving at TSPC and T-FAP differ between conditions, linking upstream niche signals to the fate decision.

**Stage 6 — Mechanistic summary**
Synthesize stages 3–5 into a regulatory circuit: which TFs govern each fate, which upstream signals activate them, and how denervation disrupts the balance toward fibrosis.

**Stage 7 — Feature selection**
Use the pySCENIC × CellRank overlap genes plus TSPC marker genes as the candidate feature space. Apply LASSO, Boruta, and XGBoost independently on the Harvey 2019 TSPC/T-FAP clusters; take the intersection of genes selected by ≥2 methods. Reduces multiple-testing burden and keeps the classifier biologically grounded.

**Stage 8 — Classifier validation**
Train on Harvey 2019 TSPC/T-FAP clusters (held out from Stage 7 feature selection). Validate generalization on Cherief 2023 innervated vs. denervated — denervation is known to shift healing toward fibrosis, so a well-calibrated classifier should shift toward the fibrotic end of the score distribution in denervated samples.

**Stage 9 — Healing index score**
Convert the binary classifier into a continuous score using predicted class probabilities. Apply to any new tendon scRNA-seq dataset from the lab.

---

## 5. Key Risks and Mitigations

| Risk | Severity | Mitigation |
|---|---|---|
| Cluster 8 sub-clustering fails to cleanly separate TSPC/T-FAP | High | Try multiple resolutions (0.8–1.5) + harmony integration; fall back to marker-based gating if needed |
| Harvey 2019 Cell Ranger produces low-quality matrix | High | Use STARsolo as alternative aligner; contact Harvey lab directly for count matrix |
| pySCENIC regulons dominated by generic stress TFs (Jun, Fos) | Medium | Apply cross-dataset direction filter; require consistent enrichment in both Harvey and Cherief independently |
| Classifier overfits to Harvey 2019 patellar tendon context | Medium | Strict train/test split; Cherief 2023 (Achilles, different injury model) as held-out test |
| TSPC/T-FAP sub-clusters too small for pySCENIC | Medium | Supplement with Harvey 2019 cells after Cell Ranger; pool timepoints if needed |

---

## 6. Key Papers

| Paper | Role in project |
|---|---|
| Harvey et al. 2019 (*Nat Cell Biol*) | Defines TSPC/T-FAP; ground-truth labels for classifier training |
| Cherief et al. 2023 (*Sci Transl Med*) | Primary dataset; innervation/denervation contrast; human biopsy data |
| Howell et al. 2017 (*Sci Rep*) | Establishes neonatal regeneration model; biological context |
| Kaji et al. 2020 (*eLife*) | TGFβ as migratory signal in neonatal regeneration |
| Moser et al. 2021 (*J Orthop Res*) | SMAlin cells as fibrotic contributors in rotator cuff repair |
