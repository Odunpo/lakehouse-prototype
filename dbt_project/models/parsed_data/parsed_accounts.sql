{{ config(materialized='incremental', schema='parsed_data') }}

{%- set yaml_metadata -%}

source_name: raw_data
source_table: raw_accounts
columns:
    - name: id
      type: VARCHAR
    - name: user_id
      type: VARCHAR
    - name: currency
      type: VARCHAR
    - name: balance
      type: DECIMAL(15,2)
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