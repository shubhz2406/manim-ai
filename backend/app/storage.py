import boto3

s3 = boto3.client(
    "s3",
    endpoint_url="http://127.0.0.1:9000",  # MinIO endpoint
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin",
    region_name="us-east-1"
)

BUCKET_NAME = "manim-videos"
