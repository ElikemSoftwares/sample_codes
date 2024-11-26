import os
import subprocess
import datetime
import psycopg2

# Database configuration
source_db = {
    "host": "10.133.132.90",
    "database": "cno_prod",
    "user": "postgres",
    "password": "12345",
    "port": "5432"
}

target_db = {
    "host": "10.129.7.247",
    "database": "TPGA01",
    "user": "postgres",
    "password": "postgres",
    "port": "5431"
}

tables = []
backup_dir = "/tmp"  # Temporary location for dumps

with open('/root/sunil/sync_database', 'r') as file:
    tables = [line.strip() for line in file if line.strip()]

print(tables)

def drop_table_if_exists(connection_string, table_name):

    connection = psycopg2.connect(connection_string)

    with connection.cursor() as cursor:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        connection.commit()

def run_command(command):
    """Run a shell command."""
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        exit(1)

def dump_table(table):
    """Dump a single table from the source database."""
    dump_file = f"{backup_dir}/{table}.sql"

    os.remove(dump_file) if os.path.exists(dump_file) else None

    command = (
        f"PGPASSWORD={source_db['password']} pg_dump -h {source_db['host']} -p {source_db['port']} -U {source_db['user']} "
        f"-d {source_db['database']} -t '\"{table}\"' > {dump_file}"
    )
    run_command(command)
    return dump_file

def restore_table(dump_file, table):
    """Restore a single table to the target database."""
    command = (
        f"PGPASSWORD={target_db['password']} psql -h {target_db['host']} -p {target_db['port']} -U {target_db['user']} "
        f"-d {target_db['database']} -f {dump_file}"
    )
    run_command(command)

def sync_tables():
    """Sync tables from source to target database."""
    for table in tables:
        print(f"Syncing table: {table}")
        dump_file = dump_table(table)

        connection_string = f"postgresql://{target_db['user']}:{target_db['password']}@{target_db['host']}:{target_db['port']}/{target_db['database']}"
        drop_table_if_exists(connection_string, table)

        restore_table(dump_file, table)

if __name__ == "__main__":
    print(f"Starting sync at {datetime.datetime.now()}")
    sync_tables()
    print(f"Sync completed at {datetime.datetime.now()}")
