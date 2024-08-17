from setuptools import find_packages, setup

setup(
    name="dagster_dbt_data_vault",
    packages=find_packages(exclude=["dagster_dbt_data_vault_tests"]),
    install_requires=[
        "dagster==1.7.14",
        "dagster-cloud",
        "dagster-duckdb",
        "dagster-dbt",
        "dbt-duckdb",
        "dbt-trino",
        "pandas[parquet]",
        "pyarrow",
        "fastparquet",
        "confluent-kafka",
        "jinja2",
        "pyyaml",
        "pyiceberg[hive]",
        "pyarrow",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest", "faker"]},
)
