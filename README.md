# Data Lakehouse End to End prototype

This is an end-to-end Data Lakehouse prototype built to manage real-time data ingestion, storage, and transformation for historical and incremental data tracking. Starting with PostgreSQL as the data source, Change Data Capture (CDC) events are captured by Debezium and streamed into Kafka. Flink processes and loads these events into Iceberg tables stored in Minio object storage.

Dagster orchestrates the transformations and processing within Iceberg, with dbt handling SQL transformations and Trino as the query engine. This setup supports ELT (Extract, Load, Transform) workflows and establishes a Data Vault model with historical layers, retaining all source changes for reliable data lineage and analytics.

For more information, visit the [article](https://medium.com/@oleg.1999.ustimenko/building-an-end-to-end-elt-cdc-data-lakehouse-prototype-with-iceberg-87e0b55ebd29) on Medium.

## Getting started

This guide will help you set up and run the project locally, enabling you to replicate, store, and process streaming data in a Data Vault structure.

## Architecture and Setup

![](architecture.jpg)

### 1. Start All Services with Docker Compose

To initialize the necessary components of the Data Lakehouse, run:

```bash
docker compose up -d
```

This command will start the following services:
- `postgres`: Source database to replicate data from.
- `connect`: Debezium connector for extracting CDC (Change Data Capture) data from PostgreSQL and sending it to Kafka.
- `kafka`: Temporary storage for CDC raw data.
- `flink-jobmanager`, `flink-taskmanager`, `flink-sql-client`: Services for streaming data from Kafka to Iceberg.
- `minio`: Object storage for data.
- `mc`: Initialization container for Minio.
- `rest`: Iceberg catalog REST API.
- `trino`: Data engine for processing data stored in Iceberg.

### 2. Set Up the Debezium Connector

To enable data replication from PostgreSQL to Kafka, create a Debezium connector by running:

```bash
./run_bank_connector.sh
```

### 3. Insert Sample Data into PostgreSQL

Add data to PostgreSQL by running:

```bash
./run_psql_sql.sh
```

### 4. Set Up Flink for Data Replication

To configure data replication from Kafka to Iceberg using Flink, run:

```bash
./run_flink_sql.sh
```

You can monitor job statuses and view replication details on the Flink Dashboard (http://localhost:8081).
Access Minio at http://localhost:9001 (username: admin, password: password) to view the data.

## Using Dagster

### Python packages installation

First, install your Dagster code location as a Python package. By using the --editable flag, pip will install your Python package in ["editable mode"](https://pip.pypa.io/en/latest/topics/local-project-installs/#editable-installs) so that as you develop, local code changes will automatically apply.

```bash
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### DBT dependencies installation
```bash
cd dbt_project
dbt deps
cd ..
```

### Run Dagster

Create `.env` file and add the next variables:
```
DAGSTER_DBT_PARSE_PROJECT_ON_LOAD=1
ICEBERG_S3_ENDPOINT=http://localhost:9000
ICEBERG_S3_ACCESS_KEY=admin
ICEBERG_S3_SECRET_KEY=password
TRINO_HOST=localhost
TRINO_PORT=8080
TRINO_USER=commander
TRINO_CATALOG=iceberg
TRINO_SCHEMA=raw_data
```

To start the Dagster UI web server:

```bash
dagster dev
```

Open http://localhost:3000 with your browser to see the project.

### Activating Schedules and Sensors

Activate sensors and schedules by navigating to: `Automation` -> Select all -> `Actions` -> `Start automations`

Once active, your project should be up and running! To view the lineage of all data assets, go to `Assets` -> `View global asset lineage`

## Querying Data in Trino

Final data can also be queried using Trino. To connect to Trino, use:

```bash
docker exec -it trino trino
```
And
```sql
-- Check raw data tables
USE iceberg.raw_data;
SHOW TABLES;
SELECT * FROM users;

-- Check parsed data tables
USE iceberg.parsed_data;
SHOW TABLES;
SELECT * FROM parsed_users;

-- Check data vault tables
USE iceberg.data_vault;
SHOW TABLES;
SELECT * FROM s_users;
```

## Data Analysis and Visualization with Metabase

Metabase serves as the user interface for data analysis and visualization in this Data Lakehouse prototype.
It connects directly to Trino, allowing you to explore data in Iceberg and build interactive dashboards and reports.
The container has an additional Starburst plugin to be able to connect to Trino engine.

To access Metabase, open http://localhost:3001 in your browser.
To connect Metabase to Trino, use Starburst database connection (host: `trino`, port: `8080`, catalog: `iceberg`, username: `commander`)