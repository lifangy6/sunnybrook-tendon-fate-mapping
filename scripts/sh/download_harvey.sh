#!/bin/bash
#SBATCH --job-name=harvey_download
#SBATCH --time=06:00:00
#SBATCH --mem=16G
#SBATCH --cpus-per-task=8
#SBATCH --output=/home/lifangy6/scratch/BINF6999/scripts/harvey_download_%j.log

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
