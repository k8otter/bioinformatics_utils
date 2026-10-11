#!/bin/bash
#
#SBATCH -p cpu
#SBATCH -n 1
#SBATCH --cpus-per-task=20
#SBATCH --mem=120G
#SBATCH --time=12:00:00
#SBATCH --job-name=phylo
#SBATCH --mail-user=kxo233@case.edu
#SBATCH --mail-type=ALL
#SBATCH --account=PDS0375

#
#################################################

# Script by Jorge L. Perez-Moreno, Ph.D.   jperezmoreno@umass.edu
# Adapted by Kate Otter, Ph.D.


### Set up environment with your conda library path
export LD_LIBRARY_PATH=/users/PDS0375/k8otter/.miniconda3/lib/:$LD_LIBRARY_PATH
conda activate bioinf

### Variables to adjust:

### ADJUST according to computational resources available
CPU="20"

### Variables to adjust
PROJECT="PDF"
INPUT="${PROJECT}/PDF_20260922_alignment_ready.fa"

#############################

### Use the allocated CPUs and the date the job starts
CPU="${SLURM_CPUS_PER_TASK:-20}"
RUN_DATE=$(date +%Y%m%d)

### Output directory and shared filename prefix
OUTDIR="${PROJECT}"
PREFIX="${OUTDIR}/${PROJECT}_${RUN_DATE}"
mkdir -p "$OUTDIR"

### Align sequences
mafft --genafpair --maxiterate 10000 --thread "$CPU" \
    "$INPUT" > "${PREFIX}_alignment.fa"

### Sanitize FASTA headers
cut -d ' ' -f1 "${PREFIX}_alignment.fa" \
    > "${PREFIX}_aligned.fa"

### Trim alignment gaps
clipkit "${PREFIX}_aligned.fa" -m smart-gap

### Infer phylogeny
iqtree -s "${PREFIX}_aligned.fa.clipkit" \
    -pre "${PREFIX}_trimmed" \
    -T "$CPU" \
    -m TESTNEW -msub nuclear \
    -bb 1000 -bnni -abayes