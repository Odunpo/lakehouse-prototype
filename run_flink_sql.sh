#!/bin/bash

sql_commands="
-- Kafka extraction

CREATE CATALOG kafka_extraction
WITH ('type'='generic_in_memory');
USE CATALOG kafka_extraction;

CREATE DATABASE bank;

CREATE TABLE kafka_extraction.bank.users (
  payload STRING
) WITH (
  'connector'='kafka',
  'topic'='bank.public.users',
  'properties.group.id'='usersRawGroup',
  'scan.startup.mode'='earliest-offset',
  'properties.bootstrap.servers'='kafka:29092',
  'value.format'='json'
);

CREATE TABLE kafka_extraction.bank.accounts (
  payload STRING
) WITH (
  'connector'='kafka',
  'topic'='bank.public.accounts',
  'properties.group.id'='accountsRawGroup',
  'scan.startup.mode'='earliest-offset',
  'properties.bootstrap.servers'='kafka:29092',
  'value.format'='json'
);


-- Iceberg loading

CREATE CATALOG iceberg
WITH (
    'type'='iceberg',
    'catalog-type'='rest',
    'uri'='http://rest:8181',
    'io-impl'='org.apache.iceberg.aws.s3.S3FileIO',
    'warehouse'='s3://warehouse',
    's3.endpoint'='http://minio:9000',
    's3.path-style-access'='true'
);
USE CATALOG iceberg;

CREATE DATABASE IF NOT EXISTS raw_data;

CREATE TABLE iceberg.raw_data.users (
    data STRING,
    op STRING,
    ts_ms BIGINT,
    source_ts_ms BIGINT,
    source_tx_id INT,
    source_lsn INT,
    source_connector STRING,
    source_db STRING,
    source_schema STRING,
    source_table STRING
);

CREATE TABLE iceberg.raw_data.accounts (
    data STRING,
    op STRING,
    ts_ms BIGINT,
    source_ts_ms BIGINT,
    source_tx_id INT,
    source_lsn INT,
    source_connector STRING,
    source_db STRING,
    source_schema STRING,
    source_table STRING
);


-- Insert data from kafka to iceberg

INSERT INTO iceberg.raw_data.users (
    data,
    op,
    ts_ms,
    source_ts_ms,
    source_tx_id,
    source_lsn,
    source_connector,
    source_db,
    source_schema,
    source_table
)
SELECT
    CASE
        WHEN JSON_VALUE(payload, '$.op') = 'd'
            THEN JSON_QUERY(payload, '$.before')
        ELSE JSON_QUERY(payload, '$.after')
    END AS data,
    JSON_VALUE(payload, '$.op') AS op,
    CAST(JSON_VALUE(payload, '$.ts_ms') AS BIGINT) AS ts_ms,
    CAST(JSON_VALUE(payload, '$.source.ts_ms') AS BIGINT) AS source_ts_ms,
    CAST(JSON_VALUE(payload, '$.source.txId') AS INT) AS source_tx_id,
    CAST(JSON_VALUE(payload, '$.source.lsn') AS INT) AS source_lsn,
    JSON_VALUE(payload, '$.source.connector') AS source_connector,
    JSON_VALUE(payload, '$.source.db') AS source_db,
    JSON_VALUE(payload, '$.source.schema') AS source_schema,
    JSON_VALUE(payload, '$.source.table') AS source_table
FROM kafka_extraction.bank.users;

INSERT INTO iceberg.raw_data.accounts (
    data,
    op,
    ts_ms,
    source_ts_ms,
    source_tx_id,
    source_lsn,
    source_connector,
    source_db,
    source_schema,
    source_table
)
SELECT
    CASE
        WHEN JSON_VALUE(payload, '$.op') = 'd'
            THEN JSON_QUERY(payload, '$.before')
        ELSE JSON_QUERY(payload, '$.after')
    END AS data,
    JSON_VALUE(payload, '$.op') AS op,
    CAST(JSON_VALUE(payload, '$.ts_ms') AS BIGINT) AS ts_ms,
    CAST(JSON_VALUE(payload, '$.source.ts_ms') AS BIGINT) AS source_ts_ms,
    CAST(JSON_VALUE(payload, '$.source.txId') AS INT) AS source_tx_id,
    CAST(JSON_VALUE(payload, '$.source.lsn') AS INT) AS source_lsn,
    JSON_VALUE(payload, '$.source.connector') AS source_connector,
    JSON_VALUE(payload, '$.source.db') AS source_db,
    JSON_VALUE(payload, '$.source.schema') AS source_schema,
    JSON_VALUE(payload, '$.source.table') AS source_table
FROM kafka_extraction.bank.accounts;
"

echo "$sql_commands" | docker exec -i flink-sql-client sql-client -