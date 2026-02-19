from dagster import job
from megaproject_dagster.assests.megaprojectnews_assets import scrapy_data
from megaproject_dagster.ops.megaprojectnews_ops import scrape_data, upload_to_s3


@job
def scrapy_job():
    scrapy_data()


@job(resource_defs={"s3": s3_resource})
def scrape_and_upload():
    file_path = scrape_data()
    upload_to_s3(file_path)
