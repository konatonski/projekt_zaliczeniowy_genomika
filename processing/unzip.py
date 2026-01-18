import os
import gzip
import shutil
import pandas as pd

# config
dir_down = "downloads"
dir_data = "../data"
csv_file = "accessions.csv"

os.makedirs(dir_data, exist_ok=True)

# load mapping
df = pd.read_csv(csv_file)
acc_map = dict(zip(df['Accession'], df['Species']))

print("unpacking and renaming...")

count = 0
for fname in os.listdir(dir_down):
    if not fname.endswith(".gz"): continue

    # find accession match
    found_acc = None
    for acc in acc_map:
        if fname.startswith(acc):
            found_acc = acc
            break
    
    if found_acc:
        # clean name: Bifidobacterium longum -> Bifidobacterium_longum.faa
        name = acc_map[found_acc].replace(" ", "_").replace(".", "") + ".faa"
        in_path = os.path.join(dir_down, fname)
        out_path = os.path.join(dir_data, name)

        # unzip
        with gzip.open(in_path, 'rb') as f_in, open(out_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        
        count += 1
    else:
        print(f"no match for {fname}")

print(f"unpacked {count} files")