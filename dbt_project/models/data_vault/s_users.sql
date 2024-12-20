{{ config(materialized='incremental', schema='data_vault') }}

{%- set yaml_metadata -%}

source_model: parsed_users
source_pk:
    name: id
    name_hk: users_hk
columns:
    - email
    - name
    - created_at
    - __deleted_flag
    - __valid_from_dttm

{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{{
    satellite(
        source_model=metadata_dict["source_model"],
        source_pk=metadata_dict["source_pk"],
        columns=metadata_dict["columns"]
    )
}}