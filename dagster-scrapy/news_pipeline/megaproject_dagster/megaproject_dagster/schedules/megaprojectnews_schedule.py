from dagster import schedule
from megaproject_dagster.jobs.megaprojectnews_job import scrapy_job, scrape_and_upload


# This schedule runs the Scrapy job daily at midnight UTC.
@schedule(cron_schedule="0 0 * * *", job=scrapy_job, execution_timezone="UTC")
def daily_scrapy_schedule(_context):
    return {}


@schedule(
    cron_schedule="0 * * * *",  # Run hourly (adjust as needed)
    job=scrape_and_upload,
    execution_timezone="UTC",
)
def scrape_and_upload_schedule():
    return {}
