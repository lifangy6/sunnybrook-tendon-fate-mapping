# Computational environment

Everything in this repository was produced by three separate environments. They
were never unified, and this document records them as they actually were rather
than as a tidied-up single stack.

**Start here:** to run the analysis, install [`analysis.txt`](analysis.txt).
Everything else in this folder is for a specific purpose described below.

| # | Environment | Runs | Python | Spec |
|---|---|---|---|---|
| 1 | Analysis | `scripts/ipynb/01`–`10`, `scripts/py/pyscenic_02_prepare_loom.py` | 3.14.5 | [`analysis.txt`](analysis.txt), [`analysis-lock.txt`](analysis-lock.txt) |
| 2 | Poster build | `scripts/py/` (except the loom prep) | 3.12 | [`poster.txt`](poster.txt) |
| 3 | pySCENIC | `scripts/sh/` on Alliance Canada | 3.11.5 | [`scripts/sh/pyscenic_00_setup.sh`](../scripts/sh/pyscenic_00_setup.sh) |

Environment 1 is the one that matters most: it produced every number, figure,
and model in the results. If you only recreate one, recreate that.

---

## 1. Analysis environment

Python 3.14.5. Every notebook from QC through the healing index ran here.

Run from the repository root:

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux
pip install -r environments/analysis.txt
jupyter lab
```

Two files describe this environment, for different purposes:

- **`analysis.txt`** — the 23 direct dependencies with exact pins, grouped by
  analysis stage and commented. Read and edit this one.
- **`analysis-lock.txt`** — a full `pip freeze` (161 packages) that also pins
  the 138 transitive dependencies `analysis.txt` leaves to pip. Use it when you
  want a byte-for-byte rebuild rather than a readable list:

  ```bash
  pip install -r environments/analysis-lock.txt
  ```

  It matters because some of those transitive packages affect results without
  ever being imported by name — `pynndescent`, for instance, is what
  `umap-learn` uses to build the nearest-neighbour graph, so its version can
  shift UMAP coordinates.

### How these versions were recovered

They were not reconstructed from guesswork. The notebooks ran on a system
Python install at `AppData\Local\Python\pythoncore-3.14-64`, which was still
intact, so the pins were read directly off the interpreter that did the work.
Three independent cross-checks agree with it:

- `05_cellrank_fate_trajectory.ipynb` prints `CellRank 2.3.2` in its output.
- `06_liana_cellcell_communication.ipynb` prints `liana 0.1.9`.
- The `FutureWarning` in notebooks 08 and 09 says `'penalty' was deprecated in
  version 1.8`, consistent with the installed scikit-learn 1.8.0.

### Dependencies that an import scan would miss

`leidenalg`, `igraph`, and `umap-learn` are never imported by name in any
notebook, but `sc.tl.leiden` and `sc.tl.umap` fail without them. They are
pinned in `analysis.txt` for that reason. If you ever regenerate that file from
imports alone, you will drop them and the clustering step will break.

---

## 2. Poster build environment

Python 3.12, run through `uv` with no persistent virtualenv:

Run from the repository root:

```bash
uv run --python 3.12 --with-requirements environments/poster.txt \
    python scripts/py/build_poster_final.py

