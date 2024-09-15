import requests
from .utils import GITHUB_TOKEN

def fetch_top_java_repos(n=1000):
    repos = []
    per_page = 100
    pages = n // per_page
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}

    for page in range(1, pages + 1):
        url = 'https://api.github.com/search/repositories'
        params = {
            'q': 'language:Java',
            'sort': 'stars',
            'order': 'desc',
            'per_page': per_page,
            'page': page
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            repos.extend(data['items'])
        else:
            print(f"Error fetching page {page}: {response.status_code}")
            break
    return repos[:n]
