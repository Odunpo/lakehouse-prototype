from dagster import SensorDefinition, sensor, RunRequest, RunConfig

from dagster_dbt_data_vault.assets.raw_data.asset_configuration import (
    SensorConfiguration,
    raw_data_assets_configs,
)
from dagster_dbt_data_vault.assets.raw_data.assets import LastLsnConfig
from dagster_dbt_data_vault.resources.raw_data.trino import TrinoResource


def create_raw_data_sensor(config: SensorConfiguration) -> SensorDefinition:
    @sensor(
        name=config.name,
        job_name=config.job_name
    )
    def _sensor(context, trino: TrinoResource):
        last_lsn = int(context.cursor) if context.cursor else 0

        with trino.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                f"SELECT max(source_lsn) FROM {config.asset_table_name}"
            )
            res = cur.fetchone()

        current_lsn = res[0] if res else 0

        if current_lsn > last_lsn:
            yield RunRequest(
                run_key=context.cursor,
                run_config=RunConfig(
                    {config.asset_name: LastLsnConfig(last_lsn=last_lsn)}
                )
            )

        str_current_lsn = str(current_lsn)
        context.update_cursor(str_current_lsn)

    return _sensor


raw_data_sensors = [
    create_raw_data_sensor(c.sensor_config)
    for c in raw_data_assets_configs
]
