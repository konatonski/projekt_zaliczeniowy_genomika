import subprocess
import multiprocessing

input_file = "all_proteins_combined.fasta"
output_prefix = "mmseqs_output"
tmp_dir = "tmp_mmseqs"
threads = multiprocessing.cpu_count()

print(f"running mmseqs on {threads} CPU cores")

cmd = [
    "./mmseqs/bin/mmseqs", "easy-cluster",
    input_file,
    output_prefix,
    tmp_dir,
    "--min-seq-id", "0.5",
    "-c", "0.8",
    "--cov-mode", "0",
    "--threads", str(threads),
    "--remove-tmp-files", "1"
]

try:
    #no capture_output=True, so it prints to terminal in real-time
    subprocess.run(cmd, check=True)
    print("\n" + "="*30)
    print("CLUSTERING COMPLETE")
    print(f"results saved to: {output_prefix}_cluster.tsv")

except subprocess.CalledProcessError as e:
    print(f"Error running MMseqs2: {e}")