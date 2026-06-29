#!/bin/bash
# Run interactively on HPC login node (not submitted via sbatch)
# Usage: bash pyscenic_00_setup.sh
#
# Creates a Python virtual environment using Alliance Canada pre-built wheels.
# pySCENIC 0.12.0 is available via avail_wheels — installed with --no-index (faster).
# Only needs to be run once.

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

echo "=== Installing pySCENIC from Alliance Canada wheel (0.12.0) ==="
pip install --no-index pyscenic

echo "=== Installing remaining dependencies from PyPI ==="
# Pin dask/distributed to pre-dask-expr era; arboreto 0.1.6 is incompatible with dask>=2024
pip install arboreto ctxcore loompy "dask==2023.12.1" "distributed==2023.12.1"

echo "=== Patching pySCENIC 0.12.0 for NumPy 1.24+ compatibility ==="
# np.object/np.bool/np.int/np.float were removed in NumPy 1.24; replace with bare Python builtins
PYSCENIC_DIR=/scratch/lifangy6/BINF6999/envs/pyscenic/lib/python3.11/site-packages/pyscenic
find $PYSCENIC_DIR -name "*.py" -exec sed -i \
    -e 's/np\.object\b/object/g' \
    -e 's/np\.bool\b/bool/g' \
    -e 's/np\.int\b/int/g' \
    -e 's/np\.float\b/float/g' \
    -e 's/np\.complex\b/complex/g' \
    -e 's/\.iteritems()/.items()/g' \
    {} +
echo "Patch applied."

echo "=== Verifying installation ==="
python -c "import pyscenic; print('pySCENIC', pyscenic.__version__, 'OK')"
python -c "import arboreto; print('arboreto OK')"
python -c "import loompy; print('loompy OK')"

echo ""
echo "=== Done ==="
echo "In future sessions, activate with:"
echo "  module load python/3.11.5 arrow/17.0.0 && source $ENV_DIR/bin/activate"
