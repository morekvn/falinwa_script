#!/bin/bash

YMD=$(date "+%Y%m%d_%H%M%S")
IP_address="TYPE_THE_IP_ADDRESS_OF_FTP_SERVER"
username="TYPE_FTP_USER"
password="TYPE_FTP_USER_PASSWORD"

cd location/to/odoo/filestore

tar -zcvf BACKUP_$YMD.tar.gz ODOO_DATABASE_NAME/

ftp -n <<EOF
 verbose
 open $IP_address
 user $username $password
 put BACKUP_$YMD.tar.gz
 bye
EOF

rm BACKUP_$YMD.tar.gz
echo "Sent with love to Backup Server"
