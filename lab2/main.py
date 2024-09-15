# main.py
from src.data_collection import fetch_top_java_repos
from src.data_processing import process_repo
from src.data_analysis import load_ck_metrics, compute_quality_metrics
import pandas as pd
from multiprocessing import Pool
from datetime import datetime

def main():
    # Step 1: Data Collection
    print("Fetching top Java repositories...")
    repos = fetch_top_java_repos(n=1000)

    # Convert to DataFrame for easy handling
    repos_df = pd.DataFrame(repos)
    repos_df.to_csv('data/repos_info.csv', index=False)

    # Step 2: Data Processing
    print("Cloning repositories and computing CK metrics...")
    with Pool(processes=4) as pool:
        pool.map(process_repo, repos)

    # Step 3: Data Analysis
    print("Analyzing CK metrics...")
    quality_metrics = []
    for repo in repos:
        repo_name = repo['name']
        ck_df = load_ck_metrics(repo_name)
        if not ck_df.empty:
            metrics = compute_quality_metrics(ck_df)
            metrics.update({
                'repo_name': repo_name,
                'stars': repo['stargazers_count'],
                'forks': repo['forks_count'],
                'age_years': compute_repo_age(repo),
                'releases': get_release_count(repo),
                'loc': compute_loc(ck_df),
                # Add other metrics as needed
            })
            quality_metrics.append(metrics)

    # Convert to DataFrame
    quality_df = pd.DataFrame(quality_metrics)
    quality_df.to_csv('data/quality_metrics.csv', index=False)

    # Step 4: Answer Research Questions
    # Perform statistical analysis and plotting
    answer_research_questions(quality_df)

if __name__ == '__main__':
    main()


def compute_repo_age(repo):
    created_at = datetime.strptime(repo['created_at'], '%Y-%m-%dT%H:%M:%SZ')
    age = (datetime.now() - created_at).days / 365
    return age

def get_release_count(repo):
    return repo['open_issues_count']  # Or fetch releases using GitHub API if necessary

def compute_loc(ck_df):
    return ck_df['loc'].sum()

def answer_research_questions(df):
    # RQ01: Popularity vs Quality
    import matplotlib.pyplot as plt
    plt.scatter(df['stars'], df['cbo_mean'])
    plt.xlabel('Stars')
    plt.ylabel('Mean CBO')
    plt.title('Popularity vs Coupling (CBO)')
    plt.savefig('data/plots/popularity_vs_cbo.png')
    # Similarly for other metrics and research questions