import pandas as pd
import os

data_dir = './DataSheets'
output_dir = './ConvertedSheets'

def csv_clean():
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Loop through each file in the data directory
    for filename in os.listdir(data_dir):
        if filename.endswith('.csv'):
            df = pd.read_csv(os.path.join(data_dir, filename))

            # Drop the first column
            df = df.drop(df.columns[0], axis=1)

            df.to_csv(os.path.join(output_dir, filename), index=False)

def clean_selected(file_path):
    print("Cleaning selected file:", file_path)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    df = pd.read_csv(file_path)

    # Drop the first column
    df = df.drop(df.columns[0], axis=1)

    df.to_csv(os.path.join(output_dir, os.path.basename("clean_audio.csv")), index=False)