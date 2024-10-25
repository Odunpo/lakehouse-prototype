from abc import ABC, abstractmethod


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
