#!/bin/bash
#SBATCH --job-name=tf_cobind_batch         # Job name
#SBATCH --output=batch_%A_%a.log          # Standard output log
#SBATCH --error=batch_%A_%a.err           # Standard error log
#SBATCH --ntasks=1                        # Number of tasks (single task)
#SBATCH --time=04:00:00                   # Maximum runtime (adjust as needed)
#SBATCH --mem=64G                         # Memory per job (adjust based on your requirements)
#SBATCH --array=1-19                      # Array job for batch IDs (adjust as needed)

# Load necessary modules (if your cluster requires it, uncomment below)
# module load miniconda

# Use Python from Miniconda installation
PYTHON_PATH=~/miniconda3/bin/python3

# Define the number of lines per batch (adjust if needed)
LINES_PER_BATCH=10000000

# Calculate the start and end lines for this batch
START_LINE=$(( (SLURM_ARRAY_TASK_ID - 1) * LINES_PER_BATCH + 1 ))
END_LINE=$(( SLURM_ARRAY_TASK_ID * LINES_PER_BATCH ))

# Ensure the end line doesn't exceed the total number of lines in TF_peaks.bed
TOTAL_LINES=$(wc -l < TF_peaks.bed)
if [ $END_LINE -gt $TOTAL_LINES ]; then
  END_LINE=$TOTAL_LINES
fi

# Extract the batch lines into a temporary file
sed -n "${START_LINE},${END_LINE}p" TF_peaks.bed > tf_batch_${SLURM_ARRAY_TASK_ID}.bed

# Process all six Cobind metrics for this batch
for METRIC in overlap jaccard dice simpson pmi npmi; do
  echo "Processing $METRIC for batch ${SLURM_ARRAY_TASK_ID}..."
  $PYTHON_PATH ./bin/cobind.py $METRIC CTCF_peaks.bed tf_batch_${SLURM_ARRAY_TASK_ID}.bed --save > tf_batch_${SLURM_ARRAY_TASK_ID}_${METRIC}_results.csv
done

# Clean up the temporary batch file after processing
rm tf_batch_${SLURM_ARRAY_TASK_ID}.bed

echo "Batch ${SLURM_ARRAY_TASK_ID} completed successfully."

