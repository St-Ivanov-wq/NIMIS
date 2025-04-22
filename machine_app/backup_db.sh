#!/bin/bash
DATE=$(date +%Y-%m-%d)
pg_dump -U machine_user -h localhost -d filedata > ~/machine_app/backups/db_backup_$DATE.sql
find ~/machine_app/backups -type f -mtime +7 -delete

