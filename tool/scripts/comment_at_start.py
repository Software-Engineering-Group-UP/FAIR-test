"""
This script checks all Python and R files in a GitHub repository for a starting comment.
It uses the GitHub API to fetch the contents of each file in the repository.
The GitHub token is read from a .env file in the root directory.
The script is executable and accepts the repository URL as a command-line argument.
"""

import os
import requests
import argparse
from dotenv import load_dotenv
import base64

def check_comment(file_content):
    """
    Check if a file starts with a comment.

    Args:
    - file_content: The content of the file to check.

    Returns:
    - True if the file starts with a comment, False otherwise.
    """
    lines = file_content.split('\n')
    for line in lines:
        stripped_line = line.strip()
        if stripped_line:  # if the line is not empty
            if stripped_line.startswith('#') or stripped_line.startswith('%'):
                return True
            else:
                return False
    return False

def check_repository(repo_url, github_token):
    """
    Check all Python and R files in a GitHub repository for a starting comment.

    Args:
    - repo_url: The URL of the GitHub repository to check.
    - github_token: The GitHub token to use for authentication.

    Returns:
    - A dictionary mapping file paths to a boolean indicating if the file starts with a comment.
    """
    # Parse owner and repo from URL
    split_url = repo_url.split('/')
    repo_owner = split_url[-2]
    repo_name = split_url[-1]

    # Set up session with GitHub token
    session = requests.Session()
    session.headers.update({'Authorization': f'token {github_token}'})

    # Get list of all files in repository
    page = 1
    file_list = []
    while True:
        response = session.get(f'https://api.github.com/repos/{repo_owner}/{repo_name}/git/trees/master?recursive=1&page={page}')
        response.raise_for_status()
        data = response.json()
        file_list.extend([file['path'] for file in data['tree'] if file['type'] == 'blob' and (file['path'].endswith('.py') or file['path'].endswith('.r'))])
        if 'next' in response.links:
            page += 1
        else:
            break

    # Check each file for a starting comment
    results = {}
    total_files = 0
    files_with_comments = 0
    files_without_comments = 0
    for file_path in file_list:
        total_files += 1
        response = session.get(f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}')
        response.raise_for_status()
        data = response.json()
        file_content = base64.b64decode(data['content']).decode('utf-8')
        has_comment = check_comment(file_content)
        results[file_path] = has_comment
        if has_comment:
            files_with_comments += 1
        else:
            files_without_comments += 1

    return results, total_files, files_with_comments, files_without_comments

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check a GitHub repository for starting comments in Python and R files.')
    parser.add_argument('repo_url', help='The URL of the GitHub repository to check.')
    args = parser.parse_args()

    # Load GitHub token from .env file
    load_dotenv()
    github_token = os.getenv('GITHUB_ACCESS_TOKEN')

    results, total_files, files_with_comments, files_without_comments = check_repository(args.repo_url, github_token)
    print(f'Total Python/R files scanned: {total_files}')
    print(f'Files with starting comment: {files_with_comments}')
    print(f'Files without starting comment: {files_without_comments}')