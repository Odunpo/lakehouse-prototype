import os

import dagster_dbt_data_vault.common.configuration as conf
from .jobs_factory import create_jobs

script_dir = os.path.dirname(__file__)
config_path = os.path.join(script_dir, "../config.yml")
configuration = conf.load_configuration_file(config_path)

asset_configs = conf.create_asset_configurations(configuration)
job_configs = conf.create_job_configurations(asset_configs)
jobs = create_jobs(job_configs)
