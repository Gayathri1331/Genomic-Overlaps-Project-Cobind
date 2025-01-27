import pandas as pd

# Load merged results for each metric
overlap = pd.read_csv("final_tf_overlap_results.csv").rename(columns={"score": "C"})
jaccard = pd.read_csv("final_tf_jaccard_results.csv").rename(columns={"score": "J"})
dice = pd.read_csv("final_tf_dice_results.csv").rename(columns={"score": "SD"})
simpson = pd.read_csv("final_tf_simpson_results.csv").rename(columns={"score": "SS"})
pmi = pd.read_csv("final_tf_pmi_results.csv").rename(columns={"score": "PMI"})
npmi = pd.read_csv("final_tf_npmi_results.csv").rename(columns={"score": "NPMI"})

# Merge all metrics on the common key (e.g., transcription factor name)
final_df = overlap.merge(jaccard, on="TF").merge(dice, on="TF").merge(simpson, on="TF").merge(pmi, on="TF").merge(npmi, on="TF")

# Save the final combined results
final_df.to_csv("final_combined_tf_results.csv", index=False)
print("Final combined results saved to final_combined_tf_results.csv.")

