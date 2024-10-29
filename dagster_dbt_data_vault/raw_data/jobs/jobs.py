import dagster_dbt_data_vault.common.configuration as conf
from .jobs_factory import create_jobs
from ..assets import asset_configs


job_configs = conf.create_job_configurations(asset_configs)
jobs = create_jobs(job_configs)
