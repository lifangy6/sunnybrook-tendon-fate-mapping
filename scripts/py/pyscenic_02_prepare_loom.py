"""
Run locally before transferring files to HPC.
Exports TSPC + T-FAP cells from both datasets as loom files for pySCENIC input.

Output files (transfer these to HPC after running):
  data/pyscenic/harvey_tspc_tfap.loom
  data/pyscenic/cherief_tspc_tfap.loom

Transfer command (run from project root):
  scp data/pyscenic/*.loom lifangy6@nibi.alliancecan.ca:/home/lifangy6/scratch/BINF6999/data/pyscenic/input/
"""

import scanpy as sc
import numpy as np
import os
from pathlib import Path

# Paths relative to this script file — works regardless of working directory
SCRIPT_DIR = Path(__file__).parent
ROOT = SCRIPT_DIR.parent.parent
OUT_DIR = ROOT / 'data' / 'pyscenic'
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Harvey 2019 ───────────────────────────────────────────────────────────────
print('Loading Harvey 2019...')
adata_harvey = sc.read_h5ad(ROOT / 'data' / 'Harvey_scRNA-seq' / 'harvey2019_processed.h5ad')

# Keep only high-confidence TSPC and T-FAP cells (Unknown excluded during annotation)
harvey_sub = adata_harvey[adata_harvey.obs['cell_type'].isin(['TSPC', 'T-FAP'])].copy()
print(f'Harvey TSPC+T-FAP: {harvey_sub.n_obs} cells')
print(harvey_sub.obs['cell_type'].value_counts())

# pySCENIC needs log-normalized counts — use adata.raw
harvey_sub_raw = harvey_sub.raw.to_adata()

out_harvey = OUT_DIR / 'harvey_tspc_tfap.loom'
harvey_sub_raw.write_loom(out_harvey)
print(f'Saved: {out_harvey}')

# ── Cherief 2023 ──────────────────────────────────────────────────────────────
# The sub h5ad has cell_type labels but no .raw (scaling was done before sub-clustering).
# Load the full Cherief h5ad to get .raw (log-normalised counts), then subset to
# the TSPC+T-FAP barcodes identified in the sub h5ad.
# Requires script 01 to have been re-run with adata.raw = adata added before scaling.

print('\nLoading Cherief 2023...')
adata_cherief_sub = sc.read_h5ad(ROOT / 'data' / 'Cherief_scRNA-seq' / 'GSE244921_cluster8_sub.h5ad')
adata_cherief_full = sc.read_h5ad(ROOT / 'data' / 'Cherief_scRNA-seq' / 'GSE244921_processed.h5ad')

# Get TSPC + T-FAP barcodes from sub h5ad
tspc_tfap_barcodes = adata_cherief_sub.obs_names[
    adata_cherief_sub.obs['cell_type'].isin(['TSPC', 'T-FAP'])
]
print(f'Cherief TSPC+T-FAP: {len(tspc_tfap_barcodes)} cells')
print(adata_cherief_sub.obs.loc[tspc_tfap_barcodes, 'cell_type'].value_counts())

# Subset full h5ad to those barcodes and extract log-normalised counts from .raw
if adata_cherief_full.raw is None:
    raise RuntimeError(
        'adata.raw not found in GSE244921_processed.h5ad.\n'
        'Re-run script 01 (add adata.raw = adata before sc.pp.scale) and save, then retry.'
    )

cherief_full_sub = adata_cherief_full[tspc_tfap_barcodes].copy()
cherief_sub_raw = cherief_full_sub.raw.to_adata()

# Carry cell_type labels from sub h5ad into the loom metadata
cherief_sub_raw.obs['cell_type'] = adata_cherief_sub.obs.loc[tspc_tfap_barcodes, 'cell_type']
print('Using adata.raw (log-normalised counts) from full Cherief h5ad')

out_cherief = OUT_DIR / 'cherief_tspc_tfap.loom'
cherief_sub_raw.write_loom(out_cherief)
print(f'Saved: {out_cherief}')

print('\n=== Transfer to HPC ===')
print('Run from project root:')
print(f'  scp data/pyscenic/*.loom lifangy6@nibi.alliancecan.ca:/home/lifangy6/scratch/BINF6999/data/pyscenic/input/')
