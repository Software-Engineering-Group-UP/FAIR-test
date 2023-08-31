# Filters coulmn names with programming languages r and python with automated testing = true
import pandas as pd
import argparse


def filter_and_save_csv(input_file, output_file):
    # Step 1: Read the CSV file into a DataFrame
    df = pd.read_csv(input_file)

    # Step 2: Filter the rows based on conditions
    filtered_df = df[
        ((df['language'] == 'Python') | (df['language'] == 'R')) &
        (df['automated_testing'] == True)  # Assuming the 'automated_testing' column contains boolean values
        ]

    # Step 3: Save the filtered DataFrame to a new CSV file
    filtered_df.to_csv(output_file, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Filter rows from a CSV file.')
    parser.add_argument('input_file', type=str, help='Input CSV file name')
    parser.add_argument('output_file', type=str, help='Output CSV file name')

    args = parser.parse_args()

    filter_and_save_csv(args.input_file, args.output_file)
