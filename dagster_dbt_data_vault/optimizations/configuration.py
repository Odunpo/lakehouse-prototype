import os
from typing import List

import yaml
from pydantic import BaseModel


class BaseTablesJobConfig(BaseModel):
    name: str
    tables: List[str]


class DropExtendedStatsJobConfig(BaseTablesJobConfig):
    ...


class DataCompactionJobConfig(BaseTablesJobConfig):
    file_size_mb: int


class BaseRetentionJobConfig(BaseTablesJobConfig):
    retention_days: int


class ExpireSnapshotsJobConfig(BaseRetentionJobConfig):
    ...


class RemoveOrphanFilesJobConfig(BaseRetentionJobConfig):
    ...


class ScheduleConfig(BaseModel):
    job_name: str
    schedule: str


def read_config_file(config_file_path: str) -> dict:
    with open(config_file_path) as f:
        return yaml.safe_load(f)


def create_data_compaction_job_configs(
        raw_config: List[dict]
) -> List[DataCompactionJobConfig]:
    return [
        DataCompactionJobConfig(
            name=r["name"],
            file_size_mb=r.get("file_size_mb") or 128,
            tables=r["tables"],
        ) for r in raw_config
    ]


def create_expire_snapshots_job_configs(
        raw_config: List[dict]
) -> List[ExpireSnapshotsJobConfig]:
    return [
        ExpireSnapshotsJobConfig(
            name=r["name"],
            retention_days=r.get("retention_days") or 7,
            tables=r["tables"],
        ) for r in raw_config
    ]


def create_remove_orphan_files_job_configs(
        raw_config: List[dict]
) -> List[RemoveOrphanFilesJobConfig]:
    return [
        RemoveOrphanFilesJobConfig(
            name=r["name"],
            retention_days=r.get("retention_days") or 7,
            tables=r["tables"],
        ) for r in raw_config
    ]


def create_drop_extended_stats_job_configs(
        raw_config: List[dict]
) -> List[BaseTablesJobConfig]:
    return [
        BaseTablesJobConfig(
            name=r["name"],
            tables=r["tables"],
        ) for r in raw_config
    ]


def create_schedule_configs(raw_config: dict) -> List[ScheduleConfig]:
    schedules = []
    for jobs in raw_config.values():
        for job in jobs:
            schedules.append(
                ScheduleConfig(job_name=job["name"], schedule=job["schedule"])
            )
    return schedules


script_dir = os.path.dirname(__file__)
config_path = os.path.join(script_dir, "config.yml")
raw_config = read_config_file(config_path)

data_compaction_job_configs = create_data_compaction_job_configs(
    raw_config["data_compaction_jobs"]
)
expire_snapshots_job_configs = create_expire_snapshots_job_configs(
    raw_config["expire_snapshots_jobs"]
)
remove_orphan_files_job_configs = create_remove_orphan_files_job_configs(
    raw_config["remove_orphan_files_jobs"]
)
drop_extended_stats_job_configs = create_drop_extended_stats_job_configs(
    raw_config["drop_extended_stats_jobs"]
)
schedule_configs = create_schedule_configs(raw_config)
