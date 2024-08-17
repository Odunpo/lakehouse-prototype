from typing import List

import yaml
from pydantic import BaseModel


class KafkaConfiguration(BaseModel):
    topic: str


class DestinationConfiguration(BaseModel):
    database: str
    table: str


class AssetConfiguration(BaseModel):
    name: str
    group_name: str
    offsets_table: str
    description: str
    kafka_configuration: KafkaConfiguration
    destination_configuration: DestinationConfiguration
    schedule: str
    job_name: str
    schedule_name: str


def load_asset_configs_from_yaml(config_path: str) -> List[AssetConfiguration]:
    with open(config_path) as f:
        config = yaml.safe_load(f)

    asset_configs = []
    for asset in config["assets"]:
        global_group_name = config["global"]["group_name"]
        global_offsets_table = config["global"]["offsets_table"]
        asset_configs.append(
            AssetConfiguration(
                name=asset["name"],
                group_name=asset.get("group_name") or global_group_name,
                offsets_table=global_offsets_table,
                description=asset["description"],
                kafka_configuration=KafkaConfiguration(
                    topic=asset["kafka"]["topic"],
                ),
                destination_configuration=DestinationConfiguration(
                    database=asset["destination"]["database"],
                    table=asset["destination"]["table"],
                ),
                schedule=asset["schedule"],
                job_name=asset.get("job_name") or asset["name"] + "_job",
                schedule_name=(
                    asset.get("schedule_name")
                    or asset["name"] + "_schedule"
                )
            )
        )

    return asset_configs
