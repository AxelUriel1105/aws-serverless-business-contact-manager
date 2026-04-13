#!/bin/bash
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
CSV_PATH="$SCRIPT_DIR/../csv_files/million_rows.csv"
time aws s3 cp "$CSV_PATH" s3://phone-book-csv-axel-aparicio/million_rows.csv