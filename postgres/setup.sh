#!/bin/bash

sudo -u postgres psql -c "CREATE USER benchmark WITH PASSWORD 'benchmark';"

sudo -u postgres psql -c "CREATE DATABASE benchmark OWNER benchmark;"

sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE benchmark TO benchmark;"

echo "PostgreSQL benchmark user and database created successfully."