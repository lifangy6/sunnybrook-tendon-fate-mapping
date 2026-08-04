# Scripts

Everything that produces a result in this repository. Three folders, by language
and by where the code runs:

| Folder | What it holds | Runs where |
|---|---|---|
| [`ipynb/`](ipynb/) | The Stage 0–9 analysis, one notebook per stage | Local, analysis env |
| [`sh/`](sh/) | Data retrieval, Cell Ranger, and the pySCENIC pipeline | Alliance Canada (SLURM) |
| [`py/`](py/) | Loom preparation, the poster build, and diagrams | Local |

Environments are documented in [`environments/README.md`](../environments/README.md).
Stage-by-stage findings and caveats are in [`docs/progress.md`](../docs/progress.md).

---

## Running the notebooks

```bash
pip install -r environments/analysis.txt
cd scripts/ipynb
jupyter lab
```

**Run notebooks with the working directory set to `scripts/ipynb/`.** Every path
in them is relative to that folder (`ROOT = Path('../..')`), so launching Jupyter
from the repository root will make the loads fail.

Each notebook opens with the same header: title, stage, purpose, then explicit
**Inputs**, **Outputs**, and which notebooks it runs after and feeds into. Read
that block before running anything — it is the fastest way to see whether the
file it needs already exists.

## Notebook order

The numbers are the run order, and each notebook's outputs are the next one's
inputs. Stage numbers refer to [`docs/progress.md`](../docs/progress.md).

| # | Notebook | Stage | What it does |
|---|---|---|---|
| 01 | [`01_cherief2023_qc_clustering`](ipynb/01_cherief2023_qc_clustering.ipynb) | 1a/1b | QC, cluster and annotate Cherief 2023 (GSE244921), innervated vs. denervated |
| 02 | [`02_cherief2023_subcluster_tspc_tfap`](ipynb/02_cherief2023_subcluster_tspc_tfap.ipynb) | 1c | Split cluster 8 into TSPC / T-FAP / Tenogenic-progenitor / Stromal |
| 03 | [`03_harvey2019_qc_clustering`](ipynb/03_harvey2019_qc_clustering.ipynb) | 2 | QC, cluster and annotate Harvey 2019 — the classifier's training labels |
| 04 | [`04_pyscenic_analysis`](ipynb/04_pyscenic_analysis.ipynb) | 3a | Differential TF regulon activity from the AUCell scores; cross-dataset filter |
| 05 | [`05_cellrank_fate_trajectory`](ipynb/05_cellrank_fate_trajectory.ipynb) | 4 | Fate probabilities and lineage drivers; builds the 119-gene candidate set |
| 06 | [`06_liana_cellcell_communication`](ipynb/06_liana_cellcell_communication.ipynb) | 5 | Ligand-receptor signalling, innervated vs. denervated |
| 07 | [`07_mechanistic_synthesis`](ipynb/07_mechanistic_synthesis.ipynb) | 6 | Joins pySCENIC × CellRank × LIANA into one regulatory circuit |
| 08 | [`08_feature_selection`](ipynb/08_feature_selection.ipynb) | 7 | LASSO + Boruta + XGBoost → 44-gene and 23-gene panels |
| 09 | [`09_classifier_training_validation`](ipynb/09_classifier_training_validation.ipynb) | 8 | Trains on Harvey, validates on Cherief |
| 10 | [`10_healing_index`](ipynb/10_healing_index.ipynb) | 9 | Continuous 0–100 Healing Index and a turnkey scoring function |

### The `b` notebooks are audit re-runs

`04b`, `05b`, `06b` and `07b` each re-test one specific claim made by the
notebook they are named after, after an independent audit questioned it. **They
do not replace the originals** — both are kept so the two can be compared, and
each `b` notebook opens by stating exactly what it is testing and why.

| # | Re-tests | Verdict |
|---|---|---|
| [`04b`](ipynb/04b_pyscenic_powermatched_filter.ipynb) | Is "0 consistent TSPC regulons" a sample-size artifact? | **Held.** 14/15 T-FAP regulons replicate under power matching; TSPC still zero |
| [`05b`](ipynb/05b_cellrank_root_sensitivity.ipynb) | Do the Stage 4 results depend on the pseudotime root? | **Mixed.** Fate percentages move 5–7 points; the 119-gene list is 94% stable |
| [`06b`](ipynb/06b_liana_permutation_v2.ipynb) | Does `delta_rank` survive a real permutation test? | **Partly.** Use `cellphone_pvals`, not `delta_rank`, for any specific LR pair |
| [`07b`](ipynb/07b_receptor_feedback_v2_tested.ipynb) | Is the receptor-feedback overlap more than chance? | **Failed.** Not significant even uncorrected — the claim is retracted |

