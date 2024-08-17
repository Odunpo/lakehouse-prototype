from dagster import (
    AssetKey,
    EventLogEntry,
    SensorEvaluationContext,
    asset_sensor,
    RunRequest,
)

from ..jobs import parsed_data_jobs


@asset_sensor(
    asset_key=AssetKey("raw_bank_users"),
    job=parsed_data_jobs[0]
)
def raw_bank_users_sensor(
        context: SensorEvaluationContext,
        asset_event: EventLogEntry
):
    assert asset_event.dagster_event and asset_event.dagster_event.asset_key
    yield RunRequest(run_key=context.cursor)
