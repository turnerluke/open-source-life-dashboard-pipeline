"""
Dagster definitions.
"""

import os
from pathlib import Path

from dagster import (
    Definitions, ScheduleDefinition, load_assets_from_modules, define_asset_job, load_assets_from_package_module
)
from dagster_duckdb_pandas import duckdb_pandas_io_manager
from dagster_dbt import dbt_cli_resource, load_assets_from_dbt_project
from dagster._utils import file_relative_path

from .assets import all_assets
#from . import finances

DBT_PROJECT_DIR = file_relative_path(__file__, "../transformation")
DBT_PROFILES_DIR = file_relative_path(__file__, "../transformation/config")

dbt_assets = load_assets_from_dbt_project(
    DBT_PROJECT_DIR,
    DBT_PROFILES_DIR,
    # prefix the output assets based on the database they live in plus the name of the schema
    key_prefix=["dbt"],
    # prefix the source assets based on just the database
    # (dagster populates the source schema information automatically)
    source_key_prefix=["duckdb"],
)

# python_assets = load_assets_from_modules([assets])
# finance_assets = load_assets_from_package_module(
#     finances,
#     group_name="finances",
# )
# print("Finance assets")
# print(finance_assets)

everything_job = define_asset_job("everything_job", selection='*')

resources = {
    "io_manager": duckdb_pandas_io_manager.configured(
        {"database": os.path.join(DBT_PROJECT_DIR, "duckdb.db")}
    ),
    "dbt": dbt_cli_resource.configured(
        {"project_dir": DBT_PROJECT_DIR, "profiles_dir": DBT_PROFILES_DIR}
    ),
}

defs = Definitions(
    assets=[*all_assets, *dbt_assets],
    resources=resources,
    schedules=[
        ScheduleDefinition(job=everything_job, cron_schedule="@daily"),
    ]
)
