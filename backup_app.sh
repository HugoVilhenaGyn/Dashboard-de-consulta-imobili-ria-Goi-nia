#!/bin/bash
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/var/www/brokerimobai/backups"
APP_DIR="/var/www/brokerimobai"

mkdir -p "$BACKUP_DIR"

FILES=(
  "app.py"
  "lisa.py"
  "templates/dashboard.html"
  "templates/historico.html"
)

BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.tar.gz"
tar -czf "$BACKUP_FILE" -C "$APP_DIR" "${FILES[@]}" 2>/dev/null

echo "Backup salvo em: $BACKUP_FILE"
ls -t "$BACKUP_DIR"/backup_*.tar.gz | tail -n +11 | xargs -r rm
echo "Backups disponíveis:"
ls -lh "$BACKUP_DIR"/backup_*.tar.gz
