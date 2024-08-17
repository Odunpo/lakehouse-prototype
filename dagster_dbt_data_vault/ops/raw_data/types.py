from pydantic import BaseModel


class KafkaTopicOffset(BaseModel):
    topic: str
    partition: int
    offset: int


class KafkaMessage(BaseModel):
    key: str
    value: str
    offset: int
    partition: int
