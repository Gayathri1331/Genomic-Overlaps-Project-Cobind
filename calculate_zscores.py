import pandas as pd

# Load the combined results
data = pd.read_csv("final_combined_tf_results.csv")

# List of metrics to normalize
metrics = ["C", "J", "SD", "SS", "PMI", "NPMI"]

# Calculate Z-scores for each metric
for metric in metrics:
    data[f"{metric}_z"] = (data[metric] - data[metric].mean()) / data[metric].std()

# Calculate the combined Z-score as the average of individual Z-scores
data["Combined_Z"] = data[[f"{metric}_z" for metric in metrics]].mean(axis=1)

# Save the results with Z-scores
data.to_csv("final_combined_tf_results_with_zscores.csv", index=False)
print("Results with Z-scores saved to final_combined_tf_results_with_zscores.csv.")

