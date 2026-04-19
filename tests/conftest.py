import os
import sys
import pytest
import boto3
from moto import mock_aws

# Add functions to sys.path so we can import lambda handlers in tests
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'functions'))

@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    os.environ["TABLE_NAME"] = "PhoneBook-AxelAparicio"

@pytest.fixture(scope="function")
def dynamodb(aws_credentials):
    """Mock DynamoDB."""
    with mock_aws():
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.create_table(
            TableName='PhoneBook-AxelAparicio',
            KeySchema=[
                {'AttributeName': 'userId', 'KeyType': 'HASH'},
            ],
            AttributeDefinitions=[
                {'AttributeName': 'userId', 'AttributeType': 'S'},
                {'AttributeName': 'email', 'AttributeType': 'S'},
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'email-index',
                    'KeySchema': [{'AttributeName': 'email', 'KeyType': 'HASH'}],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
                }
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        yield table

@pytest.fixture(scope="function")
def s3(aws_credentials):
    """Mock S3."""
    with mock_aws():
        s3 = boto3.client('s3', region_name='us-east-1')
        bucket_name = "phone-book-csv-axel-portafolio"
        s3.create_bucket(Bucket=bucket_name)
        yield s3

@pytest.fixture(scope="function")
def cognito(aws_credentials):
    """Mock Cognito."""
    with mock_aws():
        client = boto3.client('cognito-idp', region_name='us-east-1')
        user_pool = client.create_user_pool(PoolName='PhoneBook-UserPool-AxelAparicio')
        client.create_user_pool_client(
            UserPoolId=user_pool['UserPool']['Id'],
            ClientName='PhoneBook-Client-AxelAparicio'
        )
        yield client
