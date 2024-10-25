{{ config(materialized='incremental', schema='parsed_data') }}

{%- set yaml_metadata -%}

source_name: raw_data
source_table: raw_users
columns:
    - name: id
      type: VARCHAR
    - name: email
      type: VARCHAR
    - name: name
      type: VARCHAR
    - name: created_at
      custom_json_extraction: DATE_ADD('day', JSON_VALUE(data, 'lax $.created_at' RETURNING INT), DATE '1970-01-01')

{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{{
    parse_raw_data(
        source_name=metadata_dict["source_name"],
        source_table=metadata_dict["source_table"],
        columns=metadata_dict["columns"]
    )
}}