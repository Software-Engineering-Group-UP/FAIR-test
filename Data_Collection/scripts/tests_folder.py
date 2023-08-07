# python script_name.py your_input.csv


import argparse
import requests
import csv

# GitHub API credentials
api_key = ""  # Your GitHub API token here

# API endpoint
base_url = "https://api.github.com"
headers = {
    "Authorization": f"Token {api_key}",
    "Accept": "application/vnd.github.v3+json"
}


def check_for_tests_folder(repo_name):
    try:
        # Check if the repository has a folder named "tests" in the root directory
        repo_content_url = f"{base_url}/repos/{repo_name}/contents"
        response = requests.get(repo_content_url, headers=headers)
        response.raise_for_status()
        repo_contents = response.json()

        return any(content["type"] == "dir" and content["name"] == "tests" for content in repo_contents)
    except requests.exceptions.RequestException as e:
        print(f"Error while fetching data for '{repo_name}': {str(e)}")
        return False


def main(csv_file):
    rows = []

    with open(csv_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames + ["test_folder"]

        for row in reader:
            repo_name = row["name"]
            has_tests_folder = check_for_tests_folder(repo_name)

            row["test_folder"] = str(has_tests_folder)
            rows.append(row)

    with open(csv_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Updated data appended to '{csv_file}'.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check GitHub repositories for the presence of 'tests' folder and append data to CSV.")
    parser.add_argument("csv_file", help="Name of the CSV file containing repository data.")
    args = parser.parse_args()

    main(args.csv_file)
