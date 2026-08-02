#!/bin/bash
# Run interactively on HPC login node (not submitted via sbatch)
# Usage: bash pyscenic_00_setup.sh
#
# Creates a Python virtual environment using Alliance Canada pre-built wheels.
# pySCENIC 0.12.0 is available via avail_wheels — installed with --no-index (faster).
# Only needs to be run once.
#
# RECORDED VERSIONS — captured from the live environment that produced the
# regulons in data/pyscenic/ (pip freeze, 2026-08-02):
#
#   pyscenic==0.12.0+computecanada     numpy==1.26.4+computecanada
#   arboreto==0.1.6+computecanada      pandas==2.2.1+computecanada
#   ctxcore==0.2.0+computecanada       dask==2023.12.1
#   loompy==3.0.7+computecanada        distributed==2023.12.1
#
# The "+computecanada" suffix is a PEP 440 local version label marking a wheel
# rebuilt by Alliance Canada. Those builds exist only in their wheelhouse, so
# the pins below deliberately omit the suffix: under PEP 440 a public version
# specifier ignores the local label, so "==0.1.6" matches 0.1.6+computecanada
# on the cluster AND plain 0.1.6 from PyPI elsewhere. Writing the suffix into
# the pin would make this script fail anywhere but Alliance Canada.
#
# numpy and pandas arrive as pySCENIC dependencies and are intentionally left
# unpinned — the wheelhouse resolves them, and over-constraining a curated
# wheelhouse tends to break resolution. They are verified at the end instead.
# numpy must stay below 2.0; pySCENIC 0.12.0 does not survive the NumPy 2 ABI
# change even with the compatibility patch applied below.

set -euo pipefail

# Arrow module must be loaded BEFORE virtualenv creation and activation
# so that pyarrow is available from the system rather than PyPI
module load python/3.11.5
module load arrow/17.0.0

ENV_DIR=/home/lifangy6/scratch/BINF6999/envs/pyscenic

echo "=== Removing existing environment (if any) ==="
rm -rf $ENV_DIR

echo "=== Creating virtual environment at $ENV_DIR ==="
virtualenv --no-download $ENV_DIR

echo "=== Activating environment ==="
source $ENV_DIR/bin/activate

echo "=== Upgrading pip from Alliance Canada wheel repo ==="
pip install --no-index --upgrade pip

echo "=== Installing pySCENIC and its pipeline deps from the Alliance Canada wheelhouse ==="
# arboreto, ctxcore and loompy are pySCENIC dependencies, so --no-index pulls
# them from the wheelhouse too. They are named explicitly here only to pin the
# versions: without the pins a wheelhouse refresh could silently change them,
# and a mismatched ctxcore/arboreto pair is the usual cause of a GRN step that
# runs to completion but emits an empty adjacency table.
pip install --no-index \
    "pyscenic==0.12.0" \
    "arboreto==0.1.6" \
    "ctxcore==0.2.0" \
    "loompy==3.0.7"

echo "=== Installing dask/distributed from PyPI ==="
# Not in the wheelhouse at these versions, so this genuinely does hit PyPI.
# Pinned to the pre-dask-expr era: arboreto 0.1.6 is incompatible with dask>=2024,
# and the two must match each other exactly.
pip install "dask==2023.12.1" "distributed==2023.12.1"

echo "=== Patching pySCENIC 0.12.0 for NumPy 1.24+ compatibility ==="
# np.object/np.bool/np.int/np.float were removed in NumPy 1.24; replace with bare Python builtins.
#
# Derived from $ENV_DIR rather than hardcoded. The previous hardcoded value was
# /scratch/$USER/... while ENV_DIR is /home/$USER/scratch/... — those only refer
# to the same directory because /home/$USER/scratch is a symlink to /scratch/$USER.
# The glob keeps this working if the python module version changes.
PYSCENIC_DIR=$(echo "$ENV_DIR"/lib/python*/site-packages/pyscenic)
if [ ! -d "$PYSCENIC_DIR" ]; then
    echo "ERROR: could not locate the installed pyscenic package under $ENV_DIR" >&2
    echo "       (looked for $ENV_DIR/lib/python*/site-packages/pyscenic)" >&2
    exit 1
fi
echo "Patching $PYSCENIC_DIR"
find "$PYSCENIC_DIR" -name "*.py" -exec sed -i \
    -e 's/np\.object\b/object/g' \
    -e 's/np\.bool\b/bool/g' \
    -e 's/np\.int\b/int/g' \
    -e 's/np\.float\b/float/g' \
    -e 's/np\.complex\b/complex/g' \
    -e 's/\.iteritems()/.items()/g' \
    {} +
echo "Patch applied."

echo "=== Verifying installation ==="
# Print resolved versions rather than a bare OK, so that a rebuild which drifts
# from the recorded set at the top of this file is visible immediately.
pip freeze | grep -iE "^(pyscenic|arboreto|ctxcore|loompy|dask|distributed|numpy|pandas)=" \
    || echo "WARNING: could not read versions from pip freeze"

python - <<'PY'
import numpy, pyscenic, arboreto, ctxcore, loompy
print(f"pySCENIC {pyscenic.__version__} imported OK (NumPy patch applied)")
major = int(numpy.__version__.split(".")[0])
if major >= 2:
    raise SystemExit(
        f"ERROR: numpy {numpy.__version__} is >= 2.0. pySCENIC 0.12.0 does not "
        "work under NumPy 2 even with the compatibility patch. Rebuild the "
        "environment against numpy<2 (1.26.4 is the recorded version)."
    )
print(f"numpy {numpy.__version__} OK (<2.0 as required)")
PY

echo ""
echo "=== Done ==="
echo "In future sessions, activate with:"
echo "  module load python/3.11.5 arrow/17.0.0 && source $ENV_DIR/bin/activate"
