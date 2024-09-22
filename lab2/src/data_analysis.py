import os
import pandas as pd

def load_ck_metrics(repo_name):
    # Corrigir o caminho para incluir diretamente o repo_name seguido de "class.csv"
    file_path = os.path.join('data', 'ck_results', f"{repo_name}class.csv")
    print(f"Verificando se o arquivo {file_path} existe...")

    if os.path.exists(file_path):
        print(f"Arquivo {file_path} encontrado. Carregando métricas CK...")
        df = pd.read_csv(file_path)
        print(f"Métricas CK carregadas para {repo_name}.")
        return df
    else:
        print(f"Nenhum arquivo de métricas CK encontrado para {repo_name}.")
        return pd.DataFrame()

def compute_quality_metrics(df):
    # Verificar se as colunas esperadas estão no DataFrame
    if 'cbo' not in df.columns or 'dit' not in df.columns or 'lcom' not in df.columns:
        print("As colunas cbo, dit, ou lcom não estão presentes no arquivo CSV.")
        return {}

    # Calcula apenas a soma para CBO, DIT e LCOM
    metrics = {}
    for metric in ['cbo', 'dit', 'lcom']:
        metrics[f'{metric}_sum'] = df[metric].sum()

    print("Métricas calculadas: ", metrics)
    return metrics
