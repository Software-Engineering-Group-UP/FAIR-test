"""
This Python program checks if GitHub Actions is implemented in a given GitHub repository.
It uses the ghapi library to interact with the GitHub API, fetching the contents of the .github/workflows directory,
and then checks if any YAML files exist in that directory. If YAML files are found, it considers
GitHub Actions to be implemented in the repository; otherwise, it considers GitHub Actions
not to be implemented.

Example usage:
python test.py https://api.github.com/repos/pik-piam/magpie4
"""

import os
import argparse
from dotenv import load_dotenv
import yaml
from ghapi.all import GhApi
from urllib.parse import urlparse
import base64

# Load environment variables from .env file
load_dotenv()

def check_github_actions(repository_url):
    """
    Check if GitHub Actions is implemented in the given GitHub repository.
    Check if the repository has a contents/.github/workflows directory with YAML files. 

    Args:
    - repository_url: The URL of the GitHub repository to check.

    Returns:
    - True if GitHub Actions is implemented, False otherwise.
    """
   # Parse owner and repo from URL
    split_url = repository_url.split('/')
    owner = split_url[-2]
    repo = split_url[-1]

    # Get the GitHub token from environment variables
    token = os.getenv('GITHUB_ACCESS_TOKEN')

    # Create a GhApi object
    api = GhApi(owner, repo, token)

    # Fetch the contents of .github/workflows directory
    try:
        data = api.repos.get_content('.github/workflows')
    except:
        return False

    # List of common Python and R linter commands and their corresponding names
    linter_commands = {
        'pylint': 'Pylint',
        'flake8': 'Flake8',
        'bandit': 'Bandit',
        'lintr::lint': 'lintr'
    }

    # List of common Python and R testing libraries and their corresponding names
    testing_libraries = {
        'pytest': 'pytest',
        'unittest': 'unittest',
        'nose': 'nose',
        'testthat': 'testthat'
    }        

    # Check if any YAML files exist in .github/workflows directory
    yaml_files = [file for file in data if file.type == 'file' and (file.name.endswith('.yml') or file.name.endswith('.yaml'))]

    for file in yaml_files:
        print(f"YAML file found: {file.name}")

        # Fetch the contents of the workflow file
        file_contents = base64.b64decode(api.repos.get_content(f'.github/workflows/{file.name}').content).decode()

        # Check if the workflow file contains any of the linter commands
        for command, name in linter_commands.items():
            # Parse the YAML file
            workflow = yaml.safe_load(file_contents)

            # Check for the command in the 'run' strings of the workflow
            for step in workflow.get('jobs', {}).values():
                for run in step.get('steps', []):
                    if 'run' in run and command in run['run']:
                        print(f"Linter found: {name}")
                        print("Checking for additional rules...")
                        print(f"Additional rules for {name}:")
                        print(run['run'])

        # Check if the workflow file contains any of the testing libraries
        for library, name in testing_libraries.items():
            # Parse the YAML file
            workflow = yaml.safe_load(file_contents)

            # Check for the library in the 'run' strings of the workflow
            for step in workflow.get('jobs', {}).values():
                for run in step.get('steps', []):
                    if 'run' in run and library in run['run']:
                        print(f"Testing library found: {name}")
                        print("Checking additional rules.. ")
                        print(f"Additional rules for {name}:")
                        print(run['run'])

    return bool(yaml_files)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check if GitHub Actions is implemented in a GitHub repository.')
    parser.add_argument('repository_url', help='The URL of the GitHub repository to check.')
    args = parser.parse_args()

    if check_github_actions(args.repository_url):
        print("GitHub Actions is implemented in the repository.")
    else:
        print("GitHub Actions is not implemented in the repository.")