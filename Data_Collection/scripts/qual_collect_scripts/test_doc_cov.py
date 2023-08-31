# Program to write testing documentation/ coverage done on the repository
# run the program using command python update_csv_file.py my_data.csv "http://example.com/page1" True "Method A" 95.0

import pandas as pd
import argparse


def update_csv_file(input_file, html_url, test_document, test_document_method, coverage):
    # Step 1: Read the existing CSV file into a DataFrame
    df = pd.read_csv(input_file)

    # Step 2: Check if the required columns exist in the DataFrame
    required_columns = ['html_url', 'test_document', 'test_document_method', 'coverage']
    missing_columns = [col for col in required_columns if col not in df.columns]

    # Step 3: If any columns are missing, add them with default values
    for col in missing_columns:
        if col == 'test_document':
            df[col] = False  # Default boolean value
        elif col == 'test_document_method':
            df[col] = 'N/A'  # Default string value
        elif col == 'coverage':
            df[col] = 0.0  # Default numerical value
        else:
            df[col] = 'N/A'  # Default string value for 'html_url'

    # Step 4: Find the index of the row where html_url matches
    idx = df[df['html_url'] == html_url].index

    if len(idx) == 0:
        print(f"No matching rows found for html_url: {html_url}")
        return

    # Step 5: Update the DataFrame with new values
    df.loc[idx, 'test_document'] = test_document
    df.loc[idx, 'test_document_method'] = test_document_method
    df.loc[idx, 'coverage'] = coverage

    # Step 6: Save the updated DataFrame back to the CSV file
    df.to_csv(input_file, index=False)
    print(f"Successfully updated row with html_url: {html_url}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update specific columns in a CSV file.')

    parser.add_argument('input_file', type=str, help='CSV file to update')
    parser.add_argument('html_url', type=str, help='HTML URL to match in the CSV file')
    parser.add_argument('test_document', type=lambda x: (str(x).lower() == 'true'),
                        help='Boolean value for test_document')
    parser.add_argument('test_document_method', type=str, help='String value for test_document_method')
    parser.add_argument('coverage', type=float, help='Numerical value for coverage')

    args = parser.parse_args()

    update_csv_file(args.input_file, args.html_url, args.test_document, args.test_document_method, args.coverage)

