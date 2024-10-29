from dagster import EnvVar
from dagster_aws.s3 import S3Resource


s3_resource = S3Resource(
    endpoint_url=EnvVar("ICEBERG_S3_ENDPOINT"),
    aws_access_key_id=EnvVar("ICEBERG_S3_ACCESS_KEY"),
    aws_secret_access_key=EnvVar("ICEBERG_S3_SECRET_KEY"),
)
