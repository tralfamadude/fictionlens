import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
from data_interface import get_paragraphs_without_embedding

# Check if an argument was provided
if len(sys.argv) > 1:
    fiction = sys.argv[1]  # Get the fiction name from the first command-line argument
else:
    print("No fiction name provided. Using default 'Great Gatsby'.")
    fiction = "Great Gatsby"  # Default value if no argument is provided

fictionname = "_".join(fiction.split())
filename = f'../data/{fictionname}.annotated.jsonl'

paragraphs = get_paragraphs_without_embedding(filename)

# Step 2: Calculate the average sentiment per 100 paragraphs
average_sentiments = []
batch_size = 100
for i in range(0, len(paragraphs), batch_size):
    batch = paragraphs[i:i + batch_size]
    total_sentiment = 0
    valid_items = 0
    for item in batch:
        if 'sentiment' in item['annotation']:
            total_sentiment += item['annotation']['sentiment']
            valid_items += 1
    if valid_items > 0:
        average_sentiments.append(total_sentiment / valid_items)

# Gatsby-themed color gradient from gold to black
cmap = LinearSegmentedColormap.from_list("Gatsby", ["gold", "black"])

# Normalize the data to [0, 1] for the color mapping
norm = plt.Normalize(min(average_sentiments), max(average_sentiments))

# Prepare data for LineCollection
points = np.array([np.arange(len(average_sentiments)), average_sentiments]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

# Create a LineCollection with the Gatsby color map
lc = LineCollection(segments, cmap=cmap, norm=norm, linewidth=2)
# Set the values used for colormapping
lc.set_array(np.array(average_sentiments))

plt.figure(figsize=(10, 6))
plt.gca().add_collection(lc)
plt.xlim(0, len(average_sentiments) - 1)
plt.ylim(min(average_sentiments), max(average_sentiments))

# Great Gatsby themed styling
plt.title(f'{fiction}: Sentiment Journey', fontsize=20, fontweight='bold', color='darkgreen')
plt.xlabel('Segment (per 100 paragraphs)', fontsize=14, fontstyle='italic', color='darkslategray')
plt.ylabel('Average Sentiment', fontsize=14, fontstyle='italic', color='darkslategray')
plt.xticks(fontsize=10, color='darkslategray')
plt.yticks(fontsize=10, color='darkslategray')
plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

folder_path = 'visualizations'

# Check if the folder exists, and if not, create it
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

file_path = os.path.join(folder_path, f'{fictionname}_sentiment.png')
plt.savefig(file_path)

plt.show()
