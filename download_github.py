#%%
import pickle as pkl
import os
import requests

def load_data(path):
    with open(path, 'rb') as f:
        return pkl.load(f)

DATA = load_data('./Jupyter_Notebook.pkl')
GITHUB_API_TOKEN = os.environ["GAPI_NO_PRIV"]

#%%
# Includes all the files in the repository recursively
def get_all_files(repo_full_name: str, default_branch: str) -> list[str]:
    url = f"https://api.github.com/repos/{repo_full_name}/git/trees/{default_branch}?recursive=1"
    response = requests.get(url, headers={"Authorization": "token " + GITHUB_API_TOKEN})
    return response.json()

# %%
def get_ipynb_files(file_tree):
    ipynb_files = []
    for f in file_tree:
        if f['type'] == 'blob' and f['path'].endswith('.ipynb'):
            ipynb_files.append(f['path'])
    return ipynb_files
# %%
def download_file_content(repo_full_name: str, default_branch: str) -> str:
    url = f"https://api.github.com/repos/{repo_full_name}/git/trees/{default_branch}?recursive=1"
    raw_url = f"https://raw.githubusercontent.com/{repo_full_name}/{default_branch}/"
    response = requests.get(url, headers={"Authorization": "token " + GITHUB_API_TOKEN}).json()
    ipynb_files = get_ipynb_files(response['tree'])
    files = {}
    for f in ipynb_files:
        file_url = raw_url + f
        response = requests.get(file_url, headers={"Authorization": "token " + GITHUB_API_TOKEN})
        files[f] = response.text
    return files
    

# %%
if __name__ == "__main__":
    files = download_file_content(DATA[0]['full_name'], DATA[0]['default_branch'])
# %%
