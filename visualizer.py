# import matplotlib.pyplot as plt

# def plot_scores(properties, scores):
#     """Plots property scores as a bar chart."""
#     names = [prop[0] for prop in scores]
#     values = [prop[1] for prop in scores]

#     plt.bar(names, values, color='skyblue')
#     plt.xlabel("Properties")
#     plt.ylabel("Scores")
#     plt.title("Property Comparisons")
#     plt.show()


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import List, Tuple

def plot_scores(properties: pd.DataFrame, scores: List[Tuple[str, float]]):
    """
    Create an enhanced bar chart of property scores
    
    :param properties: DataFrame of property details
    :param scores: List of (property_name, score) tuples
    """
    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    
    names = [prop[0] for prop in scores]
    values = [prop[1] for prop in scores]
    
    ax = sns.barplot(x=names, y=values, palette="deep")
    plt.title("RightHome.ai Property Recommendation Scores", fontsize=15)
    plt.xlabel("Properties", fontsize=12)
    plt.ylabel("Recommendation Score", fontsize=12)
    plt.xticks(rotation=45)
    
    # Add value labels on top of each bar
    for i, v in enumerate(values):
        ax.text(i, v, f'{v:.2f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('property_scores.png')
    plt.close()

def generate_heatmap(properties: pd.DataFrame, scores: List[Tuple[str, float]]):
    """
    Create a heatmap of property characteristics
    
    :param properties: DataFrame of property details
    :param scores: List of (property_name, score) tuples
    """
    plt.figure(figsize=(12, 8))
    score_dict = dict(scores)
    
    # Select relevant columns for heatmap
    heatmap_data = properties[['price', 'amenities', 'sustainability', 'walkability']].copy()
    heatmap_data.index = properties['name']
    
    # Normalize data for better visualization
    heatmap_data_normalized = (heatmap_data - heatmap_data.min()) / (heatmap_data.max() - heatmap_data.min())
    
    sns.heatmap(
        heatmap_data_normalized, 
        annot=heatmap_data.values, 
        cmap='YlGnBu', 
        fmt='.0f',
        cbar_kws={'label': 'Normalized Score'}
    )
    
    plt.title("Property Characteristics Heatmap", fontsize=15)
    plt.tight_layout()
    plt.savefig('property_heatmap.png')
    plt.close()