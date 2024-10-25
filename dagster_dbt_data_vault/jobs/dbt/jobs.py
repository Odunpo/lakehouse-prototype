import os
from typing import List

import yaml
from dagster import define_asset_job, AssetSelection, JobDefinition


def create_dbt_jobs(path: str) -> List[JobDefinition]:
    with open(path) as f:
        config = yaml.safe_load(f)

    # jobs = [
    #     define_asset_job(
    #         name=job_config["name"],
    #         selection=AssetSelection.assets(
    #             f"{job_config["schema"]} / {job_config["assets"]}"
    #
    #         )
    #     )
    #     for job_config in config
    # ]
    jobs = []
    for job_conf in config:
        selection = [
            f"{job_conf["schema"]}/{asset}" for asset in job_conf["assets"]
        ]
        jobs.append(
            define_asset_job(
                name=job_conf["name"],
                selection=selection,
            )
        )

    return jobs


script_dir = os.path.dirname(__file__)
config_path = os.path.join(script_dir, "config.yml")
dbt_jobs = create_dbt_jobs(config_path)
