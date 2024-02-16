"""
GitHub Actions Linter Checker

This script checks if GitHub Actions is implemented in a given GitHub repository.
It fetches the repository contents using GitHub's REST API, looks for YAML files in the .github/workflows directory,
and identifies linters specified for Python and R in those YAML files, printing their names.
It also prints the programming languages used in the repository.

Usage:
python script.py <repository_url>

Example:
python script.py https://github.com/username/repository
"""

import os
import yaml
import argparse
import requests
from urllib.parse import urlparse


def check_github_actions(repository_url):
    """
    Check if GitHub Actions is implemented by fetching the contents of the .github/workflows directory.

    Args:
    - repository_url: The URL of the GitHub repository to check.

    Returns:
    - True if GitHub Actions is implemented, False otherwise.
    """
    api_url = f"{repository_url.rstrip('/')}/contents/.github/workflows"
    response = requests.get(api_url)
    return response.status_code == 200


def find_linters(repository_url):
    """
    Find linters specified for Python and R in the YAML files fetched from the repository.
    Prints the names of the linters.

    Args:
    - repository_url: The URL of the GitHub repository to check.
    """
    api_url = f"{repository_url.rstrip('/')}/contents/.github/workflows"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        for file in data:
            if file['type'] == 'file' and (file['name'].endswith('.yml') or file['name'].endswith('.yaml')):
                file_url = file['download_url']
                file_content = requests.get(file_url).text
                yaml_data = yaml.safe_load(file_content)
                for job in yaml_data.get('jobs', []):
                    if 'runs-on' in job and 'strategy' in job['runs-on'] and 'matrix' in job['runs-on']['strategy'] and 'linter' in job['runs-on']['strategy']['matrix']:
                        linter_name = job['runs-on']['strategy']['matrix']['linter']
                        print(f"Linter specified in '{file['name']}': {linter_name}")
    else:
        print("Error fetching repository contents.")


def get_programming_languages(repository_url):
    """
    Fetch and print the programming languages used in the repository.

    Args:
    - repository_url: The URL of the GitHub repository to check.
    """
    api_url = f"{repository_url.rstrip('/')}"
    response = requests.get(api_url)
    if response.status_code == 200:
        try:
            data = response.json()
            if 'language' in data:
                print(f"Programming languages used in the repository: {data['language']}")
            else:
                print("No programming language information found.")
        except Exception as e:
            print(f"Error decoding JSON response: {e}")
    else:
        print("Error fetching repository information.")


def main(repository_url):
    """
    Main function to check GitHub Actions implementation and linters in a repository.

    Args:
    - repository_url: The URL of the GitHub repository to check.
    """
    # Parse GitHub repository URL
    parsed_url = urlparse(repository_url)
    if parsed_url.netloc != 'github.com':
        print("Please provide a valid GitHub repository URL.")
        return

    # Check GitHub Actions implementation
    if check_github_actions(repository_url):
        print("GitHub Actions is implemented.")
        print("\nSearching for linters...")
        find_linters(repository_url)
    else:
        print("GitHub Actions is not implemented.")

    # Get and print programming languages used in the repository
    print("\nGetting programming languages used in the repository...")
    get_programming_languages(repository_url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check GitHub Actions implementation and programming languages used in a repository.")
    parser.add_argument("repository_url", help="GitHub repository URL.")
    args = parser.parse_args()
    main(args.repository_url)
