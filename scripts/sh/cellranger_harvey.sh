#!/bin/bash
#SBATCH --job-name=cellranger_harvey
#SBATCH --time=12:00:00
#SBATCH --mem=64G
#SBATCH --cpus-per-task=16
#SBATCH --output=/home/lifangy6/scratch/BINF6999/scripts/cellranger_%j.log
#SBATCH --mail-user=fangyi.li.galaxy@gmail.com
#SBATCH --mail-type=END,FAIL
#
# Step 3 of 3 in obtaining the Harvey 2019 count matrix (Stage 2).
# Runs Cell Ranger 10.0.0 `count` against the mm10-2020-A reference to turn the
# FASTQs into a filtered feature-barcode matrix.
#
# --create-bam false: the BAM is not needed downstream and skipping it saves
# several hours and ~50 GB.
#
# Usage: sbatch cellranger_harvey.sh
# Prerequisite: fasterq_harvey.sh completed. --sample=harvey means Cell Ranger
#         looks for harvey_S*_L*_R*_001.fastq.gz, so the SRR9087252_1/2/3.fastq.gz
#         files fasterq-dump emits must be renamed to that convention first.
# Output: harvey_output/outs/filtered_feature_bc_matrix/ — copy to
#         data/Harvey_scRNA-seq/filtered_feature_bc_matrix/ locally, then run
#         scripts/ipynb/03_harvey2019_qc_clustering.ipynb.

CELLRANGER=/home/lifangy6/scratch/BINF6999/tools/cellranger-10.0.0/cellranger

$CELLRANGER count \
    --id=harvey_output \
    --create-bam false \
    --transcriptome=/home/lifangy6/scratch/BINF6999/data/refdata-gex-mm10-2020-A \
    --fastqs=/home/lifangy6/scratch/BINF6999/data/Harvey_scRNA-seq \
    --sample=harvey \
    --localcores=16 \
    --localmem=64

