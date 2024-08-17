from dagster import Definitions

import dagster_dbt_data_vault.assets as assets
import dagster_dbt_data_vault.jobs as jobs
import dagster_dbt_data_vault.schedules as schedules
import dagster_dbt_data_vault.resources as resources
import dagster_dbt_data_vault.sensors as sensors


defs = Definitions(
    assets=[*assets.raw_data_assets, assets.dbt_bank],
    jobs=[*jobs.raw_data_jobs, *jobs.parsed_data_jobs],
    schedules=[*schedules.raw_data_schedules],
    sensors=[sensors.raw_bank_users_sensor],
    resources={
        "kafka": resources.kafka_resource,
        "db": resources.duckdb_resource,
        "dbt": resources.dbt_resource,
        "iceberg_catalog": resources.iceberg_catalog_resource,
    },
)
