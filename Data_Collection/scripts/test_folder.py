import pandas as pd
import requests
import os
import argparse
from dotenv import load_dotenv


def has_test_folder(url, username, access_token):
    print(f"Checking URL: {url}")  # Debug print

    repo_path = url.replace("https://github.com/", "")
    api_url = f"https://api.github.com/repos/{repo_path}/contents"

    headers = {
        "Authorization": f"token {access_token}",
        "User-Agent": username
    }

    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch data for {url}. Status code: {response.status_code}")
        return False

    for content in response.json():
        if content["type"] in ["file", "dir"] and "test" in content["name"].lower():
            return True
    return False


def update_csv_with_test_folder(filepath, username, access_token):
    # Read CSV using pandas
    df = pd.read_csv(filepath)

    # Check for the 'html_url' column
    if 'html_url' not in df.columns:
        print("The provided CSV file does not contain an 'html_url' column.")
        return

    # Apply the has_test_folder function to the html_url column
    df['test_folder'] = df['html_url'].apply(lambda url: has_test_folder(url, username, access_token))

    # Save the modified DataFrame back to the CSV file
    df.to_csv(filepath, index=False)


if __name__ == "__main__":
    load_dotenv()

    USERNAME = os.getenv("USER")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

    parser = argparse.ArgumentParser(description='Check GitHub repositories for test folders.')
    parser.add_argument('csv_path', help='Path to the CSV file containing GitHub repository URLs.')
    args = parser.parse_args()

    update_csv_with_test_folder(args.csv_path, USERNAME, ACCESS_TOKEN)
