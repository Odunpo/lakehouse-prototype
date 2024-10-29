from contextlib import contextmanager

from dagster import ConfigurableResource, EnvVar
from pydantic import Field
from trino.dbapi import connect, Connection


class TrinoResource(ConfigurableResource):
    """Resource for interacting with a Trino database."""

    host: str = Field(
        description="Host to connect to Trino database",
    )
    port: int = Field(
        description="Port to connect to Trino database",
        default=8080,
    )
    user: str = Field(
        description="User to connect to Trino database",
        default=None,
    )
    catalog: str = Field(
        description="Catalog to connect to Trino",
        default=None,
    )
    schema: str = Field(
        description="Schema to connect to Trino",
        default=None,
    )

    @contextmanager
    def get_connection(self) -> Connection:
        conn = connect(
            host=self.host,
            port=self.port,
            user=self.user,
            catalog=self.catalog,
            schema=self.schema,
        )

        yield conn

        conn.commit()
        conn.close()


trino_resource = TrinoResource(
    host=EnvVar("TRINO_HOST"),
    port=EnvVar.int("TRINO_PORT"),
    user=EnvVar("TRINO_USER"),
    catalog=EnvVar("TRINO_CATALOG"),
    schema=EnvVar("TRINO_SCHEMA"),
)
