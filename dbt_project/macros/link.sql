{%- macro link(source_model, source_pk_1, source_pk_2, link_hk_name) -%}

SELECT DISTINCT
    to_hex(md5(to_utf8({{ source_pk_1['name'] }} || {{ source_pk_2['name'] }}))) AS {{ link_hk_name }},
    to_hex(md5(to_utf8({{ source_pk_1['name'] }}))) AS {{ source_pk_1['name_hk'] }},
    to_hex(md5(to_utf8({{ source_pk_2['name'] }}))) AS {{ source_pk_2['name_hk'] }},
    current_timestamp(6) AS __inserted_at,
    __source_connector AS __record_source,
    __source_details AS __record_source_details,
    max(__source_lsn) AS __record_last_source_lsn
FROM {{ ref(source_model) }}
{%- if is_incremental() %}
WHERE __source_lsn > (
    SELECT max(__record_last_source_lsn)
    FROM {{ this }}
)
{%- endif %}
GROUP BY 1, 2, 3, 4, 5, 6

{%- endmacro -%}