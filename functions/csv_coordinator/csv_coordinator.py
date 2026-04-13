import json

def lambda_handler(event, context):
    bucket = event['detail']['bucket']['name']
    key = event['detail']['object']['key']
    file_size = event['detail']['object']['size']
    num_workers = 10
    
    if file_size == 0:
        return {'chunks': []}
        
    chunk_size = file_size // num_workers

    chunks = []
    for i in range(num_workers):
        start = i * chunk_size
        # El último worker se lleva el residuo de los bytes
        end = start + chunk_size - 1 if i < num_workers - 1 else file_size - 1
        
        chunks.append({
            'bucket': bucket, 
            'key': key, 
            'start': start, 
            'end': end
        })

    return {
        'chunks': chunks
    }