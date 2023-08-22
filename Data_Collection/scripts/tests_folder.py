import requests
import os
import re
import argparse
from dotenv import load_dotenv


def check_testthat_use(url, username, access_token):
    repo_path = url.replace("https://github.com/", "")

    # Fetch the DESCRIPTION file content
    desc_url = f"https://raw.githubusercontent.com/{repo_path}/master/DESCRIPTION"

    headers = {
        "Authorization": f"token {access_token}",
        "User-Agent": username
    }

    response = requests.get(desc_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch the DESCRIPTION file for {url}. Status code: {response.status_code}")
        return False, None

    if "testthat" in response.text:
        # Check README for coverage badge
        readme_url = f"https://raw.githubusercontent.com/{repo_path}/master/README.md"
        response = requests.get(readme_url, headers=headers)

        if response.status_code == 200:
            coverage_match = re.search(r'coverage[-|_]\d+%?\.svg', response.text)
            if coverage_match:
                coverage = coverage_match.group().split('-')[1].split('.')[0]
                return True, coverage
        return True, None
    return False, None


if __name__ == "__main__":
    load_dotenv()

    USERNAME = os.getenv("USER")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

    parser = argparse.ArgumentParser(description='Check GitHub R repositories for testthat usage and test coverage.')
    parser.add_argument('repo_url', help='GitHub URL of the R repository.')
    args = parser.parse_args()

    uses_testthat, coverage = check_testthat_use(args.repo_url, USERNAME, ACCESS_TOKEN)
    if uses_testthat:
        print(f"'testthat' library is used in {args.repo_url}.")
        if coverage:
            print(f"Testing coverage: {coverage}")
        else:
            print("Testing coverage info not found.")
    else:
        print(f"'testthat' library is not used in {args.repo_url}.")
