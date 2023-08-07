#command -  python test_folder.py results/pik_try.csv
# Change organization name below for execution and also change the name of .csv file from howfair


import argparse
import requests
import csv

# GitHub API credentials
api_key = "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"

organization = "pik-piam" # change the organisation name while execution for other organisations
keyword = "tests"

keyword2 = "test"

# API endpoints
base_url = "https://api.github.com"
headers = {
    "Authorization": f"Token {api_key}",
    "Accept": "application/vnd.github.v3+json"
}


def check_for_keyword_in_repo_contents(repo_name):
    try:
        # Check if the repository has the keyword in the root directory
        repo_content_url = f"{base_url}/repos/{organization}/{repo_name}/contents"
        response = requests.get(repo_content_url, headers=headers)
        response.raise_for_status()
        repo_contents = response.json()

        return any(content["type"] == "dir" and content["name"] == keyword for content in repo_contents)
    except requests.exceptions.RequestException as e:
        print(f"Error while fetching data for '{repo_name}': {str(e)}")
        return False


def check_for_keyword_in_make_file(repo_name):
    try:
        # Check if the repository has a GitHub Actions workflow file (make file)
        make_file_url = f"{base_url}/repos/{organization}/{repo_name}/contents/.github/workflows/make.yml"
        response = requests.get(make_file_url, headers=headers)
        if response.status_code == 200:
            make_file_content = response.json()["content"]
            make_file_content_decoded = make_file_content.encode("utf-8").decode("base64")
            return keyword2 in make_file_content_decoded
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error while fetching data for '{repo_name}': {str(e)}")
        return False


def main(csv_file):
    rows = []

    with open(csv_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames + ["test", "auto"]

        for row in reader:
            repo_name = row["name"]
            has_keyword_in_contents = check_for_keyword_in_repo_contents(repo_name)
            has_keyword_in_make_file = check_for_keyword_in_make_file(repo_name)

            row["test"] = str(has_keyword_in_contents)
            row["auto"] = str(has_keyword_in_make_file)
            rows.append(row)

    with open(csv_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Updated data appended to '{csv_file}'.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check repositories for keyword and make file and append data to CSV.")
    parser.add_argument("csv_file", help="Name of the CSV file containing repository data.")
    args = parser.parse_args()

    main(args.csv_file)
