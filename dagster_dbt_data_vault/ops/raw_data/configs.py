from dagster import Config


class KafkaTopicConfig(Config):
    topic: str


class OffsetTableConfig(Config):
    database: str
    table: str
    topic: str


class DestinationTableConfig(Config):
    database: str
    table: str
