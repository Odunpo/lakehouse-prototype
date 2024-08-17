CREATE TABLE kafka_offsets (
    topic VARCHAR NOT NULL,
    partition INT NOT NULL,
    topic_offset BIGINT NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (topic, partition)
);
