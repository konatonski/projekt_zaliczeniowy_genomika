#!/bin/bash
#SBATCH --job-name=mafft_align
#SBATCH --output=../logs/align_%j.log
#SBATCH --error=../logs/align_%j.err
#SBATCH --partition=common
#SBATCH --qos=kn418177_common
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=20
#SBATCH --time=08:00:00

echo "job started on $(hostname) at $(date)"

# assumes you submit this from 'processing' folder
time python3 run_align_inplace.py

echo "job ended at $(date)"