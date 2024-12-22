from setuptools import find_packages, setup

setup(
    name="pipelines",
    packages=find_packages(exclude=["orchestration_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster-dbt",
        "pandas",
        "polars",
        "dbt-core",
        "dbt-duckdb",
        "dagster-duckdb",
        "dagster-duckdb-pandas",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
