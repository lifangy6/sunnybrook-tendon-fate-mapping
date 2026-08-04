#!/bin/bash
#SBATCH --job-name=harvey_fasterq
#SBATCH --time=03:00:00
#SBATCH --mem=16G
#SBATCH --cpus-per-task=8
#SBATCH --output=/home/lifangy6/scratch/BINF6999/scripts/harvey_fasterq_%j.log
#
# Step 2 of 3 in obtaining the Harvey 2019 count matrix (Stage 2).
# Re-runs fasterq-dump on the SRA archive already fetched by download_harvey.sh,
# this time with --include-technical so the 10x barcode/UMI read is emitted too.
# Without it Cell Ranger sees only the cDNA read and cannot demultiplex cells.
#
# Overwrites the FASTQs written by download_harvey.sh — that is intended.
#
# Usage: sbatch fasterq_harvey.sh
# Prerequisite: download_harvey.sh completed (the SRR9087252/ directory exists).
# Next: cellranger_harvey.sh

module load sra-toolkit

cd /home/lifangy6/scratch/BINF6999/data/Harvey_scRNA-seq

fasterq-dump ./SRR9087252/ \
    --split-files \
    --include-technical \
    --threads 8 \
    --outdir .

pigz -p 8 SRR9087252_1.fastq SRR9087252_2.fastq
