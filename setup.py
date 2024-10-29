from setuptools import find_packages, setup

setup(
    name="dagster_dbt_data_vault",
    packages=find_packages(exclude=["dagster_dbt_data_vault_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster-dbt",
        "dagster-aws",
        "dbt-trino",
        "jinja2",
        "pyyaml",
        "trino",
        "pydantic",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest", "faker"]},
)
