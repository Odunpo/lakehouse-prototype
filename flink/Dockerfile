FROM flink:1.17.1-scala_2.12-java11

ARG REPO=https://repo1.maven.org/maven2

ARG BASE_DIR=/opt/flink
ARG BIN_DIR=$BASE_DIR/bin
ARG LIB_DIR=$BASE_DIR/lib
ARG HADOOP_DIR=/hadoop

ARG GROUP_NAME=flink
ARG USER_NAME=flink

RUN \
     curl -O --output-dir ${LIB_DIR} ${REPO}/com/fasterxml/woodstox/woodstox-core/6.5.1/woodstox-core-6.5.1.jar \
  && curl -O --output-dir ${LIB_DIR} ${REPO}/commons-logging/commons-logging/1.2/commons-logging-1.2.jar \
  && curl -O --output-dir ${LIB_DIR} ${REPO}/org/apache/flink/flink-hadoop-fs/1.17.1/flink-hadoop-fs-1.17.1.jar \
  && curl -O --output-dir ${LIB_DIR} ${REPO}/org/apache/iceberg/iceberg-flink-runtime-1.17/1.3.0/iceberg-flink-runtime-1.17-1.3.0.jar \
  && curl -O --output-dir ${LIB_DIR} ${REPO}/org/apache/iceberg/iceberg-flink/1.3.0/iceberg-flink-1.3.0.jar \
  && curl -O --output-dir ${LIB_DIR} ${REPO}/org/apache/iceberg/iceberg-nessie/1.2.1/iceberg-nessie-1.2.1.jar \
  && curl -O --output-dir ${LIB_DIR} ${REPO}/org/codehaus/staxmate/stax2/2.1/stax2-2.1.jar \
  && curl -O --output-dir ${LIB_DIR} ${REPO}/org/codehaus/woodstox/stax2-api/4.2.1/stax2-api-4.2.1.jar \
  && curl -O --output-dir ${LIB_DIR} ${REPO}/software/amazon/awssdk/bundle/2.20.74/bundle-2.20.74.jar \
  && curl -O --output-dir ${LIB_DIR} ${REPO}/software/amazon/awssdk/url-connection-client/2.20.79/url-connection-client-2.20.79.jar \
  && curl -O --output-dir ${LIB_DIR} ${REPO}/org/apache/flink/flink-connector-kafka/1.17.1/flink-connector-kafka-1.17.1.jar \
  && curl -O --output-dir ${LIB_DIR} ${REPO}/org/apache/flink/flink-sql-avro-confluent-registry/1.17.1/flink-sql-avro-confluent-registry-1.17.1.jar \
  && curl -O --output-dir ${LIB_DIR} ${REPO}/org/apache/kafka/kafka-clients/3.2.3/kafka-clients-3.2.3.jar \
  && curl -O --output-dir ${LIB_DIR} ${REPO}/org/apache/flink/flink-json/1.17.1/flink-json-1.17.1.jar \
  && curl -O --output-dir ${LIB_DIR} ${REPO}/org/apache/flink/flink-csv/1.17.1/flink-csv-1.17.1.jar

RUN \
     curl -O --create-dirs --output-dir ${HADOOP_DIR} https://dlcdn.apache.org/hadoop/common/hadoop-3.3.5/hadoop-3.3.5.tar.gz \
  && tar xzf ${HADOOP_DIR}/hadoop-3.3.5.tar.gz --directory=${HADOOP_DIR} --strip-components=1 \
  && find ${HADOOP_DIR} -mindepth 1 ! -regex "^${HADOOP_DIR}/share\(/.*\)?" -delete \
  && rm -rf ${HADOOP_DIR}/share/doc

RUN \
     adduser ${USER_NAME} ${GROUP_NAME} \
  && chown -R ${GROUP_NAME}:${USER_NAME} ${BASE_DIR} ${HADOOP_DIR} \
  && cp ${BIN_DIR}/sql-client.sh ${BIN_DIR}/sql-client

USER ${USER_NAME}

CMD ["sleep", "infinity"]
