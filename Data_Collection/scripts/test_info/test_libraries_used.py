import requests
import re

# Categories and their corresponding Python libraries
categories = {
    'Profiling': ['cProfile', 'profile', 'py-spy'],
    'Parallel Computing': ['concurrent.futures', 'multiprocessing', 'joblib'],
    'Data Manipulation': ['pandas', 'numpy'],
    'Memory Management': ['gc', 'objgraph'],
    'GPU Acceleration': ['tensorflow', 'pytorch', 'cupy'],
    'Cloud Computing': ['boto3', 'google-cloud-storage'],
}

def find_libraries_in_file(file_content):
    used_libraries = {}
    for category, libs in categories.items():
        for lib in libs:
            if re.search(f'import {lib}|from {lib} import', file_content):
                if category not in used_libraries:
                    used_libraries[category] = []
                used_libraries[category].append(lib)
    return used_libraries

def main():
    # Replace YOUR_GITHUB_TOKEN with your GitHub Personal Access Token
    YOUR_GITHUB_TOKEN = ''
    # Replace REPO_OWNER and REPO_NAME with the GitHub repository details
    REPO_OWNER = 'GFZ'
    REPO_NAME = 'spechomo'

    headers = {'Authorization': f'token {YOUR_GITHUB_TOKEN}'}
    repo_url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/trees/main?recursive=1'

    r = requests.get(repo_url, headers=headers)

    if r.status_code != 200:
        print(f"API request failed with status code {r.status_code}: {r.json().get('message', 'Unknown error')}")
        return

    response_json = r.json()
    if 'tree' not in response_json:
        print("Could not find 'tree' in API response. Response content:")
        print(response_json)
        return

    tree = response_json['tree']
    py_files = [file for file in tree if file['path'].endswith('.py')]

    for py_file in py_files:
        blob_url = py_file['url']
        r = requests.get(blob_url, headers=headers)
        blob_content = r.json()['content']
        file_content = requests.utils.unquote(blob_content)
        used_libraries = find_libraries_in_file(file_content)

        if used_libraries:
            print(f'Libraries used in {py_file["path"]}:')
            for category, libs in used_libraries.items():
                print(f'  {category}: {", ".join(libs)}')

if __name__ == '__main__':
    main()
