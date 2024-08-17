from dagster import define_asset_job, AssetSelection, JobDefinition

from dagster_dbt_data_vault.assets import asset_configs
from dagster_dbt_data_vault.assets.raw_data.asset_configuration import (
    AssetConfiguration
)


def raw_data_jobs_factory(config: AssetConfiguration) -> JobDefinition:
    return define_asset_job(
        name=config.job_name,
        selection=AssetSelection.assets(config.name),
    )


raw_data_jobs = [raw_data_jobs_factory(c) for c in asset_configs]
