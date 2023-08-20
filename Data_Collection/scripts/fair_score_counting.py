'''

 python fair_score_counting.py input.csv


This program counts the number of true values from column names  'howfairis_repository', 'howfairis_license', 'howfairis_registry', 'howfairis_citation', 'howfairis_checklist' and saves them to column called fair_score
'''



import pandas as pd
import argparse

def calculate_fair_score(dataframe):
    # Select the desired columns
    columns = ['howfairis_repository', 'howfairis_license', 'howfairis_registry', 'howfairis_citation', 'howfairis_checklist']

    # Count 'True' values along the columns for each row
    dataframe['fair_score'] = dataframe[columns].sum(axis=1)

    return dataframe

if __name__ == "__main__":
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Calculate the FAIR score from specified columns in a CSV file.")
    parser.add_argument("filename", type=str, help="Path to the CSV file.")

    args = parser.parse_args()

    # Read the CSV file
    data = pd.read_csv(args.filename)

    # Calculate the FAIR score
    updated_data = calculate_fair_score(data)

    # Save the updated DataFrame back to the original CSV file
    updated_data.to_csv(args.filename, index=False)
    print(f"Updated data saved back to {args.filename}")
