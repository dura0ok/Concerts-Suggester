#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER "$PROJECT_USER_NAME" WITH PASSWORD '$PROJECT_USER_PASSWORD';
    CREATE DATABASE "$PROJECT_USER_DATABASE_NAME";
    GRANT ALL PRIVILEGES ON DATABASE "$PROJECT_USER_DATABASE_NAME" TO "$PROJECT_USER_NAME";
EOSQL