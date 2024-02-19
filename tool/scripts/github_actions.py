"""
GitHub Actions Checker

This Python program checks if GitHub Actions is implemented in a given GitHub repository.
It sends a request to the GitHub API to fetch the contents of the .github/workflows directory,
and then checks if any YAML files exist in that directory. If YAML files are found, it considers
GitHub Actions to be implemented in the repository; otherwise, it considers GitHub Actions
not to be implemented.

Usage:
- Run the program and provide the GitHub repository URL when prompted.
- The program will then check if GitHub Actions is implemented in the specified repository
  and print the result.

Example:
python github_actions_checker.py
Enter the GitHub repository URL: https://github.com/username/repository
GitHub Actions is implemented in the repository.
"""

import os
import requests
from dotenv import load_dotenv
import yaml

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
    # Extract the owner and repository name from the provided URL
    owner, repo = repository_url.rstrip('/').split('/')[-2:]

    # Construct the API URL for fetching the contents of .github/workflows directory
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/.github/workflows"

    # Get the GitHub token from environment variables
    token = os.getenv('GITHUB_ACCESS_TOKEN')
    headers = {'Authorization': f'token {token}'}

    # Send a GET request to the API URL
    response = requests.get(api_url, headers=headers)

    # Check if the response is successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

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
        yaml_files = []
        for file in data:
            if file['type'] == 'file' and (file['name'].endswith('.yml') or file['name'].endswith('.yaml')):
                yaml_files.append(file['name'])
                print(f"YAML file found: {file['name']}")

                 # Fetch the contents of the workflow file
                file_response = requests.get(file['download_url'])
                file_contents = file_response.text

                # Check if the workflow file contains any of the linter commands
                for command, name in linter_commands.items():
                    if command in file_contents:
                        print(f"Linter found: {name}")
                        print("Checking for additional rules...")

                        # Parse the YAML file
                        workflow = yaml.safe_load(file_contents)

                        # Check for additional rules
                        for step in workflow.get('jobs', {}).values():
                            for run in step.get('steps', []):
                                if 'run' in run and command in run['run']:
                                    print(f"Additional rules for {name}:")
                                    print(run['run'])

                # Check if the workflow file contains any of the testing libraries
                for library, name in testing_libraries.items():
                    if library in file_contents:
                        print(f"Testing library found: {name}")
                        print("Checking additional rules.. ")

                        # Parse the YAML file
                        workflow = yaml.safe_load(file_contents)

                        # Check for additional rules for testing libraries
                        for step in workflow.get('jobs', {}).values():
                            for run in step.get('steps', []):
                                if 'run' in run and library in run['run']:
                                    print(f"Additional rules for {name}:")
                                    print(run['run'])

        if yaml_files:
            print("YAML files in /.github/workflows:")
            for yaml_file in yaml_files:
                print(yaml_file)
            return True

    # GitHub Actions not implemented if the code reaches here
    return False

if __name__ == "__main__":
    repository_url = input("Enter the GitHub repository URL: ")
    if check_github_actions(repository_url):
        print("GitHub Actions is implemented in the repository.")
    else:
        print("GitHub Actions is not implemented in the repository.")