.\scripts\py\export_poster.ps1      # .pptx -> PDF + PNG
```

The pins in `poster.txt` are a **reconstruction** from the `uv` wheel cache, not
a reading from a live interpreter — the `uv run` invocations left nothing
behind. See the header of that file for the caveat.

This environment deliberately resolved newer `numpy`, `pandas`, `scipy`, and
`matplotlib` than the analysis environment. The skew is real and is recorded
rather than smoothed over. It does not affect any reported result: the poster
scripts only read finished files out of `data/` and `figures/`, and never
recompute a statistic.

`export_poster.ps1` drives Microsoft PowerPoint through COM automation and
therefore needs Windows with PowerPoint installed. On another platform, export
the `.pptx` by hand or with `soffice --headless --convert-to pdf`, accepting
small differences in font and spacing.

---

## 3. pySCENIC environment (HPC)

Runs on Alliance Canada (`nibi`), not locally — the GRN inference step needs
far more memory and wall time than a laptop provides. Fully scripted in
[`scripts/sh/pyscenic_00_setup.sh`](../scripts/sh/pyscenic_00_setup.sh):

```bash
module load python/3.11.5 arrow/17.0.0
bash scripts/sh/pyscenic_00_setup.sh          # once
source /path/to/envs/pyscenic/bin/activate
```

Captured from the live environment that produced the regulons in
`data/pyscenic/` (2026-08-02) and pinned in that script:

| Package | Version | Source |
|---|---|---|
| Python | 3.11.5 | Alliance Canada module |
| arrow | 17.0.0 | Alliance Canada module |
| pySCENIC | 0.12.0 | Alliance Canada wheelhouse (`--no-index`) |
| arboreto | 0.1.6 | wheelhouse, as a pySCENIC dependency |
| ctxcore | 0.2.0 | wheelhouse, as a pySCENIC dependency |
| loompy | 3.0.7 | wheelhouse, as a pySCENIC dependency |
| numpy | 1.26.4 | wheelhouse; must stay < 2.0 |
| pandas | 2.2.1 | wheelhouse |
| dask | 2023.12.1 | PyPI; pre-`dask-expr`, arboreto 0.1.6 breaks on dask ≥ 2024 |
| distributed | 2023.12.1 | PyPI; must match dask |

### The `+computecanada` suffix

On the cluster these packages report versions like `arboreto==0.1.6+computecanada`.
That trailing label is a PEP 440 *local version identifier* marking a wheel
rebuilt by Alliance Canada against their toolchain. Those builds exist only in
their wheelhouse — `pip install arboreto==0.1.6+computecanada` fails anywhere
else.

The pins in the setup script therefore omit the suffix deliberately. PEP 440
specifies that a public version specifier ignores the local label when
matching, so `==0.1.6` matches `0.1.6+computecanada` on the cluster *and* plain
`0.1.6` from PyPI off it. Writing the suffix into the pin would hard-code the
script to Alliance Canada.

A related correction: the script previously commented that `arboreto`, `ctxcore`,
and `loompy` were installed "from PyPI". They were not — `pip install --no-index
pyscenic` already pulls them from the wheelhouse as pySCENIC dependencies, which
is why they carry the `+computecanada` label. Only `dask` and `distributed`
genuinely come from PyPI. They are now named explicitly under `--no-index` so
the versions are pinned rather than inherited silently.

The setup script also patches pySCENIC 0.12.0 for NumPy ≥ 1.24, which removed
`np.object`, `np.bool`, `np.int`, `np.float`, and `np.complex`. Without that
patch pySCENIC 0.12.0 fails on import. The patch is applied in place with
`sed`, so it must be re-run whenever the environment is rebuilt.

### NumPy constraint

`numpy` must stay below 2.0. pySCENIC 0.12.0 predates the NumPy 2 ABI change and
does not work under it even with the `np.object` / `np.bool` patch applied. The
setup script now fails loudly with an explanatory message rather than proceeding
to a broken environment if a rebuild resolves NumPy ≥ 2.

`numpy` and `pandas` are intentionally left unpinned in the install command:
they arrive as pySCENIC dependencies, and over-constraining a curated wheelhouse
tends to break resolution rather than improve it. Their recorded versions are in
the table above, and the script prints the resolved set at the end so any drift
from that set is visible immediately.

### Recovering this environment if scratch is purged

This environment lived on `scratch`, which Alliance Canada purges automatically.
The versions above were captured before that happened, so the environment can be
rebuilt from the setup script alone — but if a rebuild ever resolves a different
set, the table above is the reference for what the published results were
actually produced with.

---

## Non-Python dependencies

These are not installable from any requirements file and must be obtained
separately.

| Tool / resource | Version | Used by | Source |
|---|---|---|---|
| Cell Ranger | 10.0.0 | `cellranger_harvey.sh` | 10x Genomics |
| mm10 reference | `refdata-gex-mm10-2020-A` | `cellranger_harvey.sh` | 10x Genomics |
| SRA Toolkit | cluster module | `download_harvey.sh`, `fasterq_harvey.sh` | Alliance Canada |
| cisTarget rankings | `mm10 … v10_clust`, 500bp and 10kbp | `pyscenic_04_ctx.sh` | resources.aertslab.org |
| motif2TF table | `motifs-v9-nr.mgi-m0.001-o0.0.tbl` | `pyscenic_04_ctx.sh` | resources.aertslab.org |
| mouse TF list | `mm_mgi_tfs.txt` | `pyscenic_03_grn.sh` | pySCENIC repo (`master`) |
| Microsoft PowerPoint | any recent | `export_poster.ps1` | — |

Two of these are worth flagging as fragile. `mm_mgi_tfs.txt` is fetched from
the `master` branch of the pySCENIC GitHub repository rather than a tagged
release, so the file can change without notice. The cisTarget rankings are
large and are not mirrored here; if aertslab reorganises their hosting, the
download URLs in `pyscenic_01_download_db.sh` will need updating.

---

## Regenerating the lock file

After changing anything in the analysis environment:

```bash
pip freeze > environments/analysis-lock.txt
```

Update the matching pin in `analysis.txt` by hand — it is curated, so it should
not be machine-generated. Keep the two in step: a lock file that no longer
matches `analysis.txt` is worse than none, because it looks authoritative while
describing an environment that no longer exists.
