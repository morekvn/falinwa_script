#!/bin/bash

#define variable
USER="postgres"
DUMPALL="/usr/bin/pg_dumpall"
PGDUMP="/usr/bin/pg_dump"
PSQL="/usr/bin/psql"
PORT="5432"

#Create Directory Backup
BAK_DIR="/opt/backup"
YMD=$(date "+%Y%m%d_%H%M%S")
DIR="$BAK_DIR/OE_$YMD"
mkdir -p $DIR
cd $DIR

# read all database except template
DBS=$($PSQL -l -p $PORT -U $USER -W --no-password | awk '{print $1}' | grep -vE '^-|^List|^Name|template[0|1]' | grep -v '|' | grep -v "(")
for database in $DBS; do
    $PGDUMP $database -p $PORT -U $USER -W --no-password| gzip > $DIR/$database.sql.gz
done

#----------------------------------------------------------------------------


#delete file more than 30 days old
find $BAK_DIR/OE* -mtime +30 -delete
