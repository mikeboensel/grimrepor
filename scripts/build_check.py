import os
import sys
import subprocess
import requests
import pandas as pd
from multiprocessing import Pool
import tempfile
from tqdm import tqdm
import yaml
import glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def fetch_file(repo_url, file_name, branches=["main", "master"]):
    for branch in branches:
        try:
            raw_url = f"{repo_url.replace('github.com', 'raw.githubusercontent.com')}/{branch}/{file_name}"
            response = requests.get(raw_url)
            response.raise_for_status()
            return response.text
        except requests.RequestException:
            pass
    return None

def parse_setup_py(setup_content):
    # Extract install_requires from setup.py
    # This is a simple implementation and might need to be more robust
    install_requires = []
    for line in setup_content.split('\n'):
        if 'install_requires' in line:
            requirements = line.split('=')[-1].strip()[1:-1].replace("'", "").replace('"', '')
            install_requires = [req.strip() for req in requirements.split(',')]
            break
    return '\n'.join(install_requires)

def parse_conda_env(conda_content):
    # Parse conda environment file and convert to pip requirements
    try:
        env_dict = yaml.safe_load(conda_content)
        dependencies = env_dict.get('dependencies', [])
        pip_requirements = [dep for dep in dependencies if isinstance(dep, str)]
        pip_dict = next((item for item in dependencies if isinstance(item, dict) and 'pip' in item), None)
        if pip_dict:
            pip_requirements.extend(pip_dict['pip'])
        return '\n'.join(pip_requirements)
    except yaml.YAMLError:
        return None

def install_requirements(requirements_content):
    try:
        with tempfile.TemporaryDirectory() as env_dir:
            subprocess.run(["python3", "-m", "venv", env_dir], check=True)
            pip_executable = os.path.join(env_dir, "bin", "pip") if os.name != 'nt' else os.path.join(env_dir, "Scripts", "pip")

            with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_req_file:
                temp_req_file.write(requirements_content)
                temp_req_file.flush()

                result = subprocess.run([pip_executable, "install", "-r", temp_req_file.name], capture_output=True, text=True)

                if result.returncode != 0:
                    return False, result.stderr
                return True, None
    except Exception as e:
        return False, str(e)

def check_repo(repo):
    requirements = fetch_file(repo, "requirements.txt")
    if not requirements:
        setup_py = fetch_file(repo, "setup.py")
        if setup_py:
            requirements = parse_setup_py(setup_py)
        else:
            conda_env = fetch_file(repo, "environment.yml") or fetch_file(repo, "environment.yaml")
            if conda_env:
                requirements = parse_conda_env(conda_env)

    if not requirements:
        return repo, "No requirements found"

    success, error = install_requirements(requirements)
    if success:
        return repo, "Success"
    else:
        # Parse error message
        if "No matching distribution found" in error:
            return repo, "No matching distribution found"
        else:
            return repo, f"Failed: {error}"

def check_repos(repos):
    with Pool(processes=10) as pool:
        results = list(tqdm(pool.imap(check_repo, repos), total=len(repos), desc="Processing Repositories"))
    return dict(results)

def check_local_requirements(requirements_files):
    results = {}
    for req_file in tqdm(requirements_files, desc="Processing Local Requirements"):
        try:
            with open(req_file, 'r') as f:
                requirements_content = f.read()

            success, error = install_requirements(requirements_content)
            if success:
                results[req_file] = "Success"
            else:
                if "No matching distribution found" in error:
                    results[req_file] = "No matching distribution found"
                else:
                    results[req_file] = f"Failed: {error}"
        except Exception as e:
            results[req_file] = f"Error reading file: {str(e)}"

    return results

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--local":
        # Check local requirements files
        # FIXME: Replace with the actual path to the requirements files
        # git ls-files | grep requirements.txt
        # status of 0 means success (found 1+ requirements files)
        # os.path.walk ...
        requirements_files = glob.glob("path/to/requirements/*.txt")
        results = check_local_requirements(requirements_files)
    else:
        # Check GitHub repositories
        filepath = os.path.join(ROOT, "data", "paper_repo_info.csv")
        df = pd.read_csv(filepath)
        repos = df["repo_url"].tolist()
        results = check_repos(repos)

    # Create a DataFrame with the results
    results_df = pd.DataFrame(list(results.items()), columns=["file_or_repo", "status"])

    # Write results to a CSV file
    output_file = os.path.join(ROOT, "output", "build_check_results.csv")
    results_df.to_csv(output_file, index=False)
