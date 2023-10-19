import pandas as pd

# Load the JSON data into a pandas DataFrame
json_data = pd.read_json('rappels.json', dtype=str)

# Convert the DataFrame to an Excel file
excel_file = 'rappels.xlsx'
json_data.to_excel(excel_file, index=False)
