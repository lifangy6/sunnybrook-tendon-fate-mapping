#!/bin/bash
#SBATCH --job-name=pyscenic_aucell
#SBATCH --time=02:00:00
#SBATCH --mem=32G
#SBATCH --cpus-per-task=8
#SBATCH --array=0-1
#SBATCH --output=/home/lifangy6/scratch/BINF6999/scripts/logs/pyscenic_aucell_%A_%a.log
#SBATCH --mail-user=fangyi.li.galaxy@gmail.com
#SBATCH --mail-type=END,FAIL
#
# Step 3 of pySCENIC: AUCell — score regulon activity per cell.
# Runs as a SLURM array: task 0 = Harvey, task 1 = Cherief.
# Output loom files contain per-cell AUC scores for every regulon.
#
# Usage: sbatch pyscenic_05_aucell.sh
# Prerequisite: pyscenic_04_ctx.sh completed.

set -euo pipefail

module load python/3.11.5
module load arrow/17.0.0
source /home/lifangy6/scratch/BINF6999/envs/pyscenic/bin/activate

DATASETS=("harvey" "cherief")
DATASET=${DATASETS[$SLURM_ARRAY_TASK_ID]}

BASE=/home/lifangy6/scratch/BINF6999/data/pyscenic
LOOM=$BASE/input/${DATASET}_tspc_tfap.loom
REGULONS=$BASE/output/${DATASET}_regulons.csv
OUTPUT=$BASE/output/${DATASET}_aucell.loom

echo "=== AUCell: $DATASET ==="
echo "Regulons: $REGULONS"
echo "Output:   $OUTPUT"

pyscenic aucell \
    $LOOM \
    $REGULONS \
    --output $OUTPUT \
    --num_workers $SLURM_CPUS_PER_TASK \
    --gene_attribute var_names \
    --cell_id_attribute obs_names

echo "=== Done: $DATASET AUCell ==="
ls -lh $OUTPUT

echo ""
echo "=== Transfer results back to local machine ==="
echo "Run from local project root:"
echo "  scp lifangy6@nibi.alliancecan.ca:$BASE/output/${DATASET}_regulons.csv data/pyscenic/"
echo "  scp lifangy6@nibi.alliancecan.ca:$BASE/output/${DATASET}_aucell.loom data/pyscenic/"
