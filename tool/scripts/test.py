"""
This script reads the content of a file from a GitHub repository.

It uses the GitHub API to fetch the file content. The URL of the file is provided as a command line argument.
The script also requires a GitHub access token, which is read from a .env file in the root directory.

Usage:
    python script.py https://api.github.com/repos/owner/repo/contents/path

Replace 'script.py' with the actual name of your script, and 'https://api.github.com/repos/owner/repo/contents/path' 
with the actual URL of the file you want to read.

Before running the script, make sure to create a .env file in the same directory as your script with the following content:
    GITHUB_TOKEN=your_github_token
Replace 'your_github_token' with your actual GitHub token.
"""

import argparse
import os
from dotenv import load_dotenv
import requests

def get_file_content(url, token):
    headers = {'Authorization': f'token {token}'}
    url = f"{url}/git/trees/master?recursive=1"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tree = response.json()
        r_files = sum(1 for item in tree['tree'] if item['path'].endswith('.r'))
        python_files = sum(1 for item in tree['tree'] if item['path'].endswith('.python'))
        return r_files, python_files
    else:
        return None

def main():
    parser = argparse.ArgumentParser(description='Count .r and .python files in a GitHub repository.')
    parser.add_argument('url', help='The URL of the repository on GitHub.')
    args = parser.parse_args()

    def count_files(url, token):
        headers = {'Authorization': f'token {token}'}
        url = f"{url}/git/trees/master?recursive=1"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            tree = response.json()
            r_files = sum(1 for item in tree['tree'] if item['path'].endswith('.r'))
            python_files = sum(1 for item in tree['tree'] if item['path'].endswith('.python'))
            return r_files, python_files
        else:
            print(f"Request failed with status code {response.status_code}")
            print(f"Response text: {response.text}")
            return None

    load_dotenv()
    token = os.getenv('GITHUB_ACCESS_TOKEN')

    if token is None:
        print('GitHub token not found in .env file.')
        return

    result = count_files(args.url, token)
    if result is not None:
        r_files, python_files = result
        print(f"Number of .r files: {r_files}")
        print(f"Number of .python files: {python_files}")
    else:
        print('Failed to get file list.')

if __name__ == '__main__':
    main()