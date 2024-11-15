import pandas as pd
from sqlalchemy import create_engine

def read_excel_file(excel_file_path, sheet_name=None):
    # Step 1: Load Excel file
    try:
        if sheet_name:
            df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
        else:
            df = pd.read_excel(excel_file_path)
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None

    return df

def create_data_uri(excel_file_path, sheet_name=None):
    # Step 1: Load Excel file
    df = read_excel_file(excel_file_path, sheet_name)

    if not df:
        return None

    if "field" not in df.columns or "value" not in df.columns:
        print("Excel file must contain 'field' and 'value'")
        return None

    # Convert the DataFrame to a dictionary
    config = dict(zip(df['field'], df['value']))

    # Extract configuration details
    hostname = config.get("hostname", "")
    database = config.get("database", "")
    user = config.get("user", "")
    password = config.get("password", "")
    port = config.get("port", 5432)  # Default port for PostgreSQL

    # Validate required fields
    if not hostname or not database or not user or not password:
        print("Missing required fields: 'hostname', 'database', 'user', or 'password'.")
        return None

    uri = f"postgresql://{user}:{password}@{hostname}:{port}/{database}"
    return uri

# Function to rename columns based on Excel input
def rename_columns_from_excel(database_uri, excel_file_path, sheet_name=None):
    # Step 1: Load Excel file
    df = read_excel_file(excel_file_path, sheet_name)

    # Validate required columns
    if "table_name" not in df.columns or "old_column_name" not in df.columns or "new_column_name" not in df.columns:
        print("Excel file must contain 'table_name', 'old_column_name', and 'new_column_name' columns.")
        return

    # Step 2: Connect to the database
    try:
        engine = create_engine(database_uri)
        connection = engine.connect()
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return

    # Step 3: Rename columns
    for _, row in df.iterrows():
        table_name = row["table_name"]
        old_column = row["old_column_name"]
        new_column = row["new_column_name"]

        try:
            sql = f"ALTER TABLE {table_name} RENAME COLUMN {old_column} TO {new_column};"
            connection.execute(sql)
            print(f"Renamed column '{old_column}' to '{new_column}' in table '{table_name}'.")
        except Exception as e:
            print(f"Error renaming column '{old_column}' to '{new_column}' in table '{table_name}': {e}")

    # Close the connection
    connection.close()
    print("Column renaming process completed.")

# Path to the Excel file
excel_file_path = "change_column_name.xlsx"

db_uri = create_data_uri(excel_file_path, 'database')

if not db_uri:
    rename_columns_from_excel(db_uri, excel_file_path, 'change_column_name')
