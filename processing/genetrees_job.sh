#!/bin/bash
#SBATCH --job-name=fasttree
#SBATCH --output=../logs/tree_%j.log
#SBATCH --error=../logs/tree_%j.err
#SBATCH --partition=common
#SBATCH --qos=kn418177_common
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=20
#SBATCH --time=04:00:00

echo "job started on $(hostname) at $(date)"
time python3 run_trees.py
echo "job ended at $(date)"