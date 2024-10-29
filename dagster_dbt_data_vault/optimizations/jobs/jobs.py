from typing import List

from dagster import job, JobDefinition

import dagster_dbt_data_vault.optimizations.configuration as conf
import dagster_dbt_data_vault.optimizations.ops.ops as ops


def create_compaction_jobs(
        jobs_config: List[conf.DataCompactionJobConfig]
) -> List[JobDefinition]:
    jobs = []

    for job_config in jobs_config:

        @job(
            name=job_config.name,
            config={
                "ops": {
                    "compact_data_op": {
                        "config": {
                            "tables": job_config.tables,
                            "file_size_mb": job_config.file_size_mb,
                        }
                    }
                }
            },
            tags={"optimization": True},
        )
        def _job():
            ops.compact_data_op()

        jobs.append(_job)

    return jobs


def create_expire_snapshots_jobs(
        jobs_config: List[conf.ExpireSnapshotsJobConfig]
) -> List[JobDefinition]:
    jobs = []

    for job_config in jobs_config:

        @job(
            name=job_config.name,
            config={
                "ops": {
                    "expire_snapshots_op": {
                        "config": {
                            "tables": job_config.tables,
                            "retention_days": job_config.retention_days,
                        }
                    }
                }
            },
            tags={"optimization": True},
        )
        def _job():
            ops.expire_snapshots_op()

        jobs.append(_job)

    return jobs


def create_remove_orphan_files_jobs(
        jobs_config: List[conf.RemoveOrphanFilesJobConfig]
) -> List[JobDefinition]:
    jobs = []

    for job_config in jobs_config:

        @job(
            name=job_config.name,
            config={
                "ops": {
                    "remove_orphan_files_op": {
                        "config": {
                            "tables": job_config.tables,
                            "retention_days": job_config.retention_days,
                        }
                    }
                }
            },
            tags={"optimization": True},
        )
        def _job():
            ops.remove_orphan_files_op()

        jobs.append(_job)

    return jobs


def create_drop_extended_stats_jobs(
        jobs_config: List[conf.DropExtendedStatsJobConfig]
) -> List[JobDefinition]:
    jobs = []

    for job_config in jobs_config:

        @job(
            name=job_config.name,
            config={
                "ops": {
                    "drop_extended_stats_op": {
                        "config": {
                            "tables": job_config.tables,
                        }
                    }
                }
            },
            tags={"optimization": True},
        )
        def _job():
            ops.drop_extended_stats_op()

        jobs.append(_job)

    return jobs


def create_clean_dbt_tmp_objects_jobs(
        jobs_config: List[conf.S3DbtTmpCleanJobConfig]
) -> List[JobDefinition]:
    jobs = []

    for job_config in jobs_config:

        @job(
            name=job_config.name,
            config={
                "ops": {
                    "clean_dbt_tmp_objects_op": {
                        "config": {
                            "bucket": job_config.bucket,
                            "prefixes": job_config.prefixes,
                            "retention_hours": job_config.retention_hours,
                        }
                    }
                }
            },
            tags={"optimization": True},
        )
        def _job():
            ops.clean_dbt_tmp_objects_op()

        jobs.append(_job)

    return jobs


compaction_jobs = create_compaction_jobs(conf.data_compaction_job_configs)
expire_snapshots_jobs = create_expire_snapshots_jobs(
    conf.expire_snapshots_job_configs
)
orphan_files_jobs = create_remove_orphan_files_jobs(
    conf.remove_orphan_files_job_configs
)
extended_stats_jobs = create_drop_extended_stats_jobs(
    conf.drop_extended_stats_job_configs
)
clean_dbt_tmp_objects_jobs = create_clean_dbt_tmp_objects_jobs(
    conf.s3_dbt_tmp_clean_job_configs
)
