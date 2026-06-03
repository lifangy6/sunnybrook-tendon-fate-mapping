#!/bin/bash
#SBATCH --job-name=cellranger_harvey
#SBATCH --time=12:00:00
#SBATCH --mem=64G
#SBATCH --cpus-per-task=16
#SBATCH --output=/home/lifangy6/scratch/BINF6999/scripts/cellranger_%j.log
#SBATCH --mail-user=fangyi.li.galaxy@gmail.com
#SBATCH --mail-type=END,FAIL

CELLRANGER=/home/lifangy6/scratch/BINF6999/tools/cellranger-10.0.0/cellranger

$CELLRANGER count \
    --id=harvey_output \
    --create-bam false \
    --transcriptome=/home/lifangy6/scratch/BINF6999/data/refdata-gex-mm10-2020-A \
    --fastqs=/home/lifangy6/scratch/BINF6999/data/Harvey_scRNA-seq \
    --sample=harvey \
    --localcores=16 \
    --localmem=64

