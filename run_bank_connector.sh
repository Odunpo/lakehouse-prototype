#!/bin/bash

# Create Debezium connector using cURL
curl --location 'http://localhost:8083/connectors' \
   --header 'Accept: application/json' \
   --header 'Content-Type: application/json' \
   --data '{
   "name": "bank-connector",
   "config": {
       "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
       "database.hostname": "postgres",
       "database.port": "5432",
       "database.user": "postgres",
       "database.password": "password",
       "database.dbname": "bank",
       "database.server.id": "184054",
       "table.include.list": "public.users,public.accounts",
       "topic.prefix": "bank",
       "decimal.handling.mode": "string",
       "publication.name": "bank_pub",
       "slot.name": "bank_slot",
       "plugin.name": "pgoutput"
   }
}'