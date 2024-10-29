from typing import List

from dagster import (
    AssetKey,
    asset_sensor,
    SensorDefinition,
    SensorEvaluationContext,
    EventLogEntry,
    RunRequest,
)

from dagster_dbt_data_vault.common.configuration import SensorConfiguration


def create_sensors(
        configs: List[SensorConfiguration]
) -> List[SensorDefinition]:
    sensors = []

    for sensor_conf in configs:
        @asset_sensor(
            name=sensor_conf.name,
            job_name=sensor_conf.job.name,
            asset_key=AssetKey([
                sensor_conf.job.asset.upstream.prefix,
                sensor_conf.job.asset.upstream.name
            ]),
        )
        def _sensor(
                context: SensorEvaluationContext,
                asset_event: EventLogEntry,
        ):
            assert (
                asset_event.dagster_event
                and asset_event.dagster_event.asset_key
            )
            yield RunRequest(run_key=context.cursor)

        sensors.append(_sensor)

    return sensors
