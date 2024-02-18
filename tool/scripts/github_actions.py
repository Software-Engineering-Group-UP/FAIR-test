import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def check_linter_jobs(repository_url):
    """
    Check if the .yaml or .yml files in the .github/workflows directory execute linter jobs.

    Args:
    - repository_url: The URL of the GitHub repository to check.

    Returns:
    - True if linter jobs are executed, False otherwise.
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

        # Check if any YAML files exist in .github/workflows directory and execute linter jobs
        for file in data:
            if file['type'] == 'file' and (file['name'].endswith('.yml') or file['name'].endswith('.yaml')):
                file_url = file['download_url']
                file_content = requests.get(file_url).text

                # Check if the file content contains linter jobs
                if 'linter' in file_content:
                    return True

    # Linter jobs not found if the code reaches here
    return False

if __name__ == "__main__":
    repository_url = input("Enter the GitHub repository URL: ")
    if check_linter_jobs(repository_url):
        print("Linter jobs are executed in the repository.")
    else:
        print("Linter jobs are not executed in the repository.")
