#!/bin/bash
# Prepares environment but does not pre-load a new site with data

# Check if postgres-data directory exists
if [ ! -d "$(dirname "$0")/data/postgres-data" ]; then
    mkdir -p "$(dirname "$0")/data/postgres-data"
    echo Created "$(dirname "$0")/data/postgres-data"
fi

# Run Docker Compose with provided arguments
docker compose "$@"

