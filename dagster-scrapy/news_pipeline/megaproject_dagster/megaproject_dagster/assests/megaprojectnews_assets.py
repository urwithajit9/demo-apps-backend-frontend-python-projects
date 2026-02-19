from dagster import asset
from megaproject_dagster.ops.megaprojectnews_ops import run_scrapy_spider


@asset
def scrapy_data():
    # Run the Scrapy spider
    run_scrapy_spider()

    # Return a reference to the output file
    return {"output_file": "dagster_outputs/scrapy/quotes.json"}


# from dagster import asset, with_resources
# from my_dagster.ops.scrapy_ops import run_scrapy_spider
# from my_dagster.resources.s3_resource import s3_resource


# @with_resources(
#     {"s3": s3_resource},
# )
# @asset
# def scrapy_data(context):
#     # Run the Scrapy spider
#     run_scrapy_spider()

#     # Upload the file to S3
#     s3 = context.resources.s3
#     output_file = "dagster_outputs/scrapy/example_spider.json"
#     s3.upload_file(output_file, "my-s3-bucket", "scrapy-output/example_spider.json")

#     return {"output_file": output_file}
