from typing import List

from dagster import asset, MaterializeResult, Config, AssetsDefinition

from dagster_dbt_data_vault.resources.trino import TrinoResource
from dagster_dbt_data_vault.common.configuration import AssetConfiguration


class LastLsnConfig(Config):
    last_lsn: int


class RawDataAssetFactory:
    def __init__(self, configs: List[AssetConfiguration]):
        self.asset_configs = configs

    def create_assets(self) -> List[AssetsDefinition]:
        assets = []
        for asset_config in self.asset_configs:
            assets.append(
                self._create_asset(
                    name=asset_config.name,
                    prefix=asset_config.prefix,
                    description=asset_config.description,
                    group=asset_config.group,
                    table=asset_config.table,
                )
            )

        return assets

    @staticmethod
    def _create_asset(
            name: str,
            prefix: str,
            description: str,
            group: str,
            table: str,
    ) -> AssetsDefinition:
        @asset(
            name=name,
            key_prefix=prefix,
            description=description,
            group_name=group,
            compute_kind="Python",
        )
        def _asset(trino: TrinoResource, config: LastLsnConfig):
            # TODO: add safe query rendering. Example: TrinoOptimizer
            query = f"""
                SELECT count(*)
                FROM {table}
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
