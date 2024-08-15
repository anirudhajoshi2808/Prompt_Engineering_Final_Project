import snowflake.connector
import os
from dotenv import load_dotenv
import csv

load_dotenv()

# Establish connection using environment variables
conn = snowflake.connector.connect(
    user=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASSWORD'),
    account=os.getenv('SNOWFLAKE_ACCOUNT'),
    warehouse='SF_WH_CASE1',
    role='ACCOUNTADMIN'
)

# Query data
cursor = conn.cursor()
cursor.execute("SELECT * FROM SF_DB_CASE1.SF_CASE1.CLEANED_ONLINE_COURSES")
rows = cursor.fetchall()

cursor.close()
conn.close()
def format_row_with_separator(row, separator='####'):
    # Convert each cell to string, and wrap with quotes if it contains a comma
    formatted_cells = [
        f'"{str(cell)}"' if ',' in str(cell) else str(cell) for cell in row
    ]
    # Join all cells in the row into a single string with commas, 
    # then wrap the entire string with separators at the start and end
    return f"{separator}{','.join(formatted_cells)}{separator}"

# Assume `rows` is your list of rows fetched from Snowflake
formatted_rows = [format_row_with_separator(row) for row in rows]

# Save the formatted rows into a text file
with open('output.txt', 'w') as f:
    for formatted_row in formatted_rows:
        f.write(formatted_row + '\n')

