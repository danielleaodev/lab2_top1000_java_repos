import os

def load_dotenv():
    with open('.env') as f:
        for line in f:
            if line.startswith('GITHUB_TOKEN'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

load_dotenv()
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
