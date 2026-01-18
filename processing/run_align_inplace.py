import os
import glob
import subprocess
import shutil
from multiprocessing import Pool, cpu_count

# config (relative to 'processing' folder)
mafft_bin = "../mafft-linux64/mafft.bat"
dirs = ["../filtered_gene_families", "../raw_gene_families"]

def align_inplace(fpath):
    # safety: write to temp first
    tmp = fpath + ".tmp"
    
    # run mafft
    cmd = f"{mafft_bin} --auto --quiet {fpath} > {tmp}"
    
    try:
        subprocess.run(cmd, shell=True, check=True)
        # overwrite original
        shutil.move(tmp, fpath)
    except Exception:
        # cleanup if failed
        if os.path.exists(tmp): os.remove(tmp)

if __name__ == "__main__":
    files = []
    for d in dirs:
        # use absolute paths to avoid confusion
        abs_d = os.path.abspath(d)
        files.extend(glob.glob(os.path.join(abs_d, "*.fasta")))

    print(f"aligning {len(files)} files inplace on {cpu_count()} cores...")
    
    with Pool(cpu_count()) as p:
        p.map(align_inplace, files)
        
    print("done")