# This file is for testing the executable files before
# current executable command - test_folder.py --input results/bptlab_repostiories.csv

import os
import pandas as pd
import requests
import argparse

def check_test_folder(url):
    api_url = url.replace("https://github.com/", "https://api.github.com/repos/") + "/contents/"
    response = requests.get(api_url)

    if response.status_code == 200:
        content = response.json()
        for item in content:
            if item["type"] == "dir" and item["name"].lower() in ["test", "tests"]:
                return True
    return False

def check_automated_testing(url):
    api_url_makefile = url.replace("https://github.com/", "https://raw.githubusercontent.com/") + "/main/Makefile"
    api_url_yml = url.replace("https://github.com/",
                              "https://raw.githubusercontent.com/") + "/main/.github/workflows/ci.yml"

    response_makefile = requests.get(api_url_makefile)
    response_yml = requests.get(api_url_yml)

    if response_makefile.status_code == 200:
        makefile_content = response_makefile.text
        if "test" in makefile_content:
            return True

    if response_yml.status_code == 200:
        yml_content = response_yml.text
        if "test" in yml_content:
            return True

    return False

def check_cicd_pipeline(url):
    api_url_actions = url.replace("https://github.com/", "https://api.github.com/repos/") + "/actions"
    response_actions = requests.get(api_url_actions)

    if response_actions.status_code == 200:
        actions_data = response_actions.json()
        if actions_data.get("workflow_runs"):
            return True
    return False

def main(csv_file_path):
    # Read the CSV file
    df = pd.read_csv(csv_file_path, sep=',')

    # Initialize the new column
    df["actions"] = False

    # Iterate through the "html_url" column and populate the new columns
    for idx, row in df.iterrows():
        url = row["html_url"]
        df.at[idx, "test_folder"] = check_test_folder(url)
        df.at[idx, "automated_testing"] = check_automated_testing(url)
        df.at[idx, "actions"] = check_cicd_pipeline(url)

    # Overwrite the input CSV file with the updated DataFrame
    df.to_csv(csv_file_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check test folder, automated testing, and CI/CD in CSV file")
    parser.add_argument("input_csv", help="Path to the input CSV file")

    args = parser.parse_args()
    main(args.input_csv)