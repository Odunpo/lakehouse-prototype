{%- macro hub(source_model, source_pk) -%}

SELECT
    to_hex(md5(to_utf8({{ source_pk['name'] }}))) AS {{ source_pk['name_hk'] }},
    {{ source_pk['name'] }} AS {{ source_pk['name_id'] }},
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
GROUP BY 1, 2, 3, 4, 5


{%- endmacro -%}