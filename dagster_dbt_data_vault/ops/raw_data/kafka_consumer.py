import sys
from typing import List

from confluent_kafka import KafkaException, KafkaError, TopicPartition

from .types import KafkaTopicOffset, KafkaMessage


class KafkaConsumer:
    def __init__(self, conn, topic_offsets: List[KafkaTopicOffset]):
        self._conn = conn
        self._topic_offsets = topic_offsets

    def poll_messages(self) -> List[KafkaMessage]:
        messages = []
        running = True

        with self._conn.get_consumer() as consumer:
            consumer.assign(
                [TopicPartition(**o.dict()) for o in self._topic_offsets]
            )

            while running:
                msg = consumer.poll(timeout=1.0)
                if msg is None:
                    running = False
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        sys.stderr.write(
                            '%% %s [%d] reached end at offset %d\n' %
                            (msg.topic(), msg.partition(), msg.offset())
                        )
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    if msg.value() is not None:
                        messages.append(
                            KafkaMessage(
                                key=msg.key(),
                                value=msg.value(),
                                offset=msg.offset(),
                                partition=msg.partition(),
                            )
                        )

        return messages
