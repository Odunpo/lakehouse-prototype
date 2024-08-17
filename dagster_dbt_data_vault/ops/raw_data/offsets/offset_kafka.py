from typing import List

from confluent_kafka import KafkaException

from dagster_dbt_data_vault.ops.raw_data.types import KafkaTopicOffset


class PartitionsKafkaRepository:
    def __init__(self, conn, topic: str):
        self._conn = conn
        self._topic = topic

    def get_offsets(self) -> List[KafkaTopicOffset]:
        offsets = []

        with self._conn.get_consumer() as consumer:
            cluster_metadata = consumer.list_topics(topic=self._topic)
            topic_metadata = cluster_metadata.topics[self._topic]

            if topic_metadata.error:
                raise KafkaException(topic_metadata.error.str())

            for _, p in topic_metadata.partitions.items():
                offsets.append(
                    KafkaTopicOffset(
                        topic=self._topic,
                        partition=p.id,
                        offset=0
                    )
                )

        return offsets
