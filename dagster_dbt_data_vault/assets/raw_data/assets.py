from typing import List

from dagster import asset, MaterializeResult, Config, AssetsDefinition

from dagster_dbt_data_vault.resources.raw_data.trino import TrinoResource
from .asset_configuration import (
    AssetConfiguration,
    raw_data_assets_configs,
)


class LastLsnConfig(Config):
    last_lsn: int


class RawDataAssetFactory:
    def __init__(self, asset_configs: List[AssetConfiguration]):
        self.asset_configs = asset_configs

    def create_assets(self) -> List[AssetsDefinition]:
        assets = []
        for asset_config in self.asset_configs:
            assets.append(
                self._create_asset(
                    name=asset_config.name,
                    description=asset_config.description,
                    group_name=asset_config.group_name,
                    table_name=asset_config.table_name,
                )
            )

        return assets

    @staticmethod
    def _create_asset(
            name: str,
            description: str,
            group_name: str,
            table_name: str,
    ) -> AssetsDefinition:
        @asset(
            name=name,
            description=description,
            group_name=group_name,
            compute_kind="Python",
        )
        def _asset(trino: TrinoResource, config: LastLsnConfig):
            query = f"""
                SELECT count(*)
                FROM {table_name}
                WHERE source_lsn > {config.last_lsn}
            """

            with trino.get_connection() as conn:
                cur = conn.cursor()
                cur.execute(query)
                res = cur.fetchone()

            return MaterializeResult(
                metadata={"New rows": res[0] if res else 0}
            )

        return _asset


raw_data_factory = RawDataAssetFactory(raw_data_assets_configs)
raw_data_assets = raw_data_factory.create_assets()
