from contextlib import contextmanager

from confluent_kafka import Consumer
from dagster import ConfigurableResource, EnvVar
from pydantic import Field


class KafkaResource(ConfigurableResource):
    bootstrap_servers: str = Field(
        description="Kafka bootstrap servers host:port"
    )
    group_id: str = Field(
        description="Kafka group id"
    )
    auto_offset_reset: str = Field(
        description="Kafka auto-offset",
        default="earliest"
    )

    @classmethod
    def _is_dagster_resource(cls) -> bool:
        return True

    @contextmanager
    def get_consumer(self):
        conf = {
            "bootstrap.servers": self.bootstrap_servers,
            "group.id": self.group_id,
            "auto.offset.reset": self.auto_offset_reset,
        }
        consumer = Consumer(conf)

        yield consumer

        consumer.close()


kafka_resource = KafkaResource(
    bootstrap_servers=EnvVar("KAFKA_BROKER_URL"),
    group_id=EnvVar("KAFKA_GROUP_ID"),
)
