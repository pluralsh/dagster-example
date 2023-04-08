from dagster import Definitions, load_assets_from_modules

from . import assets, hello

defs = Definitions(
    assets=load_assets_from_modules([assets]),
    jobs=[hello.serial],
    schedules=[hello.scheduled_serial],
)
