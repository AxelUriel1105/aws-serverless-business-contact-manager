import json
import boto3
import uuid
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    body = json.loads(event['body'])

    existing = table.query(
        IndexName='email-index',
        KeyConditionExpression=boto3.dynamodb.conditions.Key('email').eq(body['email'])
    )

    if existing['Count'] > 0:
        return {
            'statusCode': 409,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'message': 'Contact with this email already exists'})
        }

    item = {
        'userId': str(uuid.uuid4()),
        'name': body['name'],
        'phone': body['phone'],
        'email': body['email']
    }

    table.put_item(Item=item)

    return {
        'statusCode': 201,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'message': 'Contact created successfully',
            'userId': item['userId']
        })
    }