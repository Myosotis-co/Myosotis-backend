
#!/bin/bash

# Clone the git repository using the provided git token
rm -rf /docker-entrypoint-initdb.d/db/backup/
mkdir docker-entrypoint-initdb.d/db/backup/
GIT_TOKEN=`cat /docker-entrypoint-initdb.d/db/git.token`
git clone https://$GIT_TOKEN@$GIT_REPO /docker-entrypoint-initdb.d/db/backup/
if [ $? -ne 0 ]; then
    echo "Error: Failed to clone the git repository"
    exit 1
fi

# Restore the backup using pg_restore
BACKUP_FILE=$(find /docker-entrypoint-initdb.d/db/backup -name '*.backup'| head -1)
echo "Backup file: $BACKUP_FILE"
if [ ! -z $BACKUP_FILE ] && [ -e $BACKUP_FILE ]; then 
    echo "[!>] Restoring database from cloned .backup file"
    pg_restore -U postgres -d postgres $BACKUP_FILE
    rm -rf /docker-entrypoint-initdb.d/db/backup/

fi

if [ $? -ne 0 ]; then
    echo "Error: Failed to restore the backup"
    exit 1
fi
