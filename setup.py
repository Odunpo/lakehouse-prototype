from setuptools import find_packages, setup

setup(
    name="dagster_dbt_data_vault",
    packages=find_packages(exclude=["dagster_dbt_data_vault_tests"]),
    install_requires=[
        "dagster==1.7.14",
        "dagster-cloud",
        "dagster-dbt",
        "dbt-trino",
        "pandas[parquet]",
        "pyarrow",
        "fastparquet",
        "confluent-kafka",
        "jinja2",
        "pyyaml",
        "pyiceberg[hive]",
        "pyarrow",
        "trino",
        "pydantic",
        "boto3",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest", "faker"]},
)
