# How to set up daily backup
1. Copy backup_openerp_dbs.sh to server
2. Make it executable using this command: sudo chmod +x /path/to/backup_openerp_dbs.sh
3. Login as user postgres by executing command: sudo su - postgres
4. Edit crontab using command: crontab -e
5. Copy entire text on crontab.txt file and paste it to server's crobtab
6. Don't forget to save crontab and congratulations.