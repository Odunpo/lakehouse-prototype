from dagster import Definitions

import dagster_dbt_data_vault.raw_data as raw
import dagster_dbt_data_vault.dbt as dbt
import dagster_dbt_data_vault.resources as resources
import dagster_dbt_data_vault.optimizations as optimizations


defs = Definitions(
    assets=[*raw.assets, *dbt.assets],
    jobs=[*raw.jobs, *dbt.jobs, *optimizations.jobs],
    sensors=[*raw.sensors, *dbt.sensors],
    schedules=[*optimizations.schedules],
    resources={
        "dbt": resources.dbt_resource,
        "trino": resources.trino_resource,
        "s3": resources.s3_resource,
    }
)
