from typing import List

from dagster import op, Config, OpExecutionContext
from dagster_aws.s3 import S3Resource

from dagster_dbt_data_vault.resources.trino import TrinoResource
from ..optimizers import TrinoOptimizer, S3Optimizer


class TablesConfig(Config):
    tables: List[str]


class CompactConfig(TablesConfig):
    file_size_mb: int


class RetentionConfig(TablesConfig):
    retention_days: int


class S3Config(Config):
    bucket: str
    prefixes: List[str]
    retention_hours: int


@op
def compact_data_op(
        context: OpExecutionContext,
        trino: TrinoResource,
        config: CompactConfig,
) -> None:
    file_size_mb = config.file_size_mb
    for table in config.tables:
        with trino.get_connection() as conn:
            trino_optimizer = TrinoOptimizer(conn, table)
            trino_optimizer.compact_data(file_size_mb)
            context.log.info(f"Compacted {table}, file size: {file_size_mb}.")


@op
def expire_snapshots_op(
        context: OpExecutionContext,
        trino: TrinoResource,
        config: RetentionConfig,
) -> None:
    retention = config.retention_days
    for table in config.tables:
        with trino.get_connection() as conn:
            trino_optimizer = TrinoOptimizer(conn, table)
            trino_optimizer.expire_snapshots(retention)
            context.log.info(f"Expired {table}, retention: {retention} days.")


@op
def remove_orphan_files_op(
        context: OpExecutionContext,
        trino: TrinoResource,
        config: RetentionConfig,
) -> None:
    retention = config.retention_days
    for table in config.tables:
        with trino.get_connection() as conn:
            trino_optimizer = TrinoOptimizer(conn, table)
            trino_optimizer.remove_orphan_files(retention)
            context.log.info(f"""
                Removed orphan files for {table}, retention: {retention} days.
            """)


@op
def drop_extended_stats_op(
        context: OpExecutionContext,
        trino: TrinoResource,
        config: TablesConfig,
) -> None:
    for table in config.tables:
        with trino.get_connection() as conn:
            trino_optimizer = TrinoOptimizer(conn, table)
            trino_optimizer.drop_extended_stats()
            context.log.info(f"Dropped extended stats for {table}.")


@op
def clean_dbt_tmp_objects_op(
        context: OpExecutionContext,
        s3: S3Resource,
        config: S3Config,
) -> None:
    s3_optimizer = S3Optimizer(
        s3=s3,
        bucket=config.bucket,
        prefixes=config.prefixes,
        retention_hours=config.retention_hours,
    )

    context.log.info(f"""
        Deleting objects with retention hours: {config.retention_hours}
        for prefixes: {config.prefixes}
    """)
    deleted_objects = s3_optimizer.delete_stale_dbt_tmp_objects()
    context.log.info(f"Deleted {len(deleted_objects)} dbt tmp objects")
