import json
import boto3
import uuid
import os
import csv
import io

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        csv_content = body['csv_content']

        csv_file = io.StringIO(csv_content)
        reader = csv.DictReader(csv_file)

        inserted = 0
        skipped = 0
        errors = []

        for row in reader:
            if not all(k in row for k in ['name', 'phone', 'email']):
                errors.append(f"Row missing fields: {row}")
                continue

            existing = table.query(
                IndexName='email-index',
                KeyConditionExpression=boto3.dynamodb.conditions.Key('email').eq(row['email'])
            )

            if existing['Count'] > 0:
                skipped += 1
                continue

            table.put_item(Item={
                'userId': str(uuid.uuid4()),
                'name': row['name'],
                'phone': row['phone'],
                'email': row['email']
            })
            inserted += 1

        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'message': f'CSV processed successfully',
                'inserted': inserted,
                'skipped': skipped,
                'errors': errors
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'message': str(e)})
        }
    