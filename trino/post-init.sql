CREATE SCHEMA iceberg.raw_data WITH (location = 's3://warehouse/raw_data');
CREATE SCHEMA iceberg.parsed_data WITH (location = 's3://warehouse/parsed_data');
CREATE SCHEMA iceberg.data_vault WITH (location = 's3://warehouse/data_vault');