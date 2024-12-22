from dagster import load_assets_from_modules, load_assets_from_package_module

#from .crypto import assets as crypto_assets
from . import crypto

#finances_assets = load_assets_from_modules([crypto])

#print(finances_assets)

crypto_assets = load_assets_from_package_module(
    crypto,
    group_name="finances",
    key_prefix="crypto",
)

assets = crypto_assets
