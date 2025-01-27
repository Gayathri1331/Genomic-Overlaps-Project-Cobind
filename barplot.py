import pandas as pd
import matplotlib.pyplot as plt

# Load data from a TSV file into a DataFrame
# The file 'output.tsv' is assumed to contain tab-separated values
data = pd.read_csv('output.tsv', sep='\t')

# Define the metrics that will be plotted and assign colors for different protein types
metrics = ['NPMI', 'PMI', 'SS', 'SD', 'J', 'C', 'Zscore']
colors = {'Cohesin proteins': 'red', 'Other proteins': 'blue'}

# Function to classify protein types based on their names
def classify_protein(protein):
    # List of proteins categorized as "Cohesin proteins"
    cohesin_list = ['SMC3', 'RAD21', 'SMC1A', 'STAG1', 'STAG2']
    # Return the type of protein based on its presence in the cohesin list
    return 'Cohesin proteins' if protein in cohesin_list else 'Other proteins'

# Create a set of subplots, one for each metric
fig, axes = plt.subplots(nrows=1, ncols=len(metrics), figsize=(18, 8))

# Iterate over each metric to create individual plots
for i, metric in enumerate(metrics):
    # Sort the data by the current metric in descending order and select the top 20 entries
    sorted_data = data.sort_values(by=metric, ascending=False).head(20)

    # Determine the color of bars based on the protein type classification
    bar_colors = [colors[classify_protein(protein)] for protein in sorted_data['TF_name']]

    # Create a horizontal bar plot for each metric using the top 20 entries
    axes[i].barh(sorted_data['TF_name'], sorted_data[metric], color=bar_colors)
    axes[i].set_title(metric)  # Set title for each subplot with the metric name
    axes[i].invert_yaxis()  # Invert y-axis to have the highest values at the top

# Customize and add a legend to indicate what colors represent which protein types
legend_handles = [
    plt.Line2D([0], [0], color='red'),  # Red line for Cohesin proteins
    plt.Line2D([0], [0], color='blue')  # Blue line for Other proteins
]
fig.legend(legend_handles, ['Cohesin proteins', 'Other proteins'], loc='lower right', ncol=2)

# Adjust layout to ensure plots and legend do not overlap
plt.tight_layout(rect=[0.05, 0.05, 1, 0.95])

# Display the plot with all subplots and legend
plt.show()
