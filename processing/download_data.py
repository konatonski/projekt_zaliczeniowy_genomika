import os
import pandas as pd
import urllib.request
from Bio import Entrez

# CONFIG
input_csv = "accessions.csv"
output_dir = "downloads"
Entrez.email = "kornelnatonski@gmail.com" # CHANGE THIS

os.makedirs(output_dir, exist_ok=True)
df = pd.read_csv(input_csv)
failed = []
count = 0

print("Downloading...")

for acc in df['Accession']:
    try:
        # search assembly
        handle = Entrez.esearch(db="assembly", term=acc, retmax=1)
        record = Entrez.read(handle)
        
        # get ftp link
        id = record['IdList'][0]
        summary = Entrez.read(Entrez.esummary(db="assembly", id=id))
        data = summary['DocumentSummarySet']['DocumentSummary'][0]
        ftp_path = data.get('FtpPath_RefSeq') or data.get('FtpPath_GenBank')
        
        # construct url
        fname = os.path.basename(ftp_path) + "_protein.faa.gz"
        url = f"{ftp_path}/{fname}"
        
        # download
        urllib.request.urlretrieve(url, os.path.join(output_dir, fname))
        count += 1
        
    except Exception:
        failed.append(acc)

print(f"successfully downloaded {count} files")
if failed:
    print(f"{len(failed)} downloads failed: {failed}")