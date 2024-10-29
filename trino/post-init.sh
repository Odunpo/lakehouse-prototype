#!/bin/bash

nohup /usr/lib/trino/bin/run-trino &

# Wait until Trino is ready
until trino --execute "SELECT 1" > /dev/null 2>&1; do
    echo "Waiting for Trino to be ready..."
    sleep 5
done

# Run SQL script
trino < /tmp/post-init.sql

tail -f /dev/null
