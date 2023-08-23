import os
import pandas as pd


def get_all_csv_files(root_dir):
    """Get all .csv files from root_dir and its subdirectories."""
    csv_files = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.csv'):
                csv_files.append(os.path.join(dirpath, filename))

    return csv_files


def combine_csv_files(csv_files, output_file='../results/university_of_potsdam/combined.csv'):                # Change this path where you want to save the results
    """Combine the given list of .csv files into a single .csv file."""
    dfs = []

    for csv_file in csv_files:
        try:
            dfs.append(pd.read_csv(csv_file))
        except pd.errors.ParserError:
            print(f"Error reading file: {csv_file}. Skipping...")

    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df.to_csv(output_file, index=False)


if __name__ == "__main__":
    root_directory = "../results/university_of_potsdam"                                                      # Change this path from where you want to combine the files
    all_csv_files = get_all_csv_files(root_directory)

    if all_csv_files:
        combine_csv_files(all_csv_files)
        print(f"All successfully read .csv files have been combined into combined.csv")
    else:
        print("No .csv files found.")
