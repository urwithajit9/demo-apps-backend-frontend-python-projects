from dagster import resource
import boto3


# @resource
# def s3_resource():
#     return boto3.client("s3")


@resource(config_schema={"bucket_name": str, "aws_region": str})
def s3_resource(init_context):
    return boto3.client(
        "s3",
        region_name=init_context.resource_config["aws_region"],
    )
