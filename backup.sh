#!/bin/bash

BACKUP_DIR="/path/to/backup/directory"
DJANGO_PROJECT_DIR="/path/to/django/project"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="django_app_backup_$TIMESTAMP.tar.gz"

mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_DIR/$BACKUP_NAME" -C "$DJANGO_PROJECT_DIR" .

cd "$BACKUP_DIR" || exit
ls -tp | grep -v '/$' | tail -n +4 | xargs -I {} rm -- {}
