{%- macro parse_raw_data(source_name, source_table, columns) -%}

SELECT
    {% for column in columns %}
        {%- if column.get('custom_json_extraction') != None -%}
            {{ column.get('custom_json_extraction') }} AS {{ column['name'] }},
        {%- else -%}
            JSON_VALUE(data, 'lax $.{{ column["name"] }}' RETURNING {{ column['type'] }}) AS {{ column['name'] }},
        {%- endif %}
    {% endfor -%}
    CASE WHEN op = 'd' THEN true ELSE false END AS __deleted_flag,
    CAST(DATE_ADD('millisecond', CAST(source_ts_ms AS BIGINT) % 1000, FROM_UNIXTIME(CAST(source_ts_ms AS BIGINT) / 1000)) AS TIMESTAMP(6)) AS __valid_from_dttm,
    source_lsn AS __source_lsn,
    source_connector AS __source_connector,
    source_db || '.' || source_schema || '.' || source_table AS __source_details,
    CURRENT_TIMESTAMP(6) AS __inserted_at
FROM {{ source(source_name, source_table) }}
{% if is_incremental() %}
WHERE source_lsn > (SELECT max(__source_lsn) FROM {{ this }})
{% endif %}

{%- endmacro -%}