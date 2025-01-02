'''
Author: Akira Yoshiyama, 2024-12-29

WHAT DOES THIS DO? (THIS IS THE MAIN SCRIPT)

It will create a new requirements.txt file for a github repo with likely acceptable version ranges for each package used in the repo 
and the most likely python version for the repo. There is no need for there to be an exisiting requirements.txt file. This script 
will find the packages used in the repo.

ASSUMPTIONS:
- Assume linux system (not super important)
- Forget about CUDA versions (sorry pytorch users)
- Forget about dependency conflicts for now

STEPS:
1. Find the minimum version of Python that works (using Vermin)
    -> Note that vermin requires the latest version of Python to run
2. Parse the github repo to find all libraries used and the library functions/classes/etc. used for each library
    -> Note that I tokenize the code first so that we can parse the code into an AST
3. Find the range of versions of each library that likely works for the repo (i.e. the versions where none of the functions/classes/etc. used are nonexistent or deprecated)
    -> Uses LLM to do this, using context of the parsed libraries and library functions/classes/etc. used, and the last commit date
4. Find the most likely python version for the repo
    -> Uses LLM to do this, using context of the parsed libraries and library functions/classes/etc. used, the last commit date and the absolute minimum python version
5. Write the python version and package versions to a new_requirements.txt file

FUTURE IMPROVEMENTS:
1. We could use an LLM to parse the readme to look for package version ranges
2. We could feed the LLM the documentation of each package as context as well when finding the version ranges
3. We don't know how functions/classes change over time between versions. This also matters but is not checked.

CONSIDERATIONS:
1. I considered parsing the source code of each package to find the acceptable version ranges, but this would require downloading
    every single version of every single package. I decided against this.

'''

import subprocess, re, os, sys
from package_analysis import analyze_python_files
from find_package_versions import check_all_packages, ask_gpt_python_version

###########################
# VERMIN FUNCTIONS
###########################

# Run a command and return output
def run_command(command):
    return subprocess.run(command, shell=True, check=True, capture_output=True, text=True)

# Get Python version using vermin
def get_python_version(repo_path):
    pattern = r"Minimum required versions:\s*(\d+\.\d+)"
    try:
        output = run_command(f"vermin {repo_path}").stdout
    except Exception as e:
        print(f"Vermin Error: {e}")
        return None
    match = re.search(pattern, output)
    if match:
        return match.group(1)
    else:
        return None

###########################
# PARSING REQUIREMENTS.TXT FUNCTIONS
###########################

def find_requirements_file(repo_path):
    # Search for requirements.txt in repo_path
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file == "requirements.txt":
                return os.path.join(root, file)
    return None

def read_requirements_file(requirements_file_path):
    with open(requirements_file_path, 'r') as file:
        # Exclude lines that start with '#'
        return [line for line in file.read().splitlines() if not line.startswith('#')]

###########################
# MAIN FUNCTION
###########################

def fix_dependencies(repo_path, last_commit_date):
    # Get min python version for package
    min_python_version = get_python_version(repo_path)
    if min_python_version is None:
        print("Error getting Python version")
        return

    # Get all imported packages and their functions/classes/etc. used in the repo
    usage_dict = {pkg: uses for pkg, uses in analyze_python_files(repo_path).items() 
                  if pkg not in sys.stdlib_module_names}
    print(usage_dict)

    # For each package in usage_dict, find the min and max versions that work
    package_versions = check_all_packages(usage_dict, min_python_version, last_commit_date)
    python_version = ask_gpt_python_version(package_versions, min_python_version, last_commit_date)

    # Write to a requirements.txt file
    with open(os.path.join(repo_path, "new_requirements.txt"), "w") as file:
        file.write(f"python=={python_version}\n")
        for package, version in package_versions.items():
            file.write(f"{package}{version}\n")

if __name__ == "__main__":
    print("What is the path to the package (absolute path)?")
    repo_path = input()
    print("What is the date of the last commit (YYYY-MM-DD)?")
    last_commit_date = input()

    # Process and fix dependencies in requirements.txt
    out = fix_dependencies(repo_path, last_commit_date)
