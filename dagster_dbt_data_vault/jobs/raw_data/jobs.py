from dagster import define_asset_job, AssetSelection, JobDefinition

from dagster_dbt_data_vault.assets import raw_data_assets_configs
from dagster_dbt_data_vault.assets.raw_data.asset_configuration import (
    JobConfiguration
)


def create_raw_data_job(config: JobConfiguration) -> JobDefinition:
    return define_asset_job(
        name=config.name,
        selection=AssetSelection.assets(config.asset_name),
    )


raw_data_jobs = [
    create_raw_data_job(c.job_config)
    for c in raw_data_assets_configs
]
