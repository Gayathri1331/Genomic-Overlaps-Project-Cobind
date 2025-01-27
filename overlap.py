from matplotlib_venn import venn3

# Example data: Top TFs from three metrics
set1 = set(data[data["C"] > threshold]["TF"])
set2 = set(data[data["J"] > threshold]["TF"])
set3 = set(data[data["SD"] > threshold]["TF"])

# Venn diagram
venn3([set1, set2, set3], ('C', 'J', 'SD'))
plt.title("Overlap of Top TFs by Metrics")
plt.show()

