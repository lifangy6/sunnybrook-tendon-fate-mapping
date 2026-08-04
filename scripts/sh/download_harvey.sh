#!/bin/bash
#SBATCH --job-name=harvey_download
#SBATCH --time=06:00:00
#SBATCH --mem=16G
#SBATCH --cpus-per-task=8
#SBATCH --output=/home/lifangy6/scratch/BINF6999/scripts/harvey_download_%j.log
#
# Step 1 of 3 in obtaining the Harvey 2019 count matrix (Stage 2).
# Downloads SRR9087252 (PRJNA506218 — uninjured adult mouse patellar tendon)
# from the SRA and converts it to gzipped FASTQ.
#
# The fasterq-dump call here omits --include-technical, so it does NOT emit the
# read carrying the 10x cell barcode + UMI. Run fasterq_harvey.sh afterwards to
# redo the dump with that read included; Cell Ranger needs it.
#
# Usage: sbatch download_harvey.sh
# Next:  fasterq_harvey.sh, then cellranger_harvey.sh

module load sra-toolkit

DATA_DIR=/home/lifangy6/scratch/BINF6999/data/Harvey_scRNA-seq

mkdir -p $DATA_DIR
cd $DATA_DIR

prefetch SRR9087252 --max-size 30GB

fasterq-dump ./SRR9087252/ \
    --split-files \
    --threads 8 \
    --outdir .

pigz -p 8 SRR9087252*.fastq
