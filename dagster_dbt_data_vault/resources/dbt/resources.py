from dagster_dbt import DbtCliResource

from dagster_dbt_data_vault.assets.dbt.constants import DBT_DIRECTORY

dbt_resource = DbtCliResource(project_dir=DBT_DIRECTORY)
