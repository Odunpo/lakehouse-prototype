from typing import List, Tuple

import pandas as pd
from dagster import (
    op,
    OpExecutionContext,
    Out,
    Output,
    AssetMaterialization,
    MetadataValue,
)

from dagster_dbt_data_vault.resources.raw_data.iceberg_catalog import (
    IcebergCatalogResource
)
from dagster_dbt_data_vault.resources.raw_data.duckdb import DuckDBResource
from dagster_dbt_data_vault.resources.raw_data.kafka import KafkaResource
from .configs import (
    KafkaTopicConfig,
    OffsetTableConfig,
    DestinationTableConfig,
)
from .data_loader.iceberg_catalog_loader import IcebergCatalogRawDataLoader
from .kafka_consumer import KafkaConsumer
from .offsets import PartitionsKafkaRepository, OffsetDuckDbRepository
from .types import KafkaMessage, KafkaTopicOffset


@op
def retrieve_offsets_from_kafka(
        context: OpExecutionContext,
        kafka: KafkaResource,
        config: KafkaTopicConfig,
) -> List[KafkaTopicOffset]:
    repo = PartitionsKafkaRepository(kafka, config.topic)
    partitions = repo.get_offsets()

    context.log.info(
        f"Retrieved {len(partitions)} partitions for {config.topic}"
    )

    return partitions


@op
def retrieve_offsets_from_db(
        context: OpExecutionContext,
        db: DuckDBResource,
        config: OffsetTableConfig,
) -> List[KafkaTopicOffset]:
    repo = OffsetDuckDbRepository(conn=db, **config.dict())
    offsets = repo.get_offsets()

    context.log.info(
        f"Retrieved offsets: {[o.dict() for o in offsets]} for {config.topic}"
    )

    for offset in offsets:
        if offset.offset > 0:
            offset.offset += 1

    return offsets


@op
def define_offsets(
        context: OpExecutionContext,
        kafka_offsets: List[KafkaTopicOffset],
        db_offsets: List[KafkaTopicOffset],
) -> List[KafkaTopicOffset]:

    if not db_offsets:
        context.log.info("No DB offsets, using Kafka offsets instead")

        return kafka_offsets

    kafka_offsets_df = pd.DataFrame(o.dict() for o in kafka_offsets)
    db_offsets_df = pd.DataFrame(o.dict() for o in db_offsets)

    ind = ["topic", "partition"]
    offsets_df = db_offsets_df.set_index(ind).join(
        kafka_offsets_df.set_index(ind),
        how="outer",
        rsuffix="r",
    ).reset_index().fillna(0)[["topic", "partition", "offset"]]

    offsets = [KafkaTopicOffset(**o) for o in offsets_df.to_dict("records")]

    context.log.info(f"Offsets for extraction: {[o.dict() for o in offsets]}")

    return offsets


@op(out={"messages": Out(is_required=False)})
def extract_kafka_messages(
        context: OpExecutionContext,
        kafka: KafkaResource,
        offsets: List[KafkaTopicOffset],
) -> List[KafkaMessage]:
    consumer = KafkaConsumer(kafka, offsets)
    messages = consumer.poll_messages()

    context.log.info(f"Extracted {len(messages)} messages from kafka")

    if messages:
        yield Output(messages, "messages")


@op
def process_kafka_messages(
        context: OpExecutionContext,
        config: KafkaTopicConfig,
        messages: List[KafkaMessage],
) -> pd.DataFrame:
    df = pd.DataFrame([m.dict() for m in messages])
    df.rename(
        columns={"offset": "kafka_offset", "partition": "kafka_partition"},
        inplace=True,
    )
    df["kafka_topic"] = config.topic
    df["run_id"] = context.run_id

    context.log.info(f"Processed {len(df)} messages. Run id: {context.run_id}")

    return df


@op(out={"offsets": Out(), "num_messages": Out()})
def load_kafka_messages(
        context: OpExecutionContext,
        iceberg_catalog: IcebergCatalogResource,
        processed_messages: pd.DataFrame,
        config: DestinationTableConfig,
) -> Tuple[List[KafkaTopicOffset], int]:
    with iceberg_catalog.get_catalog() as catalog:
        loader = IcebergCatalogRawDataLoader(
            catalog,
            config.database,
            config.table
        )
        loader.load_data(processed_messages)

    num_messages = len(processed_messages)
    context.log.info(f"Loaded {num_messages} messages")

    raw_offsets = processed_messages \
        .groupby(["kafka_topic", "kafka_partition"])["kafka_offset"] \
        .max() \
        .reset_index() \
        .to_dict(orient="records")

    offsets = [
        KafkaTopicOffset(
            topic=offset["kafka_topic"],
            partition=offset["kafka_partition"],
            offset=offset["kafka_offset"],
        )
        for offset in raw_offsets
    ]

    context.log.info(f"New offsets: {[o.dict() for o in offsets]}")

    return offsets, num_messages


@op
def save_offsets(
        context: OpExecutionContext,
        db: DuckDBResource,
        config: OffsetTableConfig,
        offsets: List[KafkaTopicOffset],
        num_messages: int,
):
    repo = OffsetDuckDbRepository(conn=db, **config.dict())
    repo.set_offsets(offsets)

    context.log.info(f"Saved {len(offsets)} offsets")

    context.log_event(
        AssetMaterialization(
            asset_key=context.asset_key,
            metadata={
                "Number of messages": MetadataValue.int(num_messages)
            }
        )
    )
