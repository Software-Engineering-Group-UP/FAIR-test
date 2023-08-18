'''

 python append_org_researchGroup_name.py ../results/university_of_potsdam/AEye/aeye-lab.csv --organization "university_of_potsdam" --research_group "aeya"

'''



import argparse
import pandas as pd

def update_csv(csv_file, organization, research_group):
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Update the "organisation" and "researchGroup" columns with provided values
    df["organisation"] = organization
    df["researchGroup"] = research_group

    # Save the updated DataFrame back to the CSV file
    df.to_csv(csv_file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update CSV file with organization and research group values")
    parser.add_argument("csv_file", help="Path to the CSV file")
    parser.add_argument("--organization", "-o", required=True, help="Value for the 'organisation' column")
    parser.add_argument("--research_group", "-r", required=True, help="Value for the 'researchGroup' column")

    args = parser.parse_args()

    update_csv(args.csv_file, args.organization, args.research_group)
    print(f"CSV file '{args.csv_file}' updated with organization '{args.organization}' and research group '{args.research_group}'.")
