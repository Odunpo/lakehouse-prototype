from contextlib import contextmanager

from dagster import ConfigurableResource, EnvVar
from pydantic import Field
from pyiceberg.catalog import load_catalog


class IcebergCatalogResource(ConfigurableResource):
    catalog_type: str = Field(
        description="The type of Apache Iceberg catalog. Default: rest",
        default="rest",
    )
    uri: str = Field(
        description="Uri of the Apache Iceberg catalog"
    )
    s3_endpoint: str = Field(
        description="The S3 endpoint of the catalog"
    )
    s3_access_key: str = Field(
        description="The S3 access key of the catalog"
    )
    s3_secret_key: str = Field(
        description="The S3 secret key of the catalog"
    )
    io_implementation: str = Field(
        description="The IO implementation of the catalog"
    )

    @classmethod
    def _is_dagster_resource(cls) -> bool:
        return True

    @contextmanager
    def get_catalog(self):
        conf = {
            "uri": self.uri,
            "s3.endpoint": self.s3_endpoint,
            "s3.access-key-id": self.s3_access_key,
            "s3.secret-access-key": self.s3_secret_key,
            "py-io-impl": self.io_implementation,
        }
        catalog = load_catalog(name=self.catalog_type, **conf)

        yield catalog


iceberg_catalog_resource = IcebergCatalogResource(
    catalog_type=EnvVar("ICEBERG_CATALOG_TYPE"),
    uri=EnvVar("ICEBERG_CATALOG_URI"),
    s3_endpoint=EnvVar("ICEBERG_S3_ENDPOINT"),
    s3_access_key=EnvVar("ICEBERG_S3_ACCESS_KEY"),
    s3_secret_key=EnvVar("ICEBERG_S3_SECRET_KEY"),
    io_implementation=EnvVar("ICEBERG_IO_IMPL"),
)
