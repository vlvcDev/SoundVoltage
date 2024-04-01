import pandas as pd
import os

# Define the directories
data_dir = './DataSheets'
output_dir = './ConvertedSheets'

# Check if output directory exists, if not, create it
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop through each file in the data directory
for filename in os.listdir(data_dir):
    if filename.endswith('.csv'):
        # Read the CSV file
        df = pd.read_csv(os.path.join(data_dir, filename))

        # Drop the first column
        df = df.drop(df.columns[0], axis=1)

        # Write the new CSV file to the output directory
        df.to_csv(os.path.join(output_dir, filename), index=False)