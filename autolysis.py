# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "seaborn",
#   "pandas",
#   "matplotlib",
#   "httpx",
#   "chardet",
#   "numpy",
#   "scikit-learn"
# ]
# ///

import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import httpx
import chardet
import importlib
import subprocess
from sklearn.cluster import KMeans
import numpy as np


# Constants
API_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")

if not AIPROXY_TOKEN:
    print("Error: The AIPROXY_TOKEN environment variable is not set.")
    sys.exit(1)

# Function to load data with encoding detection
def load_data(file_path):
    """Load CSV data with encoding detection."""
    try:
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
        encoding = result['encoding']
        return pd.read_csv(file_path, encoding=encoding)
    except Exception as e:
        print(f"Failed to load the dataset: {e}")
        sys.exit(1)

# Function to analyze data
def analyze_data(df):
    """Perform basic data analysis."""
    numeric_df = df.select_dtypes(include=['number'])
    analysis = {
        'summary': df.describe(include='all').to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'correlation': numeric_df.corr().to_dict(),
        'outliers': {
            col: ((numeric_df[col] - numeric_df[col].mean()).abs() > 3 * numeric_df[col].std()).sum()
            for col in numeric_df.columns
        }
    }
    return analysis

# Function to perform advanced analysis
def advanced_analysis(df):
    """Perform advanced analyses like clustering."""
    numeric_df = df.select_dtypes(include=['number']).dropna()  # Drop rows with missing values in numeric columns
    if numeric_df.shape[1] >= 2:  # Ensure there are at least two numeric columns
        kmeans = KMeans(n_clusters=3, random_state=42).fit(numeric_df)
        # Create a cluster column with NaN values initially
        cluster_labels = pd.Series(np.nan, index=df.index)
        # Assign cluster labels only to rows used in clustering
        cluster_labels.loc[numeric_df.index] = kmeans.labels_
        df['Cluster'] = cluster_labels
        return {
            'cluster_centers': kmeans.cluster_centers_.tolist(),
            'labels': cluster_labels.tolist()
        }
    return {}


# Function to visualize data
def visualize_data(df, output_dir):
    """Generate and save visualizations."""
    sns.set(style="whitegrid")
    os.makedirs(output_dir, exist_ok=True)
    numeric_columns = df.select_dtypes(include=['number']).columns
    image_paths = []

    # Histograms
    for column in numeric_columns:
        plt.figure()
        sns.histplot(df[column].dropna(), kde=True)
        plt.title(f'Distribution of {column}')
        img_path = os.path.join(output_dir, f'{column}_distribution.png')
        plt.savefig(img_path)
        plt.close()
        image_paths.append(img_path)

    # Correlation Heatmap
    if len(numeric_columns) > 1:
        plt.figure(figsize=(10, 8))
        sns.heatmap(df[numeric_columns].corr(), annot=True, cmap="coolwarm")
        plt.title("Correlation Heatmap")
        heatmap_path = os.path.join(output_dir, 'correlation_heatmap.png')
        plt.savefig(heatmap_path)
        plt.close()
        image_paths.append(heatmap_path)

    return image_paths

def generate_narrative(analysis, advanced, image_paths):
    """Generate narrative using LLM."""
    headers = {
        'Authorization': f'Bearer {AIPROXY_TOKEN}',
        'Content-Type': 'application/json'
    }
    prompt = f"""
    Analyze the following data:
    - Summary Statistics: {analysis['summary']}
    - Missing Values: {analysis['missing_values']}
    - Correlation: {list(analysis['correlation'].keys())[:5]}  # Limit the size
    - Outliers: {analysis['outliers']}
    Advanced Analysis: {advanced}
    Include insights from these visualizations: {image_paths}.
    Provide a concise and meaningful narrative.
    """
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = httpx.post(API_URL, headers=headers, json=data, timeout=60.0)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except httpx.TimeoutException:
        print("Error: Request timed out. Consider simplifying the prompt or analysis.")
        return "Narrative generation failed due to a timeout."
    except Exception as e:
        print(f"An error occurred while generating the narrative: {e}")
        return "Narrative generation failed."


# Main script logic
def main(file_path):
    dataset_name = os.path.splitext(os.path.basename(file_path))[0]
    output_dir = dataset_name
    df = load_data(file_path)
    analysis = analyze_data(df)
    advanced = advanced_analysis(df)
    image_paths = visualize_data(df, output_dir)
    narrative = generate_narrative(analysis, advanced, image_paths)
    readme_path = os.path.join(output_dir, 'README.md')

    # Save narrative and embed images
    with open(readme_path, 'w') as f:
        f.write(narrative)
        f.write("\n\n## Visualizations\n")
        for img in image_paths:
            f.write(f"![{os.path.basename(img)}]({os.path.basename(img)})\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python autolysis.py <dataset.csv>")
        sys.exit(1)
    main(sys.argv[1])



