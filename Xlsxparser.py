import pandas as pd

# Load spreadsheet
xl = pd.ExcelFile('./DataSheets/CapstoneData.xlsx')

df = xl.parse(xl.sheet_names[0])

# Drop rows with any empty values
df = df.dropna(axis=0)

# Select the second and third columns (assuming 0-indexing)
df1 = df.iloc[:, [1, 2]]

# Write to csv
df1.to_csv('Audio1.csv', index=False)

# Check if the DataFrame has at least 7 columns (bug test)
if df.shape[1] >= 7:
    df2 = df.iloc[:, [5, 6]]

    # Write to csv
    df2.to_csv('Audio2.csv', index=False)
else:
    print("The DataFrame does not have enough columns.")