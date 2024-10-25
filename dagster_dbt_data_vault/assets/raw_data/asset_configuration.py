import os
from typing import List

import yaml
from pydantic import BaseModel


class JobConfiguration(BaseModel):
    name: str
    asset_name: str


class SensorConfiguration(BaseModel):
    name: str
    job_name: str
    asset_name: str
    asset_table_name: str


class AssetConfiguration(BaseModel):
    name: str
    group_name: str
    description: str
    table_name: str
    job_config: JobConfiguration
    sensor_config: SensorConfiguration


def load_asset_configs_from_yaml(config_path: str) -> List[AssetConfiguration]:
    with open(config_path) as f:
        config = yaml.safe_load(f)

    group_name = config["group_name"]

    asset_configs = []
    for asset in config["assets"]:
        asset_name = asset["name"]
        asset_description = asset.get("description") or ""
        asset_table_name = asset.get("table_name") or asset_name
        job_name = asset["name"] + "_job"
        sensor_name = asset["name"] + "_sensor"

        asset_configs.append(
            AssetConfiguration(
                name=asset_name,
                group_name=group_name,
                description=asset_description,
                table_name=asset_table_name,
                job_config=JobConfiguration(
                    name=job_name,
                    asset_name=asset_name,
                ),
                sensor_config=SensorConfiguration(
                    name=sensor_name,
                    job_name=job_name,
                    asset_name=asset_name,
                    asset_table_name=asset_table_name,
                )
            )
        )

    return asset_configs


script_dir = os.path.dirname(__file__)
config_path = os.path.join(script_dir, "config.yml")
raw_data_assets_configs = load_asset_configs_from_yaml(config_path)
