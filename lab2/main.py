import os
import shutil  # Para excluir diretórios
import pandas as pd
from multiprocessing import Pool
from datetime import datetime
from src.data_collection import fetch_top_java_repos, save_repos_info_to_csv
from src.data_processing import clone_repo, process_repo
from src.data_analysis import load_ck_metrics, compute_quality_metrics
import stat

# Função para calcular a idade do repositório
def compute_repo_age(repo):
    created_at = datetime.strptime(repo['created_at'], '%Y-%m-%dT%H:%M:%SZ')
    age_years = (datetime.now() - created_at).days / 365
    return age_years

# Função para contar releases
def get_release_count(repo):
    return repo.get('releases', {}).get('total_count', 0)

# Função para contar linhas de código (LOC)
def compute_loc(df):
    return df['loc'].sum()

# Função para inicializar os arquivos CSV
def init_csv_files():
    if not os.path.exists('data'):
        os.makedirs('data')

    # Inicializando o CSV com informações básicas dos repositórios e métricas CK
    quality_csv_path = 'data/quality_metrics.csv'
    if not os.path.exists(quality_csv_path):
        pd.DataFrame(columns=[
            'repo_name', 'stars', 'forks', 'age_years', 'releases', 'loc', 
            'cbo_sum', 'dit_sum', 'lcom_sum']).to_csv(quality_csv_path, index=False)

# Função para verificar se os arquivos de métricas CK já existem
def ck_results_exist(repo_name):
    file_path = os.path.join('data', 'ck_results', f"{repo_name}_class.csv")
    return os.path.exists(file_path)

# Função para excluir repositórios após o processamento
def delete_repo(clone_dir):
    def on_rm_error(func, path, exc_info):
        os.chmod(path, stat.S_IWRITE)
        os.unlink(path)

    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir, onerror=on_rm_error)
        print(f"Repositório {clone_dir} excluído após a análise.")
    else:
        print(f"Repositório {clone_dir} não encontrado para exclusão.")

# Função para processar um único repositório e salvar as métricas CK junto com os dados básicos
def process_and_save_metrics(repo):
    repo_name = repo['name']
    repo_url = repo['html_url']  # URL do repositório

    # Verificar se já existem resultados CK para este repositório
    if ck_results_exist(repo_name):
        print(f"Resultados CK já existentes para {repo_name}. Pulando processamento.")
        return  # Se já houver resultados, pular o processamento

    # Clonar o repositório e calcular as métricas CK
    clone_dir = os.path.join('data', 'repos', repo_name)
    if not clone_repo(repo_url, clone_dir):
        print(f"Repositório {repo_name} ignorado devido a falhas na clonagem.")
        return  # Ignorar este repositório e continuar com os próximos

    # Continuar com o processamento e cálculos das métricas CK
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
        })

        # Adiciona métricas de qualidade ao arquivo CSV em modo append
        pd.DataFrame([metrics]).to_csv('data/quality_metrics.csv', mode='a', header=False, index=False)
        print(f"Métricas para {repo_name} salvas.")
    else:
        print(f"Nenhuma métrica CK encontrada para {repo_name}, mas informações básicas foram salvas.")

    # Excluir o repositório após o processamento
    delete_repo(clone_dir)


# Função para salvar todas as métricas consolidadas
def save_all_metrics(all_metrics):
    pd.DataFrame(all_metrics).to_csv('data/quality_metrics.csv', mode='w', header=True, index=False)
    print("Todas as métricas foram salvas no CSV.")

def main():
    # Inicializar os arquivos CSV se ainda não existirem
    init_csv_files()

    print("Fetching top Java repositories...")
    repos = fetch_top_java_repos(n=1000)
    save_repos_info_to_csv(repos)

    # Carregar informações dos repositórios do CSV existente
    repos_info = pd.read_csv('data/repos_info.csv')
    repos = repos_info.to_dict('records')

    print("Compilando métricas CK existentes...")
    with Pool(processes=4) as pool:
        pool.map(process_and_save_metrics, repos)

if __name__ == '__main__':
    main()
