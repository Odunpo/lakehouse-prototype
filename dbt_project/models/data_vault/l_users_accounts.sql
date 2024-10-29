{{
    config(
        materialized='incremental',
        schema='data_vault',
        unique_key='users_accounts_hk',
        incremental_strategy='merge',
        merge_update_columns=['__record_last_source_lsn']
    )
}}

{{
    link(
        source_model='parsed_accounts',
        source_pk_1={'name': 'user_id', 'name_hk': 'users_hk'},
        source_pk_2={'name': 'id', 'name_hk': 'accounts_hk'},
        link_hk_name='users_accounts_hk'
    )
}}