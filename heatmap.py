import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Example data similar to what might be extracted from your analysis
data = {
    'C': [1.0, 0.981, 0.981, 0.725, 0.725, 0.923],
    'J': [0.974, 1.0, 0.999, 0.604, 0.604, 0.842],
    'SD': [0.974, 0.999, 1.0, 0.604, 0.604, 0.842],
    'SS': [0.732, 0.615, 0.615, 1.0, 0.999, 0.926],
    'PMI': [0.677, 0.565, 0.566, 0.938, 1.0, 0.926],
    'NPMI': [0.869, 0.776, 0.777, 0.935, 0.950, 1.0]
}

df = pd.DataFrame(data, index=['C', 'J', 'SD', 'SS', 'PMI', 'NPMI'])

# Set up the matplotlib figure
plt.figure(figsize=(10, 8))

# Create a heatmap with both Pearson's r and Spearman's rho
sns.set_theme(style="white")
ax = sns.heatmap(df, annot=True, cmap='coolwarm', vmin=0.6, vmax=1)

# Customize the plot
plt.title('Heatmap showing Pearson’s and Spearman’s pairwise correlations')
plt.show()