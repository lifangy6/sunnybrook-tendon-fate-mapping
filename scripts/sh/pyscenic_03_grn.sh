#!/bin/bash
#SBATCH --job-name=pyscenic_grn
#SBATCH --time=06:00:00
#SBATCH --mem=64G
#SBATCH --cpus-per-task=16
#SBATCH --array=0-1
#SBATCH --output=/home/lifangy6/scratch/BINF6999/scripts/logs/pyscenic_grn_%A_%a.log
#SBATCH --mail-user=fangyi.li.galaxy@gmail.com
#SBATCH --mail-type=END,FAIL
#
# Step 1 of pySCENIC: GRNBoost2 — infer TF-to-target co-expression network.
# Runs as a SLURM array: task 0 = Harvey, task 1 = Cherief.
#
# Usage: sbatch pyscenic_03_grn.sh
# Prerequisite: pyscenic_01_download_db.sh and pyscenic_02_prepare_loom.py completed.

set -euo pipefail

module load python/3.11.5
module load arrow/17.0.0
source /home/lifangy6/scratch/BINF6999/envs/pyscenic/bin/activate

DATASETS=("harvey" "cherief")
DATASET=${DATASETS[$SLURM_ARRAY_TASK_ID]}

BASE=/home/lifangy6/scratch/BINF6999/data/pyscenic
INPUT=$BASE/input/${DATASET}_tspc_tfap.loom
TF_LIST=$BASE/db/mm_mgi_tfs.txt
OUTPUT=$BASE/output/${DATASET}_adjacencies.tsv

mkdir -p $BASE/output

echo "=== GRNBoost2: $DATASET ==="
echo "Input:  $INPUT"
echo "Output: $OUTPUT"
echo "Cores:  $SLURM_CPUS_PER_TASK"

pyscenic grn \
    --num_workers $SLURM_CPUS_PER_TASK \
    --output $OUTPUT \
    --method grnboost2 \
    --gene_attribute var_names \
    --cell_id_attribute obs_names \
    $INPUT \
    $TF_LIST

echo "=== Done: $DATASET GRN ==="
ls -lh $OUTPUT
