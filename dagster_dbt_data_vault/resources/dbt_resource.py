from dagster_dbt import DbtCliResource

from ..assets.constants import DBT_DIRECTORY

dbt_resource = DbtCliResource(project_dir=DBT_DIRECTORY)
