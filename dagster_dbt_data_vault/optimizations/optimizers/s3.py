from datetime import datetime, timedelta, UTC
from typing import List

from dagster_aws.s3 import S3Resource


class S3Optimizer:
    def __init__(
            self,
            s3: S3Resource,
            bucket: str,
            prefixes: List[str],
            retention_hours: int
    ):
        self._s3 = s3
        self._bucket = bucket
        self._prefixes = prefixes
        self._retention = timedelta(hours=retention_hours)

    def _list_objects_by_prefix(self, prefix: str) -> List[dict]:
        objects = self._s3.get_client().list_objects_v2(
            Bucket=self._bucket,
            Prefix=prefix,
        )

        return [
            {"key": o["Key"], "last_modified": o["LastModified"]}
            for o in objects["Contents"]
        ]

    def _filter_by_retention(self, objects: List[dict]) -> List[dict]:
        threshold = datetime.now(UTC) - self._retention

        return [o for o in objects if o["last_modified"] < threshold]

    def delete_stale_dbt_tmp_objects(self) -> List[str]:
        objects = []
        for prefix in self._prefixes:
            objects.extend(self._list_objects_by_prefix(prefix))

        objects = self._filter_by_retention(objects)
        dbt_objects = [o["key"] for o in objects if "__dbt_tmp" in o["key"]]

        for o in dbt_objects:
            self._s3.get_client().delete_object(Bucket=self._bucket, Key=o)

        return dbt_objects
