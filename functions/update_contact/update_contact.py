import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    user_id = event['pathParameters']['userId']
    body = json.loads(event['body'])

    result = table.update_item(
        Key={'userId': user_id},
        UpdateExpression='SET #n = :name, phone = :phone, email = :email',
        ExpressionAttributeNames={'#n': 'name'},
        ExpressionAttributeValues={
            ':name': body['name'],
            ':phone': body['phone'],
            ':email': body['email']
        },
        ReturnValues='ALL_NEW'
    )

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(result['Attributes'])
    }