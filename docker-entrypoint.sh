#!/bin/bash
set -e

# Create required directories if they don't exist
mkdir -p /app/input /app/output /app/logs

# Check if we're running as the correct user
if [ "$(id -u)" = "0" ]; then
    echo "Error: Running as root is not allowed"
    exit 1
fi

# Initialize application
echo "Initializing application..."
python -c "from app.utils import check_folders; check_folders()"

# Run database migrations if they exist
if [ -f "migrations/migrate.py" ]; then
    echo "Running database migrations..."
    python migrations/migrate.py
fi

# Execute the main command
exec "$@"