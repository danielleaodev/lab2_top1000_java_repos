import pandas as pd
import numpy as np
import os

def load_ck_metrics(repo_name):
    file_path = os.path.join('data', 'ck_results', repo_name, 'class.csv')
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return df
    else:
        print(f"No CK metrics found for {repo_name}")
        return pd.DataFrame()

def compute_quality_metrics(df):
    # Compute median, mean, and standard deviation for CBO, DIT, LCOM
    metrics = {}
    for metric in ['cbo', 'dit', 'lcom']:
        metrics[f'{metric}_median'] = df[metric].median()
        metrics[f'{metric}_mean'] = df[metric].mean()
        metrics[f'{metric}_std'] = df[metric].std()
    return metrics
