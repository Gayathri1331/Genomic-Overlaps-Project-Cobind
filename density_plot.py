import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Generate Z-scores
x = np.linspace(-10, 10, 1000)
y = norm.pdf(x, 0, 1)

# Plot the density
plt.fill_between(x, y, color='green', alpha=0.6)

# Highlight specific Z-scores
highlighted_z_scores = [-6, -4.8, -2, 2, 4.8, 6]  # Example Z-scores for annotation
for z in highlighted_z_scores:
    plt.axvline(z, color='black', linestyle='--')

# Annotate genes or elements
genes = ['RAD21', 'SMC3', 'SMC1A', 'TRIM22', 'STAG1', 'STAG2']
for i, gene in enumerate(genes):
    plt.text(8, 0.15 - i * 0.02, gene, color='red', fontsize=10)

# Add labels and title
plt.xlabel('Combined Z-score')
plt.ylabel('Density')
plt.title('Density Plot')

# Show the plot
plt.show()

