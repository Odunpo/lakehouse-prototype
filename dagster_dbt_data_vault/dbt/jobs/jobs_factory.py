from typing import List

from dagster import define_asset_job, JobDefinition, AssetKey

from dagster_dbt_data_vault.common.configuration import JobConfiguration


def create_jobs(config: List[JobConfiguration]) -> List[JobDefinition]:
    jobs = []

    for job_conf in config:
        job = define_asset_job(
            name=job_conf.name,
            selection=[AssetKey([job_conf.asset.prefix, job_conf.asset.name])]
        )
        jobs.append(job)

    return jobs
