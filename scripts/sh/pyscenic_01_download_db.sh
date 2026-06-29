#!/bin/bash
#SBATCH --job-name=pyscenic_download_db
#SBATCH --time=03:00:00
#SBATCH --mem=8G
#SBATCH --cpus-per-task=2
#SBATCH --output=/home/lifangy6/scratch/BINF6999/scripts/logs/pyscenic_download_%j.log
#SBATCH --mail-user=fangyi.li.galaxy@gmail.com
#SBATCH --mail-type=END,FAIL
#
# Downloads mm10 cisTarget databases and mouse TF list required by pySCENIC.
# Only needs to be run once. Files are ~1.5 GB total.
#
# Usage: sbatch pyscenic_01_download_db.sh

set -euo pipefail

DB_DIR=/home/lifangy6/scratch/BINF6999/data/pyscenic/db
mkdir -p $DB_DIR
mkdir -p /home/lifangy6/scratch/BINF6999/scripts/logs

echo "=== Downloading mm10 cisTarget databases to $DB_DIR ==="

# Promoter-proximal (500 bp up / 100 bp down from TSS)
wget -c -P $DB_DIR \
    https://resources.aertslab.org/cistarget/databases/mus_musculus/mm10/refseq_r80/mc_v10_clust/gene_based/mm10_500bp_up_100bp_down_full_tx_v10_clust.genes_vs_motifs.rankings.feather

# Broader regulatory regions (10 kbp up / 10 kbp down)
wget -c -P $DB_DIR \
    https://resources.aertslab.org/cistarget/databases/mus_musculus/mm10/refseq_r80/mc_v10_clust/gene_based/mm10_10kbp_up_10kbp_down_full_tx_v10_clust.genes_vs_motifs.rankings.feather

# Motif-to-TF annotation table (v9; v10 URL returns 404 on aertslab server)
wget -c -P $DB_DIR \
    https://resources.aertslab.org/cistarget/motif2tf/motifs-v9-nr.mgi-m0.001-o0.0.tbl

# Mouse transcription factor list
wget -c -O $DB_DIR/mm_mgi_tfs.txt \
    https://raw.githubusercontent.com/aertslab/pySCENIC/master/resources/mm_mgi_tfs.txt

echo "=== Downloaded files ==="
ls -lh $DB_DIR
echo "=== Done ==="
