-- Kafka extraction

CREATE CATALOG kafka_extraction
WITH ('type'='generic_in_memory');

CREATE DATABASE bank;

CREATE TABLE `kafka_extraction`.`bank`.`users` (
  `payload` STRING
) WITH (
  'connector' = 'kafka',
  'topic' = 'bank.public.users',
  'properties.group.id' = 'usersRawGroup',
  'scan.startup.mode' = 'earliest-offset',
  'properties.bootstrap.servers' = 'kafka:29092',
  'value.format' = 'json'
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

CREATE DATABASE bank;

CREATE TABLE `iceberg`.`bank`.`users` (
    `after` STRING,
    `op` STRING,
    `ts_ms` BIGINT,
    `source_ts_ms` BIGINT,
    `source_tx_id` INT,
    `source_lsn` INT,
    `source_db` STRING,
    `source_schema` STRING,
    `source_table` STRING
);


-- Checkpoints to commit new data every 1 minute

SET execution.checkpointing.interval = '1m';


-- Insert data from kafka to iceberg

INSERT INTO `iceberg`.`bank`.`users` (
    after,
    op,
    ts_ms,
    source_ts_ms,
    source_tx_id,
    source_lsn,
    source_db,
    source_schema,
    source_table
)
SELECT
  JSON_QUERY(payload, '$.after') AS after,
  JSON_VALUE(payload, '$.op') AS op,
  CAST(JSON_VALUE(payload, '$.ts_ms') AS BIGINT) AS ts_ms,
  CAST(JSON_VALUE(payload, '$.source.ts_ms') AS BIGINT) AS source_ts_ms,
  CAST(JSON_VALUE(payload, '$.source.txId') AS INT) AS source_tx_id,
  CAST(JSON_VALUE(payload, '$.source.lsn') AS INT) AS source_lsn,
  JSON_VALUE(payload, '$.source.db') AS source_db,
  JSON_VALUE(payload, '$.source.schema') AS source_schema,
  JSON_VALUE(payload, '$.source.table') AS source_table
FROM `kafka_extraction`.`default`.`users`;





-- Example of debezium payload from kafka:
-- {
--     "before":null,
--     "after": {
--         "id":"902b1599-1a40-429b-9caa-756f8719b1da",
--         "email":"oleg@oleg.com",
--         "name":"Oleg",
--         "created_at":19983
--     },
--     "source": {
--         "version":"2.3.4.Final",
--         "connector":"postgresql",
--         "name":"bank",
--         "ts_ms":1726587015825,
--         "snapshot":"false",
--         "db":"bank",
--         "sequence":"[null,\"25803680\"]",
--         "schema":"public",
--         "table":"users",
--         "txId":739,
--         "lsn":25803680,
--         "xmin":null
--     },
--     "op":"c",
--     "ts_ms":1726587016299,
--     "transaction":null
-- }


-- Example of debezium-json format usage (only for snapshots):
-- CREATE TABLE users (
--     origin_ts TIMESTAMP(3) METADATA FROM 'value.ingestion-timestamp' VIRTUAL,
--     event_time TIMESTAMP(3) METADATA FROM 'value.source.timestamp' VIRTUAL,
--     origin_database STRING METADATA FROM 'value.source.database' VIRTUAL,
--     origin_schema STRING METADATA FROM 'value.source.schema' VIRTUAL,
--     origin_table STRING METADATA FROM 'value.source.table' VIRTUAL,
--     origin_properties MAP<STRING, STRING> METADATA FROM 'value.source.properties' VIRTUAL,
--     id STRING,
--     email STRING,
--     name STRING,
--     created_at STRING
-- ) WITH (
--     'connector' = 'kafka',
--     'topic' = 'bank.public.users',
--     'properties.bootstrap.servers' = 'kafka:29092',
--     'properties.group.id' = 'usersGroup',
--     'format' = 'debezium-json',
--     'debezium-json.schema-include' = 'true',
--     'scan.startup.mode' = 'earliest-offset'
-- );