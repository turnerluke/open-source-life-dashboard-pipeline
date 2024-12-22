# from dagster import load_assets_from_modules

from .finances import assets as finance_assets

# all_assets = load_assets_from_modules([finances])
all_assets = finance_assets

#print(all_assets)