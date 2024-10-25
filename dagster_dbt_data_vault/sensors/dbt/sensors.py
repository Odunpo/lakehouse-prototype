import os
from typing import List, Optional

import yaml
from dagster import (
    AssetKey,
    asset_sensor,
    SensorDefinition,
    SensorEvaluationContext,
    EventLogEntry,
    RunRequest,
)
from pydantic import BaseModel


class SensorConfig(BaseModel):
    name: str
    job: str
    prefix: Optional[str]
    upstream_asset: str


def load_sensor_configs(path: str) -> List[SensorConfig]:
    with open(path) as f:
        configs = yaml.safe_load(f)["sensors"]

    return [
        SensorConfig(
            name=c["name"],
            job=c["job"],
            prefix=c.get("prefix"),
            upstream_asset=c["upstream_asset"],
        )
        for c in configs
    ]


def create_dbt_sensor(config: SensorConfig) -> SensorDefinition:
    if config.prefix is not None:
        asset_key = [config.prefix, config.upstream_asset]
    else:
        asset_key = [config.upstream_asset]

    @asset_sensor(
        name=config.name,
        job_name=config.job,
        asset_key=AssetKey(asset_key),
    )
    def _sensor(
            context: SensorEvaluationContext,
            asset_event: EventLogEntry,
    ):
        assert (
            asset_event.dagster_event and asset_event.dagster_event.asset_key
        )
        yield RunRequest(run_key=context.cursor)

    return _sensor


script_dir = os.path.dirname(__file__)
config_path = os.path.join(script_dir, "config.yml")
sensor_configs = load_sensor_configs(config_path)
dbt_sensors = [create_dbt_sensor(c) for c in sensor_configs]
