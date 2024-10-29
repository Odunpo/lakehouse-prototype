from abc import ABC, abstractmethod
from enum import Enum

from trino.dbapi import Connection


class IOptimizer(ABC):
    def __init__(self, conn, table: str):
        self._conn = conn
        self._table = table

    @abstractmethod
    def compact_data(self, file_size_mb: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def expire_snapshots(self, retention_days: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove_orphan_files(self, retention_days: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def drop_extended_stats(self) -> None:
        raise NotImplementedError


class TrinoOptimizationCommand(Enum):
    COMPACT = """
        ALTER TABLE {table}
        EXECUTE optimize(file_size_threshold => '{int_param}MB')
    """
    EXPIRE_SNAPSHOTS = """
        ALTER TABLE {table}
        EXECUTE expire_snapshots(retention_threshold => '{int_param}d')
        """
    REMOVE_ORPHAN_FILES = """
        ALTER TABLE {table}
        EXECUTE remove_orphan_files(retention_threshold => '{int_param}d')
    """
    DROP_EXTENDED_STATS = "ALTER TABLE {table} EXECUTE drop_extended_stats"


class TrinoOptimizer(IOptimizer):
    def __init__(self, conn: Connection, table: str):
        super().__init__(conn, table)

    def compact_data(self, file_size_mb: int) -> None:
        query = self._render_query(
            TrinoOptimizationCommand.COMPACT,
            file_size_mb
        )
        self._execute(query)

    def expire_snapshots(self, retention_days: int) -> None:
        query = self._render_query(
            TrinoOptimizationCommand.EXPIRE_SNAPSHOTS, retention_days
        )
        self._execute(query)

    def remove_orphan_files(self, retention_days: int) -> None:
        query = self._render_query(
            TrinoOptimizationCommand.REMOVE_ORPHAN_FILES, retention_days
        )
        self._execute(query)

    def drop_extended_stats(self) -> None:
        query = self._render_query(
            TrinoOptimizationCommand.DROP_EXTENDED_STATS
        )
        self._execute(query)

    def _execute(self, query: str) -> None:
        cur = self._conn.cursor()
        try:
            cur.execute(query)
        finally:
            cur.close()

    def _render_query(
            self,
            optimize_comm: TrinoOptimizationCommand,
            int_param: int = None
    ) -> str:
        if int_param is None:
            return optimize_comm.value.format(
                table=self._sanitize_table_name(self._table)
            )
        return optimize_comm.value.format(
            table=self._sanitize_table_name(self._table),
            int_param=self._sanitize_int_param(int_param)
        )

    @staticmethod
    def _sanitize_table_name(identifier: str) -> str:
        schema, table = identifier.split(".")
        if not schema.isidentifier():
            raise ValueError("Invalid schema name provided")
        if not table.isidentifier():
            raise ValueError("Invalid table name provided")
        return identifier

    @staticmethod
    def _sanitize_int_param(param: int) -> int:
        if not isinstance(param, int) or param <= 0:
            raise ValueError("Parameter must be a positive integer")
        return param
