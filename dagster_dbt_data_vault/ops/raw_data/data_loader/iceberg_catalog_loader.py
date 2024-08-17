import pandas as pd
import pyarrow as pa
from pyiceberg.catalog import Catalog
from pyiceberg.schema import Schema
from pyiceberg.types import NestedField, StringType, LongType, IntegerType

from .iloader import IRawDataLoader


class IcebergCatalogRawDataLoader(IRawDataLoader):
    def __init__(self, catalog: Catalog, schema: str, table: str):
        self._catalog = catalog
        self._schema = schema
        self._table = table

    def load_data(self, data: pd.DataFrame):
        if not self._check_table_exists():
            self._create_raw_data_table()

        df_schema = pa.schema([
            ("key", pa.string(), False),
            ("value", pa.string(), False),
            ("kafka_offset", pa.uint64(), False),
            ("kafka_partition", pa.uint16(), False),
            ("kafka_topic", pa.string(), False),
            ("run_id", pa.string(), False),
        ])

        df = pa.Table.from_pandas(data, df_schema)

        table = self._catalog.load_table(f"{self._schema}.{self._table}")
        table.append(df)

    def _check_table_exists(self) -> bool:
        tables = self._catalog.list_tables(self._schema)
        for _, table in tables:
            if table == self._table:
                return True
        return False

    def _create_raw_data_table(self):
        schema = Schema(
            NestedField(1, "key", StringType(), required=True),
            NestedField(2, "value", StringType(), required=True),
            NestedField(3, "kafka_offset", LongType(), required=True),
            NestedField(4, "kafka_partition", IntegerType(), required=True),
            NestedField(5, "kafka_topic", StringType(), required=True),
            NestedField(6, "run_id", StringType(), required=True),
        )

        self._catalog.create_table(
            identifier=f"{self._schema}.{self._table}",
            schema=schema
        )
