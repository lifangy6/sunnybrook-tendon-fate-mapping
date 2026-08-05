#!/bin/bash
#SBATCH --job-name=pyscenic_ctx
#SBATCH --time=08:00:00
#SBATCH --mem=128G
#SBATCH --cpus-per-task=8
#SBATCH --array=0-1
#SBATCH --output=/home/lifangy6/scratch/BINF6999/scripts/logs/pyscenic_ctx_%A_%a.log
#SBATCH --mail-user=fangyi.li.galaxy@gmail.com
#SBATCH --mail-type=END,FAIL
#
# Step 2 of pySCENIC: cisTarget — prune co-expression modules by TF motif enrichment.
# Runs as a SLURM array: task 0 = Harvey, task 1 = Cherief.
# Uses both 500 bp and 10 kbp regulatory region databases.
#
# Usage: sbatch pyscenic_04_ctx.sh
# Prerequisite: pyscenic_03_grn.sh completed.

set -euo pipefail

module load python/3.11.5
module load arrow/17.0.0
source /home/lifangy6/scratch/BINF6999/envs/pyscenic/bin/activate

DATASETS=("harvey" "cherief")
DATASET=${DATASETS[$SLURM_ARRAY_TASK_ID]}

BASE=/home/lifangy6/scratch/BINF6999/data/pyscenic
ADJ=$BASE/output/${DATASET}_adjacencies.tsv
LOOM=$BASE/input/${DATASET}_tspc_tfap.loom
DB_500BP=$BASE/db/mm10_500bp_up_100bp_down_full_tx_v10_clust.genes_vs_motifs.rankings.feather
DB_10KBP=$BASE/db/mm10_10kbp_up_10kbp_down_full_tx_v10_clust.genes_vs_motifs.rankings.feather
MOTIFS=$BASE/db/motifs-v9-nr.mgi-m0.001-o0.0.tbl
OUTPUT=$BASE/output/${DATASET}_regulons.csv

echo "=== cisTarget: $DATASET ==="
echo "Adjacencies: $ADJ"
echo "Output:      $OUTPUT"

pyscenic ctx \
    $ADJ \
    $DB_500BP $DB_10KBP \
    --annotations_fname $MOTIFS \
    --expression_mtx_fname $LOOM \
    --mode "dask_multiprocessing" \
    --output $OUTPUT \
    --num_workers $SLURM_CPUS_PER_TASK \
    --mask_dropouts \
    --gene_attribute var_names \
    --cell_id_attribute obs_names

echo "=== Done: $DATASET regulons ==="
# The cisTarget CSV holds one row per TF x enriched-motif module, preceded by 3
# header lines — so its line count is NOT the regulon count. A regulon is one TF,
# whose target set is the union across that TF's motif rows, and that is what
# AUCell scores in the next step. Reporting `wc -l` here as "Regulon count" is
# what put an inflated figure (471/417 instead of 153/157) into the project
# write-ups; both quantities are now printed, each with an accurate label.
echo "TF x motif modules: $(( $(wc -l < $OUTPUT) - 3 ))"
echo "Regulons (unique TFs, = what AUCell will score): $(tail -n +4 $OUTPUT | cut -d, -f1 | sort -u | wc -l)"
ls -lh $OUTPUT
