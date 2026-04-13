import boto3
import uuid
import os
import csv
import io
import time

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    bucket = event['bucket']
    key = event['key']
    start = event['start']
    end = event['end']

    range_header = f'bytes={start}-{end}'
    response = s3.get_object(Bucket=bucket, Key=key, Range=range_header)
    content = response['Body'].read().decode('utf-8', errors='replace')

    lines = content.split('\n')
    if start == 0:
        lines = lines[1:]
    else:
        lines = lines[1:]

    reader = csv.DictReader(
        io.StringIO('\n'.join(lines)),
        fieldnames=['name', 'phone', 'email']
    )

    batch = []
    inserted = 0

    for row in reader:
        if not row.get('name') or row['name'] == 'name':
            continue
        if not row.get('email') or not row.get('phone') or not row.get('name'):
            continue
        if row['email'].strip() == '' or row['name'].strip() == '':
            continue

        batch.append({
            'PutRequest': {
                'Item': {
                    'userId': str(uuid.uuid4()),
                    'name': row['name'].strip(),
                    'phone': row['phone'].strip(),
                    'email': row['email'].strip()
                }
            }
        })

        if len(batch) == 25:
            write_batch(batch)
            inserted += 25
            batch = []

    if batch:
        write_batch(batch)
        inserted += len(batch)

    return {'statusCode': 200, 'inserted': inserted}


def write_batch(batch):
    unprocessed = batch
    retries = 0
    while unprocessed and retries < 5:
        response = table.meta.client.batch_write_item(
            RequestItems={os.environ['TABLE_NAME']: unprocessed}
        )
        unprocessed = response.get('UnprocessedItems', {}).get(
            os.environ['TABLE_NAME'], []
        )
        if unprocessed:
            retries += 1
            time.sleep(2 ** retries * 0.05)