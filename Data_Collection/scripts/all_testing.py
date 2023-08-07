"""
write a python program to iterate through  column name "html_url" from a csv file and find out if given url has test or tests named folder (which is used code for testing) in the root directory also find out if test keyword is present in make file or yml file used for automated testing in cicd and write the result in same csv file with column names test_folder and automated_testing

to run this file command- python check_testing.py input.csv output.csv

Status -

"""

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
    api_url_yml = url.replace("https://github.com/", "https://raw.githubusercontent.com/") + "/main/.github/workflows/ci.yml"

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

def main(csv_file_path, output_file_path):
    # Read the CSV file
    df = pd.read_csv(csv_file_path, sep=';')

    # Initialize the new columns
    df["test_folder"] = False
    df["automated_testing"] = False

    # Iterate through the "html_url" column and populate the new columns
    for idx, row in df.iterrows():
        url = row["html_url"]
        df.at[idx, "test_folder"] = check_test_folder(url)
        df.at[idx, "automated_testing"] = check_automated_testing(url)

    # Save the updated DataFrame back to the CSV file
    df.to_csv(output_file_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check test folder and automated testing in CSV file")
    parser.add_argument("input_csv", help="Path to the input CSV file")
    parser.add_argument("output_csv", help="Path to save the output CSV file")

    args = parser.parse_args()
    main(args.input_csv, args.output_csv)

