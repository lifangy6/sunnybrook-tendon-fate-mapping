#!/bin/bash
#SBATCH --job-name=harvey_fasterq
#SBATCH --time=03:00:00
#SBATCH --mem=16G
#SBATCH --cpus-per-task=8
#SBATCH --output=/home/lifangy6/scratch/BINF6999/scripts/harvey_fasterq_%j.log

module load sra-toolkit

cd /home/lifangy6/scratch/BINF6999/data/Harvey_scRNA-seq

fasterq-dump ./SRR9087252/ \
    --split-files \
    --include-technical \
    --threads 8 \
    --outdir .

pigz -p 8 SRR9087252_1.fastq SRR9087252_2.fastq
