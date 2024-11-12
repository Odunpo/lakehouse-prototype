# Project paths and variables
DBT_PROJECT_PATH := dbt_project
VENV_PATH := venv
MINIO_URL := http://localhost:9001
FLINK_DASHBOARD := http://localhost:8081
METABASE_URL := http://localhost:3001
DAGSTER_UI := http://localhost:3000

# Environment Setup
.PHONY: init
init:
	python3 -m venv $(VENV_PATH)
	$(VENV_PATH)/bin/pip install -e ".[dev]"
	@echo "Environment setup complete. Activate with 'source $(VENV_PATH)/bin/activate'"

# Start services using Docker Compose
.PHONY: up
up:
	docker compose up -d
	@echo "All services started. Access Minio at $(MINIO_URL), Flink Dashboard at $(FLINK_DASHBOARD), Metabase at $(METABASE_URL), and Dagster at $(DAGSTER_UI)"

# Stop and remove all services
.PHONY: down
down:
	docker compose down
	@echo "All services stopped."

# Setup Debezium connector
.PHONY: setup-connector
setup-connector:
	./run_bank_connector.sh
	@echo "Debezium connector setup complete."

# Insert sample data into PostgreSQL
.PHONY: insert-sample-data
insert-sample-data:
	./run_psql_sql.sh
	@echo "Sample data inserted into PostgreSQL."

# Setup Flink for data replication
.PHONY: setup-flink
setup-flink:
	./run_flink_sql.sh
	@echo "Flink data replication setup complete. Monitor the Flink Dashboard at $(FLINK_DASHBOARD)"

# Install dbt dependencies
.PHONY: dbt-deps
dbt-deps:
	cd $(DBT_PROJECT_PATH) && dbt deps
	@echo "DBT dependencies installed."

# Run Dagster Dev server
.PHONY: dagster-dev
dagster-dev:
	@echo "Starting Dagster UI server..."
	dagster dev


.PHONY: all
all: init up setup-connector insert-sample-data setup-flink
	@echo "All components set up and running!"