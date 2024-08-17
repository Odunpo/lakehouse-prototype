from abc import ABC, abstractmethod
from typing import Dict, List, Union

from jinja2 import Template

from dagster_dbt_data_vault.ops.raw_data.types import KafkaTopicOffset


class IOffsetDbRepository(ABC):
    @abstractmethod
    def get_offsets(self) -> List[Dict[str, Union[str, int]]]:
        raise NotImplementedError

    def set_offsets(self, offsets: List[tuple]) -> None:
        raise NotImplementedError


class OffsetDuckDbRepository(IOffsetDbRepository):
    def __init__(
            self,
            conn,
            database: str,
            table: str,
            topic: str,
    ):
        self._conn = conn
        self._database = database
        self._table = table
        self._topic = topic

    def get_offsets(self) -> List[KafkaTopicOffset]:
        query_template = Template(
            """
            SELECT
                topic,
                partition,
                topic_offset
            FROM {{ db }}.{{ table }}
            WHERE topic = '{{ topic }}'
            """
        )

        query_params = {
            "db": self._database,
            "table": self._table,
            "topic": self._topic,
        }
        query = query_template.render(query_params)

        with self._conn.get_connection() as conn:
            conn.execute(query)
            res = conn.fetchall()

        offsets = []
        for row in res:
            offsets.append(
                KafkaTopicOffset(
                    topic=row[0],
                    partition=row[1],
                    offset=row[2],
                )
            )

        return offsets

    def set_offsets(self, offsets: List[KafkaTopicOffset]) -> None:
        query_template = Template(
            """
            INSERT INTO {{ db }}.{{ table }} (topic, partition, topic_offset)
            VALUES (?, ?, ?)
            ON CONFLICT (topic, partition)
            DO UPDATE SET
                topic_offset = EXCLUDED.topic_offset,
                last_updated = get_current_timestamp()
            """
        )

        query_params = {
            "db": self._database,
            "table": self._table,
        }
        query = query_template.render(query_params)

        with self._conn.get_connection() as conn:
            for o in offsets:
                conn.execute(query, (o.topic, o.partition, o.offset))
