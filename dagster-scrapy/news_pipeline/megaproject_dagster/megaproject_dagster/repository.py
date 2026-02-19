from dagster import repository
from .jobs.megaprojectnews_job import scrapy_job
from .assests.megaprojectnews_assets import scrapy_data

from dagster import Definitions
from megaproject_dagster.assets.megaprojectnews_assets import scrapy_data
from megaproject_dagster.jobs.megaprojectnews_job import scrape_and_upload
from megaproject_dagster.schedules.megaprojectnews_schedule import (
    daily_scrapy_schedule,
    scrape_and_upload_schedule,
)

defs = Definitions(
    assets=scrapy_data,
    jobs=[scrape_and_upload],
    schedules=[scrape_and_upload_schedule, daily_scrapy_schedule],
)


@repository
def megaproject_repository():
    return [scrapy_job, scrapy_data]
