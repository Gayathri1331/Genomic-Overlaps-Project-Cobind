import subprocess
import pandas as pd
import os

# Define input files
query_file = "CTCF_peaks.bed"  # Replace with the path to your query BED file
reference_file = "TF_peaks.bed"  # Replace with the path to your reference BED file

# Define metrics and output file names
metrics = {
    "overlap": "overlap_results.csv",
    "jaccard": "jaccard_results.csv",
    "dice": "dice_results.csv",
    "simpson": "simpson_results.csv",
    "pmi": "pmi_results.csv",
    "npmi": "npmi_results.csv"
}

# Step 1: Run Cobind commands for all metrics
print("Running Cobind metrics...")
for metric, output_file in metrics.items():
    try:
        print(f"Calculating {metric}...")
        # Construct the Cobind command
        command = [
            "python3", "./bin/cobind.py", metric,
            query_file, reference_file, "--save"
        ]
        # Run the command
        with open(output_file, "w") as outfile:
            subprocess.run(command, stdout=outfile, check=True)
        print(f"{metric} completed. Results saved to {output_file}.")
    except subprocess.CalledProcessError as e:
        print(f"Error running {metric}: {e}")
        exit(1)

# Step 2: Merge results
print("\nMerging results...")

# Load the first result file
merged_df = pd.read_csv(metrics["overlap"])
merged_df.rename(columns={"score": "C"}, inplace=True)

# Merge subsequent results
for metric, output_file in list(metrics.items())[1:]:
    df = pd.read_csv(output_file)
    metric_column = {
        "jaccard": "J",
        "dice": "SD",
        "simpson": "SS",
        "pmi": "PMI",
        "npmi": "NPMI"
    }.get(metric, metric)
    df.rename(columns={"score": metric_column}, inplace=True)
    merged_df = merged_df.merge(df, on="TF")  # Replace "TF" with the appropriate merge key if needed

# Save merged results
merged_output_file = "collocation_metrics_results.csv"
merged_df.to_csv(merged_output_file, index=False)
print(f"Merged results saved to {merged_output_file}.")

