from pathlib import Path

from dagster_dbt import DbtCliResource


DBT_DIRECTORY = Path(__file__).joinpath(
    "..", "..", "..", "dbt_project"
).resolve()


dbt_resource = DbtCliResource(project_dir=str(DBT_DIRECTORY))
