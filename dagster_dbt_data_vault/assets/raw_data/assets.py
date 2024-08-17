import os

from dagster import graph_asset, AssetsDefinition

import dagster_dbt_data_vault.ops as op
from .asset_configuration import (
    AssetConfiguration,
    load_asset_configs_from_yaml,
)


def raw_data_asset_factory(config: AssetConfiguration) -> AssetsDefinition:
    @graph_asset(
        name=config.name,
        group_name=config.group_name,
        description=config.description,
        config={
            "retrieve_offsets_from_kafka": {
                "config": {
                    "topic": config.kafka_configuration.topic,
                }
            },
            "retrieve_offsets_from_db": {
                "config": {
                    "topic": config.kafka_configuration.topic,
                    "database": config.destination_configuration.database,
                    "table": config.offsets_table,
                }
            },
            "process_kafka_messages": {
                "config": {
                    "topic": config.kafka_configuration.topic,
                }
            },
            "load_kafka_messages": {
                "config": {
                    "database": config.destination_configuration.database,
                    "table": config.destination_configuration.table,
                }
            },
            "save_offsets": {
                "config": {
                    "topic": config.kafka_configuration.topic,
                    "database": config.destination_configuration.database,
                    "table": config.offsets_table,
                }
            },
        }
    )
    def _asset():
        kafka_offsets = op.retrieve_offsets_from_kafka()
        db_offsets = op.retrieve_offsets_from_db()
        offsets = op.define_offsets(kafka_offsets, db_offsets)
        messages = op.extract_kafka_messages(offsets)
        proc_messages = op.process_kafka_messages(messages)
        new_offsets, num_messages = op.load_kafka_messages(proc_messages)
        return op.save_offsets(new_offsets, num_messages)

    return _asset


script_dir = os.path.dirname(__file__)
config_path = os.path.join(script_dir, "config.yml")
asset_configs = load_asset_configs_from_yaml(config_path)

raw_data_assets = [raw_data_asset_factory(c) for c in asset_configs]
