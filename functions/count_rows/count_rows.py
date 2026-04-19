import boto3

def count_items():
    client = boto3.client('dynamodb', region_name='us-east-1')
    paginator = client.get_paginator('scan')
    
    # Usamos Select='COUNT' para no traer los datos, solo el número
    response_iterator = paginator.paginate(
        TableName='PhoneBook-AxelAparicio', 
        Select='COUNT'
    )
    
    total = 0
    print("Contando páginas de DynamoDB...")
    for page in response_iterator:
        total += page['Count']
        print(f"Van: {total}", end='\r')
        
    print(f"\n¡Total exacto de registros: {total}!")

if __name__ == "__main__":
    count_items()