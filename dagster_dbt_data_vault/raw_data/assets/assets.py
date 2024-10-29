import os

import dagster_dbt_data_vault.common.configuration as conf
from .assets_factory import RawDataAssetFactory


script_dir = os.path.dirname(__file__)
config_path = os.path.join(script_dir, "../config.yml")
configuration = conf.load_configuration_file(config_path)

asset_configs = conf.create_asset_configurations(configuration)
factory = RawDataAssetFactory(asset_configs)
assets = factory.create_assets()
