from typing import List

from dagster import SensorDefinition, sensor, RunRequest, RunConfig

from dagster_dbt_data_vault.resources.trino import TrinoResource
from dagster_dbt_data_vault.common.configuration import SensorConfiguration
from ..assets import LastLsnConfig


def create_sensors(
        configs: List[SensorConfiguration]
) -> List[SensorDefinition]:
    sensors = []

    for sensor_conf in configs:
        @sensor(
            name=sensor_conf.name,
            job_name=sensor_conf.job.name,
        )
        def _sensor(context, trino: TrinoResource, conf=sensor_conf):
            last_lsn = int(context.cursor) if context.cursor else 0
            table = conf.job.asset.table
            asset_prefix = conf.job.asset.prefix
            asset_name = conf.job.asset.name
            asset_op_name = f"{asset_prefix}__{asset_name}"

            with trino.get_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    f"SELECT max(source_lsn) FROM {table}"
                )
                res = cur.fetchone()

            current_lsn = res[0] if res else 0
            context.log.info(f"Current lsn: {current_lsn}")
            context.log.info(f"Last lsn: {last_lsn}")

            if current_lsn > last_lsn:
                context.log.info(f"Submitting run request for {asset_name}")
                yield RunRequest(
                    run_key=context.cursor,
                    run_config=RunConfig(
                        {asset_op_name: LastLsnConfig(last_lsn=last_lsn)}
                    )
                )

            str_current_lsn = str(current_lsn)
            context.update_cursor(str_current_lsn)

        sensors.append(_sensor)

    return sensors
