from dagster import Definitions

import dagster_dbt_data_vault.assets as assets
import dagster_dbt_data_vault.jobs as jobs
import dagster_dbt_data_vault.resources as resources
import dagster_dbt_data_vault.sensors as sensors

import dagster_dbt_data_vault.optimizations as optimizations

defs = Definitions(
    assets=[assets.dbt_bank, *assets.raw_data_assets],
    jobs=[
        *jobs.dbt_jobs,
        *jobs.raw_data_jobs,
        *optimizations.jobs,
    ],
    resources={
        "dbt": resources.dbt_resource,
        "trino": resources.trino_resource,
    },
    sensors=[*sensors.dbt_sensors, *sensors.raw_data_sensors],
    schedules=[*optimizations.schedules],
)
