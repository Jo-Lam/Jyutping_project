import pandas as pd

# Load the uploaded data to inspect its structure
file_path = 'data/20240806_cleandata.csv'
data = pd.read_csv(file_path)

# Display the first few rows of the dataset and its structure
data.head(), data.info()

data['forename_pinyin_char2_t'] = data['forename_pinyin_char2_t'].fillna(0).astype(int)
data['forename_jyutping_char2_t'] = data['forename_jyutping_char2_t'].fillna(0).astype(int)

from itertools import combinations

# Function to calculate recall and reduction ratio
def evaluate_blocking_with_precision(data, ground_truth_col, block_col):
    # True matches (pairs in the same ground truth block)
    ground_truth_pairs = {
        frozenset(pair)
        for block in data[ground_truth_col].unique()
        for pair in combinations(data[data[ground_truth_col] == block].index, 2)
    }

    # Candidate pairs (pairs in the same blocking rule block)
    candidate_pairs = {
        frozenset(pair)
        for block in data[block_col].unique()
        for pair in combinations(data[data[block_col] == block].index, 2)
    }

    # Metrics
    true_positives = len(ground_truth_pairs & candidate_pairs)
    recall = true_positives / len(ground_truth_pairs) if ground_truth_pairs else 0
    precision = true_positives / len(candidate_pairs) if candidate_pairs else 0
    reduction_ratio = 1 - (len(candidate_pairs) / (len(data) * (len(data) - 1) / 2))

    return recall, precision, reduction_ratio


# define blocking

# jyutping
data['block_rule0'] = data['中文姓']
data['block_rule1'] = data['surname_jyutping_char1_v'] + data['surname_jyutping_char1_t'].astype(str)
data['block_rule2'] = data['surname_pinyin_char1_v'] + data['surname_pinyin_char1_t'].astype(str) 
data['block_rule3'] = data['surname_pinyin_char1_v'] 
data['block_rule4'] = data['surname']

data['block_rule5'] = data['surname_jyutping_char1_v'].str[:2] + data['surname_jyutping_char1_t'].astype(str)
data['block_rule6'] = data['surname_jyutping_char1_v'].str[:2] 
data['block_rule7'] =  data['surname_jyutping_char1_t'].astype(str)

data['block_rule8'] = data['surname_pinyin_char1_v'].str[:2] + data['surname_pinyin_char1_t'].astype(str) 
data['block_rule9'] = data['surname_pinyin_char1_v'].str[:2]
data['block_rule10'] = data['surname_pinyin_char1_t'].astype(str) 


results = []

for rule in ['block_rule1', 'block_rule2', 'block_rule3', 'block_rule4', 'block_rule5', 'block_rule6', 'block_rule7', 'block_rule8', 'block_rule9', 'block_rule10']:
    recall, precision, reduction_ratio = evaluate_blocking_with_precision(data, 'block_rule0', rule)
    results.append({'Blocking Rule': rule, 'Recall': recall, 'Precision': precision, 'Reduction Ratio': reduction_ratio})

# Convert results to DataFrame for better visualization
results_df = pd.DataFrame(results)
print(results_df)

# Plot Recall vs. Precision graph
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

color_mapping = {
    'block_rule4': 'green',    # HKG-romanisation
    'block_rule1': 'blue',   # Jyutping
    'block_rule5': 'blue',
    'block_rule6': 'blue',
    'block_rule7': 'blue',
    'block_rule2': 'orange',  # Pinyin
    'block_rule3': 'orange',
    'block_rule7': 'orange',
    'block_rule8': 'orange',
    'block_rule9': 'orange'
}

legend_labels = {
    'orange': 'HKG-Romanisation',
    'blue': 'Jyutping',
    'green': 'Pinyin'
}

# Create custom legend patches
legend_patches = [
    mpatches.Patch(color=color, label=label)
    for color, label in legend_labels.items()
]
# Assign colors to each blocking rule
results_df['Color'] = results_df['Blocking Rule'].map(color_mapping)

# Plot Recall vs. Precision graph with the updated labels and color coding
plt.figure(figsize=(8, 6))
for color, group in results_df.groupby('Color'):
    plt.scatter(group['Recall'], group['Precision'], s=100, alpha=0.8, label=f'{color.capitalize()} Group')
    for _, row in group.iterrows():
        plt.text(row['Recall'] + 0.01, row['Precision'], row['Blocking Rule'], fontsize=10)

# Add labels, title, legend, and grid
plt.title('Recall vs. Precision for Blocking Rules: Surnames', fontsize=14)
plt.xlabel('Recall', fontsize=12)
plt.ylabel('Precision', fontsize=12)
plt.yticks(np.arange(0,1.1,0.1))
plt.grid(True)
plt.legend(handles=legend_patches, title="Blocking Rule Categories", loc="lower left")
plt.show()

