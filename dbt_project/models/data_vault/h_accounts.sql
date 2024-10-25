{{
    config(
        materialized='incremental',
        schema='data_vault',
        unique_key='accounts_hk',
        incremental_strategy='merge',
        merge_update_columns=['__record_last_source_lsn']
    )
}}

{{
    hub(
        source_model='parsed_accounts',
        source_pk={
            'name': 'id',
            'name_hk': 'accounts_hk',
            'name_id': 'accounts_id'
        }
    )
}}