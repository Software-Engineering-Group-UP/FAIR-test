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

        # Check if any YAML files exist in .github/workflows directory
        yaml_files = []
        for file in data:
            if file['type'] == 'file' and (file['name'].endswith('.yml') or file['name'].endswith('.yaml')):
                yaml_files.append(file['name'])
                print(f"YAML file found: {file['name']}")

        if yaml_files:
            print("YAML files in /.github/workflows:")
            for yaml_file in yaml_files:
                print(yaml_file)
            return True

    # GitHub Actions not implemented if the code reaches here
    return False

#function that checks if the .yaml or .yml file runs the linter jobs


if __name__ == "__main__":
    repository_url = input("Enter the GitHub repository URL: ")
    if check_github_actions(repository_url):
        print("GitHub Actions is implemented in the repository.")
    else:
        print("GitHub Actions is not implemented in the repository.")