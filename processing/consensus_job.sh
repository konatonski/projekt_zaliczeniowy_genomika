#!/bin/bash
#SBATCH --job-name=consensus
#SBATCH --output=../logs/consensus_%j.log
#SBATCH --partition=common
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=00:30:00

# config
iqtree="./iqtree-2.2.2.6-Linux/bin/iqtree2"
in_trees="../trees/genetrees/all_no_paralog_trees.newick"
out_dir="../trees/consensus_trees"

mkdir -p $out_dir
echo "starting consensus..."

# greedy (extended majority)
$iqtree -con -t $in_trees --prefix ${out_dir}/greedy --quiet
mv ${out_dir}/greedy.contree ${out_dir}/greedy.tree

# majority (>50%)
$iqtree -con -t $in_trees -minsup 0.5 --prefix ${out_dir}/majority --quiet
mv ${out_dir}/majority.contree ${out_dir}/majority.tree

# strict (100%)
$iqtree -con -t $in_trees -minsup 1.0 --prefix ${out_dir}/strict --quiet
mv ${out_dir}/strict.contree ${out_dir}/strict.tree

# cleanup
rm ${out_dir}/*.log

echo "done"