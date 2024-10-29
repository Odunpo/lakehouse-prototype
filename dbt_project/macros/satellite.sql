{%- macro satellite(source_model, source_pk, columns) -%}

SELECT
    to_hex(md5(to_utf8({{ source_pk['name'] }}))) AS {{ source_pk['name_hk'] }},
    {% for column in columns %}
        {{ column }},
    {% endfor -%}
    current_timestamp(6) AS __inserted_at,
    __source_connector AS __record_source,
    __source_details AS __record_source_details,
    __source_lsn AS __record_source_lsn
FROM {{ ref(source_model) }}
{%- if is_incremental() %}
WHERE __source_lsn > (
    SELECT max(__record_source_lsn)
    FROM {{ this }}
)
{%- endif %}

{%- endmacro -%}