'''
Author: Akira Yoshiyama, 2024-12-29

WHAT DOES THIS DO?

This script uses the OpenAI API to find the range of versions of a package that likely works for a repository. It uses the parsed
libraries and library functions/classes/etc. used in the repository.

'''

from openai import OpenAI 
from dotenv import load_dotenv
import os

def ask_gpt(package_name, uses, min_python_version, last_commit_date):
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a senior software engineer. Only respond with the version numbers in the format >=a.b.c,<x.y.z."},
                {"role": "user", 
                 "content": f"You are a senior software engineer. You have a large code repository written in Python. You are using {package_name}\
                    in your python files. The following attributes are used: {uses}. By referencing the documentation of {package_name}, find the\
                    minimum and maximum versions of {package_name} where none of the attributes listed above are missing or deprecated. Keep in mind\
                    the last commit for the repository was made on {last_commit_date}. You cannot refactor the code in your repository."
                }
            ],
            max_tokens=20,
            temperature=0.3,
            frequency_penalty=0.0,
            stream=False,
        )
        
    output_text = response.choices[0].message.content
    return output_text

def ask_gpt_python_version(dependency_versions, min_python_version, last_commit_date):
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
                {"role": "system", "content": "You are a senior software engineer. Only respond with one version in the format a.b.c"},
                {"role": "user", 
                 "content": f"You are a senior software engineer. You have a large code repository written in Python. You are using the\
                    packages: {dependency_versions}. Keep in mind the last commit for the repository was made on {last_commit_date}.\
                    The absolute minimum possible python version for this repository is {min_python_version}. What is the most likely Python version\
                    to be compatible with all packages and their correct versions for this repository?"
                }
            ],
        max_tokens=20,
        temperature=0.3,
        frequency_penalty=0.0,
        stream=False,
    )
    output_text = response.choices[0].message.content
    return output_text

def check_all_packages(usage_dict, min_python_version, last_commit_date):
    results = {}
    for package, uses in usage_dict.items():
        results[package] = ask_gpt(package, uses, min_python_version, last_commit_date)
    return results