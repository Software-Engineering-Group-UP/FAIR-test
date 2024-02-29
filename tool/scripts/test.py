import csv
import os
import requests
import base64
import re
from dotenv import load_dotenv

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
    - The total number of files scanned.
    - The number of files with a starting comment.
    - The number of files without a starting comment.
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
        file_list.extend([file['path'] for file in data if file['type'] == 'file' and (file['path'].endswith('.py') or file['path'].endswith('.r') or file['path'].endswith('.R'))])
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

    # Calculate percentage of files with comments
    percentage_with_comments = (files_with_comments / total_files) * 100 if total_files > 0 else 0

    return percentage_with_comments


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
        file_list = [file['path'] for file in data if file['type'] == 'file' and (file['path'].endswith('.py') or file['path'].endswith('.r') or file['path'].endswith('.R'))]
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

def read_repository_urls(csv_file):
    """
    Read repository URLs from a CSV file.

    Args:
    - csv_file: The path to the CSV file containing repository URLs.

    Returns:
    - A list of repository URLs.
    """
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        urls = [row[0] for row in reader]
    return urls

def execute_and_write_results(csv_file, output_file):
    """
    Execute the functions on repository URLs read from the CSV file and write the results to an output CSV file.

    Args:
    - csv_file: The path to the CSV file containing repository URLs.
    - output_file: The path to the output CSV file where results will be written.
    """
    # Load GitHub token from .env file
    load_dotenv()
    github_token = os.getenv('GITHUB_ACCESS_TOKEN')

    # Read repository URLs from the CSV file
    repository_urls = read_repository_urls(csv_file)

    # Execute functions on each repository URL and write results to output CSV file
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Repository URL', 'Total Files', 'Files with Comment', 'Files without Comment', 'Total Subdirectories', 'Subdirectories with Comment', 'Subdirectories without Comment', 'Folder Names', 'Special File Presence'])
        
        for repo_url in repository_urls:
            results, total_files, files_with_comments, files_without_comments = check_repository(repo_url, github_token)
            subdirectory_results = traverse_subdirectories(repo_url, github_token)
            folder_names = get_root_folders(repo_url, github_token)
            special_file_results = check_special_files(repo_url, github_token)
            
            writer.writerow([repo_url, total_files, files_with_comments, files_without_comments, len(subdirectory_results), sum(subdirectory_results.values()), len(subdirectory_results) - sum(subdirectory_results.values()), folder_names, special_file_results])

# Example usage
execute_and_write_results('akshay.csv', 'akshay.csv')
