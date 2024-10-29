{{
    config(
        materialized='incremental',
        schema='data_vault',
        unique_key='users_hk',
        incremental_strategy='merge',
        merge_update_columns=['__record_last_source_lsn']
    )
}}

{{
    hub(
        source_model='parsed_users',
        source_pk={
            'name': 'id',
            'name_hk': 'users_hk',
            'name_id': 'users_id'
        }
    )
}}