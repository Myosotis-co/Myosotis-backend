
#!/bin/bash

# Clone the git repository using the provided git token
rm -rf /docker-entrypoint-initdb.d/db/backup/
cd docker-entrypoint-initdb.d/db/
mkdir backup/
git clone https://$GIT_TOKEN@$GIT_REPO  /docker-entrypoint-initdb.d/db/backup/
if [ $? -ne 0 ]; then
    echo "Error: Failed to clone the git repository"
    exit 1
fi

# Restore the backup using pg_restore
BACKUP_FILE=$(find /docker-entrypoint-initdb.d/db/backup -name '*.backup'| head -1)
echo "Backup file: $BACKUP_FILE"
if [ ! -z $BACKUP_FILE ] && [ -e $BACKUP_FILE ]; then 
   /usr/bin/pg_restore -U postgres -d postgres $BACKUP_FILE

fi

if [ $? -ne 0 ]; then
    echo "Error: Failed to restore the backup"
    exit 1
fi

# Cleanup - remove the cloned repository
rm -rf /docker-entrypoint-initdb.d/db/backup/

exit 0