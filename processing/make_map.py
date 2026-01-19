import os
import glob

# config
in_dir = "../raw_gene_families"
out_map = "../trees/map.txt"

mapping = {}

print("scanning files...")
for fpath in glob.glob(os.path.join(in_dir, "*.fasta")):
    with open(fpath) as f:
        for line in f:
            if line.startswith(">"):
                full_id = line.strip()[1:]
                
                #extract species name
                #in format: Species_Name_WP_12345
                if "_WP_" in full_id:
                    species = full_id.split("_WP_")[0]
                else:
                    # fallback: split at last underscore
                    species = full_id.rsplit("_", 1)[0]
                
                mapping[full_id] = species

# write map file
with open(out_map, "w") as out:
    for fid, sp in mapping.items():
        out.write(f"{fid}\t{sp}\n")

print(f"mapped {len(mapping)} sequences to {len(set(mapping.values()))} species")
print(f"saved to {out_map}")