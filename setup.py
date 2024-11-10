from setuptools import find_packages, setup

setup(
    name="dagster_dbt_data_vault",
    packages=find_packages(exclude=["dagster_dbt_data_vault_tests"]),
    install_requires=[
        "dagster==1.8.13",
        "dagster-cloud==1.8.13",
        "dagster-dbt==0.24.13",
        "dagster-aws==0.24.13",
        "dbt-trino==1.8.2",
        "Jinja2==3.1.4",
        "pyyaml==6.0.2",
        "trino==0.330.0",
        "pydantic==2.9.2",
    ],
    extras_require={
        "dev": [
            "dagster-webserver==1.8.13",
            "pytest==8.3.3",
            "faker==30.8.1"
        ]
    },
)
