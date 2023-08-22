import os
import pandas as pd
import requests
import argparse
from dotenv import load_dotenv

def check_test_folder(url, username, access_token):
    api_url = url.replace("https://github.com/", "https://api.github.com/repos/") + "/contents/"
    headers = {
        "Authorization": f"token {access_token}",
        "User-Agent": username
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        if response.status_code == 200:
            content = response.json()
            for item in content:
                if item["type"] == "dir" and item["name"].lower() in ["test", "tests"]:
                    return True
    except requests.RequestException as e:
        print(f"Error fetching repo contents: {e}")
    return False


def check_automated_testing(url, username, access_token):
    headers = {
        "Authorization": f"token {access_token}",
        "User-Agent": username
    }

    # Checking both main and master branches
    for branch in ['main', 'master']:
        api_url_makefile = url.replace("https://github.com/",
                                       "https://raw.githubusercontent.com/") + f"/{branch}/Makefile"
        api_url_yml = url.replace("https://github.com/",
                                  "https://raw.githubusercontent.com/") + f"/{branch}/.github/workflows/ci.yml"

        response_makefile = requests.get(api_url_makefile, headers=headers)
        response_yml = requests.get(api_url_yml, headers=headers)

        if response_makefile.status_code == 200 and "test" in response_makefile.text:
            return True

        if response_yml.status_code == 200 and "test" in response_yml.text:
            return True

    return False

def main(csv_file_path, username, access_token):
    df = pd.read_csv(csv_file_path, sep=',')
    for idx, row in df.iterrows():
        url = row["html_url"]
        df.at[idx, "test_folder"] = check_test_folder(url, username, access_token)
        df.at[idx, "automated_testing"] = check_automated_testing(url, username, access_token)
    
    df.to_csv(csv_file_path, index=False)

if __name__ == "__main__":
    load_dotenv()  # Load the .env file

    USERNAME = os.getenv("USER")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

    parser = argparse.ArgumentParser(description="Check test folder and automated testing in CSV file")
    parser.add_argument("--input", help="Path to the input CSV file", required=True)
    
    args = parser.parse_args()
    main(args.input, USERNAME, ACCESS_TOKEN)
