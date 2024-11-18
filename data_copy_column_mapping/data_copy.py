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
    src_table = config.get("src_table")
    dest_table = config.get("dest_table")

    # Validate required fields
    if not hostname or not database or not user or not password:
        print("Missing required fields: 'hostname', 'database', 'user', or 'password'.")
        return None

    uri = f"postgresql://{user}:{password}@{hostname}:{port}/{database}"
    return uri, src_table, dest_table

# Function to rename columns based on Excel input
def copy_data(database_uri, excel_file_path, sheet_name, src_table, dest_table):
    df = read_excel_file(excel_file_path, sheet_name)

    # Validate required columns
    if "src_column_name" not in df.columns or "dest_column_name" not in df.columns:
        print("Excel file must contain 'src_column_name' and 'dest_column_name' columns.")
        return

    # Convert the DataFrame to a dictionary
    mapping_dict = dict(zip(df['src_column_name'], df['dest_column_name']))

    # Step 3: Connect to the database
    engine = create_engine(database_uri)

    # Step 4: Copy data
    with engine.connect() as connection:
        # Fetch data from the category table
        category_columns = ', '.join(mapping_dict.keys())
        query = f"SELECT {category_columns} FROM category"
        category_data = pd.read_sql(query, connection)

        # Map columns to socialmediain
        socialmediain_data = category_data.rename(columns=mapping_dict)

        # Insert data into socialmediain
        socialmediain_data.to_sql('socialmediain', connection, if_exists='append', index=False)
        print("Data copied successfully!")

        # Close the connection
        connection.close()

# Path to the Excel file
excel_file_path = "column_mapping.xlsx"

db_uri, src_table, dest_table = create_data_uri(excel_file_path, 'database')

if not db_uri:
    copy_data(db_uri, excel_file_path, 'column_mapping', src_table, dest_table)
