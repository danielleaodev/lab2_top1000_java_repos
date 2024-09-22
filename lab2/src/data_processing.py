import os
import subprocess
from git import Repo
import shutil
import stat
import time
from git import GitCommandError

def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def clone_repo(repo_url, clone_dir, max_retries=3):
    attempt = 0
    while attempt < max_retries:
        try:
            print(f"Tentando clonar o repositório {repo_url} (tentativa {attempt+1}/{max_retries})")
            Repo.clone_from(repo_url, clone_dir)
            print(f"Clonado com sucesso: {repo_url}")
            return True
        except GitCommandError as e:
            print(f"Erro ao clonar {repo_url}: {e}")
            attempt += 1
            if attempt < max_retries:
                print(f"Tentando novamente após uma pausa...")
                time.sleep(5)  # Pausa de 5 segundos antes de tentar novamente
            else:
                print(f"Falha ao clonar o repositório {repo_url} após {max_retries} tentativas.")
                return False

def run_ck(java_project_path, output_dir):
    ck_jar_name = 'ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar'
    ck_jar_path = os.path.abspath(os.path.join('ck', 'target', ck_jar_name))

    if not os.path.exists(ck_jar_path):
        print(f"Erro: O arquivo JAR do CK não foi encontrado em {ck_jar_path}")
        return

    # Certifica que o diretório de saída existe
    os.makedirs(output_dir, exist_ok=True)

    cmd = [
        'java', '-jar', ck_jar_path, java_project_path,
        'false',  # Use JDK 8
        '0',      # Max nested levels
        'false',  # Show methods
        output_dir
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Métricas CK calculadas para {java_project_path}")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o CK para {java_project_path}: {e.stderr}")

def process_repo(repo_info):
    repo_url = repo_info['clone_url']
    repo_name = repo_info['name']
    clone_dir = os.path.join('data', 'repos', repo_name)
    output_dir = os.path.join('data', 'ck_results', repo_name)

    clone_repo(repo_url, clone_dir)
    run_ck(clone_dir, output_dir)

    # Aguarda um momento antes de excluir
    time.sleep(30)

    # Excluir o repositório
    try:
        shutil.rmtree(clone_dir, onexc=remove_readonly)
        print(f"Repositório {repo_name} excluído após a análise.")
    except Exception as e:
        print(f"Erro ao excluir o repositório {repo_name}: {e}")