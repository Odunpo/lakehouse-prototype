from .jobs.jobs import (
    compaction_jobs,
    expire_snapshots_jobs,
    orphan_files_jobs,
    extended_stats_jobs,
)
from .schedules.schedules import optimization_schedules as schedules

jobs = [
    *compaction_jobs,
    *expire_snapshots_jobs,
    *orphan_files_jobs,
    *extended_stats_jobs
]


__all__ = ("jobs", "schedules")
