import os
import pandas as pd
from dotenv import load_dotenv
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from pathlib import Path

# Load environment variables
load_dotenv()

# Establish a connection to Snowflake without specifying database and schema
conn = snowflake.connector.connect(
    user=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASSWORD'),
    account=os.getenv('SNOWFLAKE_ACCOUNT'),
    warehouse='SF_WH_CASE1',
    role='ACCOUNTADMIN'
)

# Create and/or use the specified database and schema
conn.cursor().execute("CREATE DATABASE IF NOT EXISTS SF_DB_CASE1")
conn.cursor().execute("CREATE SCHEMA IF NOT EXISTS SF_DB_CASE1.SF_CASE1")
conn.cursor().execute("USE DATABASE SF_DB_CASE1")
conn.cursor().execute("USE SCHEMA SF_CASE1")

# Function to map pandas data types to Snowflake SQL types
def pandas_dtype_to_snowflake_sql_type(dtype):
    mapping = {
        'int64': 'NUMBER',
        'float64': 'FLOAT',
        'bool': 'BOOLEAN',
        'datetime64[ns]': 'TIMESTAMP_NTZ',
        'object': 'VARCHAR'
    }
    return mapping.get(str(dtype), 'VARCHAR')

# Function to dynamically create tables based on DataFrame's structure
def create_table_from_df(df, table_name, conn):
    column_definitions = ', '.join([f'"{col.upper()}" {pandas_dtype_to_snowflake_sql_type(str(dtype))}' for col, dtype in df.dtypes.items()])
    create_table_sql = f"CREATE OR REPLACE TABLE {table_name} ({column_definitions})"
    conn.cursor().execute(create_table_sql)

# Function to upload a CSV file to Snowflake, filtering specific columns
def upload_csv_to_snowflake(csv_path, table_name, conn):
    required_columns = [
        'Title', 'URL', 'Short Intro', 'Category', 'Sub-Category', 'Course Type',
        'Language', 'Subtitle Languages', 'Skills', 'Instructors', 'Rating',
        'Number of viewers', 'Duration', 'Site'
    ]
    
    df = pd.read_csv(csv_path)
    
    # Ensure we are only transferring the required columns
    df = df[required_columns]
    
    # Ensure column names are uppercase for Snowflake compatibility
    df.columns = [col.upper() for col in df.columns]
    
    # Create table in Snowflake
    create_table_from_df(df, table_name, conn)
    
    # Transfer data to Snowflake
    write_pandas(conn, df, table_name.upper())
    
    print("Data Transfer Completed!!")

if __name__ == "__main__":
    project_root = Path(__file__).parent

    # Path to the cleaned CSV file
    csv_file_path = project_root / 'data' / 'cleaned_online_courses.csv'
    table_name = 'CLEANED_ONLINE_COURSES'

    # Upload the CSV to Snowflake
    if os.path.exists(csv_file_path):
        upload_csv_to_snowflake(csv_file_path, table_name, conn)
    else:
        print(f"File not found: {csv_file_path}")

    # Close the Snowflake connection
    conn.close()
