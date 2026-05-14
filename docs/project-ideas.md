# Project Ideas

## Project A — What drives the TSPC vs. T-FAP fate decision?

[Harvey et al. 2019](https://doi.org/10.1038/s41556-019-0417-z) identified two PDGFRα+ populations in the same tendon sheath — one regenerates (TSPCs), one scars (T-FAPs). The gene that separates them is Tppp3, but the upstream regulatory logic is unresolved.

**Approach**
- Primary dataset: [Cherief et al. 2023](https://doi.org/10.1126/scitranslmed.ade4619) Achilles scRNA-seq (larger N, injury-activated); use [Harvey et al. 2019](https://doi.org/10.1038/s41556-019-0417-z) (2,491 cells) as secondary — TSPC cluster is too small for reliable TF inference alone
- Infer transcription factor networks driving each fate ([pySCENIC](https://pyscenic.readthedocs.io/))
- Model cell fate trajectories from a shared PDGFRα+ ancestor ([CellRank](https://cellrank.org/))
- Identify which injury signals (NGF, TGFβ, PDGF) push cells toward one fate using cell-cell communication analysis on the innervated vs. denervated comparison in [Cherief et al. 2023](https://doi.org/10.1126/scitranslmed.ade4619)

**Output:** A regulatory circuit — TF programs governing the TSPC/T-FAP fate fork, and which upstream signals can shift the balance toward regeneration.

---

## Project B — What do neonatal MPs have that adult MPs lost?

Transplanting neonatal Hic1+ MPs into injured adult tendons partially restores regeneration, suggesting the difference is cell-intrinsic. [Arostegui et al. 2022](https://doi.org/10.1038/s41467-022-32695-1) provides a rare time-resolved scRNA-seq atlas from embryo to adult — the right dataset to answer this directly.

**Approach**
- Integrate [Arostegui et al. 2022](https://doi.org/10.1038/s41467-022-32695-1) (6 timepoints, E10.5 → adult) to identify genes that monotonically decrease with age (RNA-based; this is the core deliverable)
- Cross with [Abbasi et al. 2020](https://doi.org/10.1016/j.stem.2020.07.008) Hic1-KO skin data to flag which age-decreased genes Hic1 is actively suppressing
- Cross-tissue validation: check if the same age-declining genes appear in [Scott et al. 2019](https://doi.org/10.1016/j.stem.2019.11.004) muscle MP data — conserved signatures across tissues are stronger candidates
- Optional: use [Scott et al. 2019](https://doi.org/10.1016/j.stem.2019.11.004) scATAC-seq (adult muscle) to ask whether candidate loci are chromatinclosed in adults — note this is a cross-tissue inference, not a direct integration

**Output:** A ranked list of rejuvenation candidate genes supported by transcriptional and Hic1-suppression evidence, with chromatin accessibility as a supporting (not primary) layer.

---

## Project C — A minimal gene signature for regenerative vs. fibrotic healing

The lab has established that TSPCs drive regeneration and T-FAPs drive fibrosis. The clinical question is: can we measure which process is happening in a patient biopsy? This project turns that biology into a practical classifier.

**Approach**
- Define regenerative vs. fibrotic cell labels from [Harvey et al. 2019](https://doi.org/10.1038/s41556-019-0417-z) (TSPC vs. T-FAP clusters as ground-truth labels)
- Use [LASSO](https://scikit-learn.org/stable/modules/linear_model.html#lasso), [Boruta](https://github.com/scikit-learn-contrib/boruta_py), and [XGBoost](https://xgboost.readthedocs.io/) feature selection to identify a minimal gene panel (~10–30 genes) that distinguishes the two states
- Validate on [Cherief et al. 2023](https://doi.org/10.1126/scitranslmed.ade4619) innervated vs. denervated scRNA-seq as a held-out test — denervation shifts healing toward fibrosis, providing a real biological contrast in a different injury model (note: Moser et al. 2021 is histology-based and does not have scRNA-seq count matrices)
- Test generalization to human data using [Cherief et al. 2023](https://doi.org/10.1126/scitranslmed.ade4619)'s human tendon biopsy transcriptomics

**Output:** A validated minimal gene panel and a continuous "healing index score" applicable to any scRNA-seq dataset from the lab.

---

## Quick comparison

| | Project A | Project B | Project C |
|---|---|---|---|
| **Core type** | Mechanism | Discovery | Applied ML |
| **Datasets** | [Cherief 2023](https://doi.org/10.1126/scitranslmed.ade4619) (primary), [Harvey 2019](https://doi.org/10.1038/s41556-019-0417-z) (secondary) | [Arostegui 2022](https://doi.org/10.1038/s41467-022-32695-1), [Abbasi 2020](https://doi.org/10.1016/j.stem.2020.07.008), [Scott 2019](https://doi.org/10.1016/j.stem.2019.11.004) (supporting) | [Harvey 2019](https://doi.org/10.1038/s41556-019-0417-z), [Cherief 2023](https://doi.org/10.1126/scitranslmed.ade4619) |
| **Main tools** | [pySCENIC](https://pyscenic.readthedocs.io/), [CellRank](https://cellrank.org/), [LIANA](https://liana-py.readthedocs.io/) | [scVI](https://scvi-tools.org/), [ArchR](https://www.archrproject.com/), [XGBoost](https://xgboost.readthedocs.io/) + [SHAP](https://shap.readthedocs.io/) | [LASSO](https://scikit-learn.org/stable/modules/linear_model.html#lasso), [XGBoost](https://xgboost.readthedocs.io/), [AUCell](https://bioconductor.org/packages/release/bioc/html/AUCell.html) |
