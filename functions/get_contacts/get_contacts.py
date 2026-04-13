import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])
dynamodb_client = boto3.client('dynamodb', region_name='eu-west-1')

def lambda_handler(event, context):
    params = event.get('queryStringParameters') or {}
    limit = int(params.get('limit', 10))

    result = table.scan(Limit=limit)

    table_info = dynamodb_client.describe_table(TableName=os.environ['TABLE_NAME'])
    total = table_info['Table']['ItemCount']

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'items': result['Items'],
            'total': total
        })
    }