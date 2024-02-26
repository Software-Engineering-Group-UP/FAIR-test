"""
This script checks all Python and R files in a GitHub repository for a starting comment. It uses the GitHub API to fetch the contents of each file in the repository. The GitHub token is read from a .env file in the root directory. The script is executable and accepts the repository URL as a command-line argument.

The program performs the following functions:

Checks if a file starts with a comment.
Checks all Python and R files in a GitHub repository for a starting comment.
Traverses all subdirectories of a GitHub repository and checks for starting comments in Python and R files.
Gets the names of all folders in the root directory of a GitHub repository.
Checks if the repository contains files named 'requirements.txt', 'requirements.md', 'changelog.txt', or 'changelog.md'.
Gets all libraries imported in a Python or R file.
Checks all Python and R files in a GitHub repository for imported libraries.

Executable command example- 
python comment_at_start.py https://api.github.com/repos/aadeshnpn/swarm  
"""

import os
import requests
import argparse
from dotenv import load_dotenv
import base64
import re

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
            if stripped_line.startswith('#') or stripped_line.startswith('%') or stripped_line.startswith('"""') or stripped_line.startswith("'''"):
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
    file_list = []
    page = 1
    while True:
        response = session.get(f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents?recursive=1&page={page}')
        response.raise_for_status()
        data = response.json()
        file_list.extend([file['path'] for file in data if file['type'] == 'file' and (file['path'].endswith('.py') or file['path'].endswith('.r'))])
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

def traverse_subdirectories(repo_url, github_token):
    """
    Traverse all subdirectories of a GitHub repository and check for starting comments in Python and R files.

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

    # Get list of all directories in repository
    directory_list = []
    page = 1
    while True:
        response = session.get(f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents?recursive=1&page={page}')
        response.raise_for_status()
        data = response.json()
        directory_list.extend([file['path'] for file in data if file['type'] == 'dir'])
        if 'next' in response.links:
            page += 1
        else:
            break

    # Traverse each subdirectory and check for starting comments in Python and R files
    results = {}
    for directory_path in directory_list:
        response = session.get(f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{directory_path}')
        response.raise_for_status()
        data = response.json()
        file_list = [file['path'] for file in data if file['type'] == 'file' and (file['path'].endswith('.py') or file['path'].endswith('.r'))]
        for file_path in file_list:
            response = session.get(f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}')
            response.raise_for_status()
            data = response.json()
            file_content = base64.b64decode(data['content']).decode('utf-8')
            has_comment = check_comment(file_content)
            results[file_path] = has_comment

    return results

def get_root_folders(repo_url, github_token):
    """
    Get the names of all folders in the root directory of a GitHub repository.

    Args:
    - repo_url: The URL of the GitHub repository to check.
    - github_token: The GitHub token to use for authentication.

    Returns:
    - A list of folder names.
    """
    # Parse owner and repo from URL
    split_url = repo_url.split('/')
    repo_owner = split_url[-2]
    repo_name = split_url[-1]

    # Set up session with GitHub token
    session = requests.Session()
    session.headers.update({'Authorization': f'token {github_token}'})

    # Get list of all items in root directory
    response = session.get(f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents')
    response.raise_for_status()
    data = response.json()

    # Filter out the directories
    folder_names = [item['name'] for item in data if item['type'] == 'dir']

    return folder_names

def check_special_files(repo_url, github_token):
    """
    Check if the repository contains files named 'requirements.txt', 'requirements.md', 'changelog.txt', or 'changelog.md'.

    Args:
    - repo_url: The URL of the GitHub repository to check.
    - github_token: The GitHub token to use for authentication.

    Returns:
    - A dictionary mapping the special file names to a boolean indicating if the file is present in the repository.
    """
    # Parse owner and repo from URL
    split_url = repo_url.split('/')
    repo_owner = split_url[-2]
    repo_name = split_url[-1]

    # Set up session with GitHub token
    session = requests.Session()
    session.headers.update({'Authorization': f'token {github_token}'})

    # Define the special file names to check for
    special_files = ['requirements.txt', 'requirements.md', 'changelog.txt', 'changelog.md']

    # Check for the presence of each special file
    results = {}
    for file_name in special_files:
        response = session.get(f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_name}')
        results[file_name] = response.status_code == 200

    return results

def get_imported_libraries(file_content, file_type):
    """
    Get all libraries imported in a Python or R file.

    Args:
    - file_content: The content of the file to check.
    - file_type: The type of the file ('.py' for Python, '.r' for R).

    Returns:
    - A list of libraries imported in the file.
    """
    libraries = []
    if file_type == '.py':
        matches = re.findall(r'^import (\S+)|^from (\S+) import', file_content, re.MULTILINE)
        for match in matches:
            libraries.append(match[0] if match[0] else match[1])
    elif file_type == '.r':
        matches = re.findall(r'library\((.*?)\)', file_content)
        libraries.extend(matches)
    return libraries

def check_libraries(repo_url, github_token):
    """
    Check all Python and R files in a GitHub repository for imported libraries.

    Args:
    - repo_url: The URL of the GitHub repository to check.
    - github_token: The GitHub token to use for authentication.

    Returns:
    - A dictionary mapping file paths to a list of libraries imported in the file.
    """
    # Parse owner and repo from URL
    split_url = repo_url.split('/')
    repo_owner = split_url[-2]
    repo_name = split_url[-1]

    # Set up session with GitHub token
    session = requests.Session()
    session.headers.update({'Authorization': f'token {github_token}'})

    # Get list of all files in repository
    file_list = []
    page = 1
    while True:
        response = session.get(f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents?recursive=1&page={page}')
        response.raise_for_status()
        data = response.json()
        file_list.extend([file for file in data if file['type'] == 'file' and (file['path'].endswith('.py') or file['path'].endswith('.r'))])
        if 'next' in response.links:
            page += 1
        else:
            break

    # Check each file for imported libraries
    results = {}
    for file in file_list:
        response = session.get(f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file['path']}")
        response.raise_for_status()
        data = response.json()
        file_content = base64.b64decode(data['content']).decode('utf-8')
        libraries = get_imported_libraries(file_content, '.py' if file['path'].endswith('.py') else '.r')
        results[file['path']] = libraries

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check a GitHub repository for starting comments in Python and R files.')
    parser.add_argument('repo_url', help='The URL of the GitHub repository to check.')
    args = parser.parse_args()

    # Load GitHub token from .env file
    load_dotenv()
    github_token = os.getenv('GITHUB_ACCESS_TOKEN')

    # Check repository for starting comments
    results, total_files, files_with_comments, files_without_comments = check_repository(args.repo_url, github_token)
    print(f'Total Python/R files scanned: {total_files}')
    print(f'Files with starting comment: {files_with_comments}')
    print(f'Files without starting comment: {files_without_comments}')

    # Traverse subdirectories and check for starting comments
    subdirectory_results = traverse_subdirectories(args.repo_url, github_token)
    print(f'Total subdirectories scanned: {len(subdirectory_results)}')
    print(f'Subdirectories with starting comment: {len([result for result in subdirectory_results.values() if result])}')
    print(f'Subdirectories without starting comment: {len([result for result in subdirectory_results.values() if not result])}')

    # Get and print folder names in root directory
    folder_names = get_root_folders(args.repo_url, github_token)
    print(f'Folders in the root directory of the repository: {folder_names}')

    # Check for the presence of special files
    special_file_results = check_special_files(args.repo_url, github_token)
    print(f'Special file presence: {special_file_results}')

    # Check repository for imported libraries
    library_results = check_libraries(args.repo_url, github_token)
    print(f'Imported libraries: {library_results}')
    