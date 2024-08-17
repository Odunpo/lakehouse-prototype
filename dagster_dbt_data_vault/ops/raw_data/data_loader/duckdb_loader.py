import pandas as pd
from jinja2 import Template

from .iloader import IRawDataLoader


class DuckDBRawDataLoader(IRawDataLoader):
    def __init__(self, conn, database: str, table: str):
        self._conn = conn
        self._database = database
        self._table = table

    def load_data(self, data: pd.DataFrame):
        if not self._check_table_exists():
            self._create_raw_data_table()

        query_template = Template(
            """
            INSERT INTO {{ database }}.{{ table }} (
                SELECT * FROM data
            )
            """
        )

        query_params = {"database": self._database, "table": self._table}
        query = query_template.render(query_params)

        with self._conn.get_connection() as conn:
            conn.execute(query)

    def _check_table_exists(self) -> bool:
        query_template = Template(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_catalog = '{{ database }}'
            AND table_name = '{{ table }}'
            """
        )

        query_params = {"database": self._database, "table": self._table}
        query = query_template.render(query_params)

        with self._conn.get_connection() as conn:
            conn.execute(query)
            res = conn.fetchone()

        if res:
            return True
        return False

    def _create_raw_data_table(self):
        query_template = Template(
            """
            CREATE TABLE {{ database }}.{{ table }} (
                key VARCHAR NOT NULL,
                value VARCHAR NOT NULL,
                kafka_offset BIGINT NOT NULL,
                kafka_partition BIGINT NOT NULL,
                kafka_topic VARCHAR NOT NULL,
                run_id VARCHAR NOT NULL
            )
            """
        )

        query_params = {"database": self._database, "table": self._table}
        query = query_template.render(query_params)

        with self._conn.get_connection() as conn:
            conn.execute(query)
