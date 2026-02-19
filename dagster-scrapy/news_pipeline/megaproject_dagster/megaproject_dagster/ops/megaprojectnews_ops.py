import os
from scrapy.crawler import CrawlerProcess
from megaproject_news.news_scrapers.spiders.quotes import QuotesSpider

import subprocess
from dagster import op, Out, Output

OUTPUT_DIR = "dagster_outputs/scrapy"


def run_scrapy_spider():
    # Ensure the output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Configure Scrapy to save output in the output directory
    process = CrawlerProcess(
        settings={
            "FEEDS": {
                f"{OUTPUT_DIR}/quotes.json": {"format": "json"},
            },
        }
    )

    # Run the spider
    process.crawl(QuotesSpider)
    process.start()


@op(out={"file_path": Out(str)}, required_resource_keys={"s3"})
def scrape_data(context) -> str:
    """
    Runs the Scrapy spider and returns the path of the saved file.
    """
    output_path = "output/quotes.json"
    spider_name = "quotes"
    subprocess.run(["scrapy", "crawl", spider_name], check=True)
    context.log.info(f"Scraped data saved to {output_path}")
    return output_path


@op(required_resource_keys={"s3"})
def upload_to_s3(context, file_path: str):
    """
    Uploads the specified file to S3.
    """
    bucket_name = context.resources.s3.resource_config["bucket_name"]
    s3_key = file_path.split("/")[-1]

    context.log.info(f"Uploading {file_path} to s3://{bucket_name}/{s3_key}")
    with open(file_path, "rb") as f:
        context.resources.s3.upload_fileobj(f, bucket_name, s3_key)
    context.log.info(f"File successfully uploaded to s3://{bucket_name}/{s3_key}")
