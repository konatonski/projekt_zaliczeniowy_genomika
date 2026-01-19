import os
import glob
import subprocess
from multiprocessing import Pool, cpu_count

# config
fasttree_bin = "../FastTree" 

# input directories
filt_in_dir = "../filtered_gene_families"
raw_in_dir  = "../raw_gene_families"

# output directories
filt_out_dir = "../trees/genetrees/filtered_gene_families"
raw_out_dir  = "../trees/genetrees/raw_gene_families"

# ensure output dirs exist
os.makedirs(filt_out_dir, exist_ok=True)
os.makedirs(raw_out_dir, exist_ok=True)

def count_seqs_in_filtered(fpath):
    with open(fpath) as f:
        cnt = sum(1 for line in f if line.startswith(">"))
    return (fpath, cnt)

def run_fasttree_on_pair(filt_fpath):
    fname = os.path.basename(filt_fpath)
    
    #filtered
    filt_tree_path = os.path.join(filt_out_dir, fname.replace(".fasta", ".tree"))
    
    if not (os.path.exists(filt_tree_path) and os.path.getsize(filt_tree_path) > 0):
        cmd = f"{fasttree_bin} -quiet {filt_fpath} > {filt_tree_path}"
        subprocess.run(cmd, shell=True)

    #raw
    raw_fpath = os.path.join(raw_in_dir, fname)
    raw_tree_path = os.path.join(raw_out_dir, fname.replace(".fasta", ".tree"))
    
    if os.path.exists(raw_fpath):
        if not (os.path.exists(raw_tree_path) and os.path.getsize(raw_tree_path) > 0):

            cmd = f"{fasttree_bin} -quiet {raw_fpath} > {raw_tree_path}"
            subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    # gather files from filtered dir
    filt_files = glob.glob(os.path.join(filt_in_dir, "*.fasta"))
    print(f"checking {len(filt_files)} families...")

    # count sequences in filtered files
    with Pool(cpu_count()) as p:
        results = p.map(count_seqs_in_filtered, filt_files)

    # filter logic: if filtered_file < 4 seqs, discard BOTH
    valid_files = [f for f, n in results if n >= 4]
    discarded = len(filt_files) - len(valid_files)

    print(f"total: {len(filt_files)}")
    print(f"discarded (<4 seqs in filtered): {discarded}")
    print(f"accepted: {len(valid_files)}")
    print("starting tree inference for both sets...")

    # run fasttree
    n = len(valid_files)
    with Pool(cpu_count()) as p:
        for i, _ in enumerate(p.imap_unordered(run_fasttree_on_pair, valid_files), 1):
            if i % 100 == 0: 
                print(f"processing family {i}/{n}")
    
    print("done")