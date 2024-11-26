#!/bin/bash

SOURCE_DB="cno_prod"
DEST_DB="TPGA01"
SOURCE_HOST="10.133.132.90"
DEST_HOST="localhost"
SOURCE_USER="postgres"
DEST_USER="tpgteam"
TABLES=("nokia_5g_layer_wise_data" "kpi_table_nsa" "kpi_table_sa_access_sr" "kpi_table_sgnb_t_abn_rel" "kpi_table_sa_qos_flow_drop" 
"anomaly_alarm_cell_count_5g" "anomaly_alarm_summary_5g" "tpg_kpi_failure_data")


EXPORT_DIR="/tmp"
IMPORT_DIR="/tmp"

# Export tables from source database
for table in "${TABLES[@]}"; do
    echo "Exporting $table from source database..."
    psql -h $SOURCE_HOST -U $SOURCE_USER -d $SOURCE_DB -c "\COPY $table TO '$EXPORT_DIR/$table.csv' WITH (FORMAT csv, HEADER true);"
    
    # Transfer CSV file to destination server
    # echo "Transferring $table.csv to destination server..."
    # scp "$EXPORT_DIR/$table.csv" $DEST_USER@$DEST_HOST:$IMPORT_DIR/
done

# Import tables into destination database
for table in "${TABLES[@]}"; do
    echo "Importing $table.csv into destination database..."
    psql -U $DEST_USER -d $DEST_DB -c "\COPY $table FROM '$IMPORT_DIR/$table.csv' WITH (FORMAT csv, HEADER true);"
done

echo "Data synchronization completed."
