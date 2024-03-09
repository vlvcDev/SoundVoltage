import pandas as pd

# Load spreadsheet
xl = pd.ExcelFile('./DataSheets/CapstoneData.xlsx')

df = xl.parse(xl.sheet_names[0])

# Drop columns with any empty values
df = df.dropna(axis=1)

# Select the second and third columns (assuming 0-indexing)
df1 = df.iloc[:, [1, 2]]

# Write to csv
df1.to_csv('Audio1.csv', index=False)

# Select the sixth and seventh columns (assuming 0-indexing)
df2 = df.iloc[:, [5, 6]]

# Write to csv
df2.to_csv('Audio2.csv', index=False)