Where a `b` notebook overturned something, the original notebook's header now
says so, and `07b` §6 redraws the Stage 6 circuit diagram without the retracted
edges. Use `figures/mechanistic_synthesis/regulatory_circuit_v2_corrected.png`,
not the original, for the poster and report.

## HPC pipeline (`sh/`)

Two independent chains, both run on Alliance Canada. Each script's header states
its usage, prerequisite, and next step.

**Harvey 2019 count matrix** (Stage 2) — feeds notebook `03`:

```
download_harvey.sh  →  fasterq_harvey.sh  →  cellranger_harvey.sh
```

`fasterq_harvey.sh` re-dumps the same archive with `--include-technical` because
the first pass omits the 10x barcode/UMI read that Cell Ranger needs.

**pySCENIC** (Stage 3a) — feeds notebook `04`:

```
pyscenic_00_setup.sh  (once, interactive)
pyscenic_01_download_db.sh  (once — mm10 cisTarget databases, ~1.5 GB)
        ↓
../py/pyscenic_02_prepare_loom.py   ← runs locally, then scp the looms up
        ↓
pyscenic_03_grn.sh  →  pyscenic_04_ctx.sh  →  pyscenic_05_aucell.sh
```

Steps 03–05 are SLURM job arrays: task 0 = Harvey, task 1 = Cherief. Copy the
resulting `*_regulons.csv` and `*_aucell.loom` back into `data/pyscenic/` before
running notebook `04`.

## Local scripts (`py/`)

| Script | Purpose |
|---|---|
| [`pyscenic_02_prepare_loom.py`](py/pyscenic_02_prepare_loom.py) | Exports TSPC + T-FAP cells to loom for pySCENIC. **Analysis env**, not the poster env |
| [`poster_style.py`](py/poster_style.py) | Shared palette and typography for every poster figure |
| [`poster_figures.py`](py/poster_figures.py) | Regenerates all poster figures into `figures/poster/` |
| [`build_poster_final.py`](py/build_poster_final.py) | Builds the final poster `.pptx`. **The only build script to edit** |
| [`build_poster_a.py`](py/build_poster_a.py), [`build_poster_b.py`](py/build_poster_b.py) | Frozen drafts of the two layouts that were considered; kept for the record, do not re-run |
| [`make_footer_assets.py`](py/make_footer_assets.py) | Rebuilds the QR code and DRAC lockup used in the poster footer |
| [`export_poster.ps1`](py/export_poster.ps1) | Exports `.pptx` → PDF and PNG via PowerPoint COM automation |
| [`draw_pipeline.py`](py/draw_pipeline.py) | Draws `figures/pipeline_flowchart.png` for the docs |

Everything except `pyscenic_02_prepare_loom.py` runs in the **poster** env
([`environments/poster.txt`](../environments/poster.txt)); each file's docstring
carries its exact `uv run` command.

## Reproducibility notes

Worth knowing before trusting a re-run:

- **Stored outputs are the record.** The notebooks in this repository carry the
  outputs from the run that produced the reported numbers. Re-running overwrites
  them; if you only want to read the results, don't execute anything.
- **Cell execution counts in `06` are not sequential.** That notebook was
  developed out of order and its export cell ran before the last plotting cells.
  The cell order top-to-bottom is still the correct logical order, but a clean
  "Restart & Run All" has not been done since, so treat its stored outputs as a
  composite of several runs rather than a single linear execution.
- **GRNBoost2 was run once, unseeded.** The pySCENIC target-gene lists in
  `data/pyscenic/*_regulons.csv` are therefore not exactly reproducible; a rerun
  gives a similar but not identical network. Anything derived from individual
  TF-target edges is a hypothesis, not a fixed result.
- **Neither dataset has biological replicates** — one pooled sample per
  condition. Every validation in Stages 7–9 is a within- or cross-*dataset*
  check, never a cross-animal one. The notebook headers and `docs/progress.md`
  repeat this where it matters.
