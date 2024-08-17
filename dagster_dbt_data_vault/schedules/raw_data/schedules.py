from dagster import ScheduleDefinition, DefaultScheduleStatus

from dagster_dbt_data_vault.assets import asset_configs
from dagster_dbt_data_vault.assets.raw_data.asset_configuration import AssetConfiguration


def raw_data_schedules_factory(
        config: AssetConfiguration
) -> ScheduleDefinition:
    return ScheduleDefinition(
        name=config.schedule_name,
        job_name=config.job_name,
        cron_schedule=config.schedule,
        # default_status=DefaultScheduleStatus.RUNNING,
    )


raw_data_schedules = [raw_data_schedules_factory(c) for c in asset_configs]
