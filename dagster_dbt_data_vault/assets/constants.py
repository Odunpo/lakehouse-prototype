from pathlib import Path

DBT_DIRECTORY = Path(__file__).joinpath(
    "..", "..", "..", "dbt_project"
).resolve()
