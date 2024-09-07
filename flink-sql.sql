CREATE TABLE users (
    origin_ts TIMESTAMP(3) METADATA FROM 'value.ingestion-timestamp' VIRTUAL,
    event_time TIMESTAMP(3) METADATA FROM 'value.source.timestamp' VIRTUAL,
    origin_database STRING METADATA FROM 'value.source.database' VIRTUAL,
    origin_schema STRING METADATA FROM 'value.source.schema' VIRTUAL,
    origin_table STRING METADATA FROM 'value.source.table' VIRTUAL,
    origin_properties MAP<STRING, STRING> METADATA FROM 'value.source.properties' VIRTUAL,
    id STRING,
    email STRING,
    name STRING,
    created_at STRING
) WITH (
    'connector' = 'kafka',
    'topic' = 'bank.public.users',
    'properties.bootstrap.servers' = 'kafka:29092',
    'properties.group.id' = 'usersGroup',
    'format' = 'debezium-json',
    'debezium-json.schema-include' = 'true',
    'scan.startup.mode' = 'earliest-offset'
);


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


SET execution.checkpointing.interval = '1m';
