
import os
import boto3
import pytest

def load_env(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip().strip("'")

load_env(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

@pytest.fixture(scope="module")
def s3_client():
    aws_access_key_id = os.getenv("aws_access_key_id")
    aws_secret_access_key = os.getenv("aws_secret_access_key")
    endpoint_url = os.getenv("s3_endpoint")
    
    if not all([aws_access_key_id, aws_secret_access_key, endpoint_url]):
        raise ValueError("Missing required S3 environment variables")

    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint_url,
    )
    return s3

@pytest.fixture(scope="module")
def s3_bucket_name():
    s3_path = os.getenv("s3_path")
    if not s3_path:
        raise ValueError("Missing S3 path environment variable")
    return s3_path.replace("s3://", "")

def test_s3_connection(s3_client, s3_bucket_name):
    """
    Tests the S3 connection by listing the contents of the bucket.
    """
    try:
        response = s3_client.list_objects_v2(Bucket=s3_bucket_name)
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
        print(f"Successfully connected to S3 bucket: {s3_bucket_name}")
        if "Contents" in response:
            print("Contents:")
            for obj in response["Contents"]:
                print(f" - {obj['Key']}")
        else:
            print("Bucket is empty.")
    except Exception as e:
        pytest.fail(f"S3 connection test failed: {e}")
