from typing import List

from dagster import ScheduleDefinition

import dagster_dbt_data_vault.optimizations.configuration as conf


def create_optimization_schedules(
        schedule_configs: List[conf.ScheduleConfig]
) -> List[ScheduleDefinition]:
    return [
        ScheduleDefinition(
            name=c.job_name.replace("_job", "_schedule"),
            job_name=c.job_name,
            cron_schedule=c.schedule,
        ) for c in schedule_configs
    ]


optimization_schedules = create_optimization_schedules(conf.schedule_configs)
