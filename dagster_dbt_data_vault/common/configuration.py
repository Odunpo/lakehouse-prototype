from __future__ import annotations

from typing import List, Optional

import yaml
from pydantic import BaseModel


class AssetConfiguration(BaseModel):
    name: str
    prefix: str
    group: Optional[str] = None
    description: Optional[str] = None
    table: Optional[str] = None
    upstream: Optional[AssetConfiguration] = None
    downstream: Optional[AssetConfiguration] = None

    @classmethod
    def from_dict(cls, data: dict) -> AssetConfiguration:
        if isinstance(data.get("upstream"), dict):
            data["upstream"] = cls.from_dict(data["upstream"])
        if isinstance(data.get("downstream"), dict):
            data["downstream"] = cls.from_dict(data["downstream"])
        return cls(**data)


class JobConfiguration(BaseModel):
    name: str
    asset: AssetConfiguration


class SensorConfiguration(BaseModel):
    name: str
    job: JobConfiguration


def load_configuration_file(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def create_asset_configurations(config: dict) -> List[AssetConfiguration]:
    return [AssetConfiguration.from_dict(c) for c in config["assets"]]


def create_job_configurations(
        assets_conf: List[AssetConfiguration]
) -> List[JobConfiguration]:
    return [
        JobConfiguration(name=a.name + "_job", asset=a) for a in assets_conf
    ]


def create_sensor_configurations(
        jobs_conf: List[JobConfiguration]
) -> List[SensorConfiguration]:
    return [
        SensorConfiguration(
            name=job.asset.name + "_sensor",
            job=job,
        ) for job in jobs_conf
    ]
