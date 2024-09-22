import os
import requests
import time
import pandas as pd  # Import necessário para salvar em CSV
from .utils import GITHUB_TOKEN

def check_rate_limit(headers):
    remaining = int(headers.get('X-RateLimit-Remaining', 0))
    reset_time = int(headers.get('X-RateLimit-Reset', 0))
    if remaining == 0:
        sleep_time = max(reset_time - time.time(), 0)
        print(f"Rate limit reached. Sleeping for {sleep_time} seconds.")
        time.sleep(sleep_time + 1)  # Espera até a taxa ser resetada
        return True
    return False

def fetch_releases_count(repo_url, headers):
    releases_count = 0
    per_page = 30
    page = 1

    while True:
        releases_url = f"{repo_url}/releases"
        params = {'per_page': per_page, 'page': page}
        releases_response = requests.get(releases_url, headers=headers, params=params)

        if check_rate_limit(releases_response.headers):
            continue

        if releases_response.status_code == 200:
            releases = releases_response.json()
            releases_count += len(releases)

            # Se o número de releases retornadas for menor que 'per_page', significa que não há mais releases a serem buscadas
            if len(releases) < per_page:
                break
        else:
            print(f"Erro ao buscar releases para o repositório {repo_url}: {releases_response.status_code}")
            break

        page += 1
        time.sleep(1)  # Pausar para evitar limite de taxa

    return releases_count

def fetch_top_java_repos(n=1000):
    repos = []
    per_page = 50
    pages = n // per_page + 1
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}

    for page in range(1, pages + 1):
        print(f"Buscando página {page}...")
        url = 'https://api.github.com/search/repositories'
        params = {
            'q': 'language:Java',
            'sort': 'stars',
            'order': 'desc',
            'per_page': per_page,
            'page': page
        }
        response = requests.get(url, headers=headers, params=params)

        if check_rate_limit(response.headers):
            continue

        if response.status_code == 200:
            data = response.json()
            for repo in data['items']:
                # Buscar o número total de releases com paginação
                repo['releases_count'] = fetch_releases_count(repo['url'], headers)
                repos.append(repo)
        else:
            print(f"Erro ao buscar página {page}: {response.status_code}")
            break

        time.sleep(1)

    return repos[:n]

def save_repos_info_to_csv(repos):
    # Verificar se o diretório "data" existe, senão criar
    if not os.path.exists('data'):
        print("Criando diretório 'data'.")
        os.makedirs('data')

    # Definir as colunas que você deseja salvar
    columns = ['name', 'stargazers_count', 'forks_count', 'releases_count', 'created_at', 'html_url']

    # Converter a lista de repositórios em um DataFrame
    if repos:
        repos_df = pd.DataFrame(repos)
        print(f"Salvando {len(repos)} repositórios em CSV.")
    else:
        print("Nenhum repositório foi coletado.")
        return

    # Verificar se todas as colunas existem no DataFrame
    missing_columns = [col for col in columns if col not in repos_df.columns]
    if missing_columns:
        print(f"As colunas a seguir estão faltando no DataFrame: {missing_columns}")
        # Adicionar colunas faltantes com valores nulos
        for col in missing_columns:
            repos_df[col] = None

    # Salvar o DataFrame em um CSV
    try:
        repos_df.to_csv('data/repos_info.csv', columns=columns, index=False)
        print("Arquivo repos_info.csv salvo com sucesso.")
    except Exception as e:
        print(f"Erro ao salvar o arquivo repos_info.csv: {e}")

