import dagster_dbt_data_vault.common.configuration as conf
from .sensors_factory import create_sensors
from ..jobs import job_configs


sensor_configs = conf.create_sensor_configurations(job_configs)
sensors = create_sensors(sensor_configs)
