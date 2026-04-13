#!/bin/bash

aws dynamodb delete-table --table-name PhoneBook-AxelAparicio --region eu-west-1

aws dynamodb wait table-not-exists --table-name PhoneBook-AxelAparicio --region eu-west-1

aws dynamodb create-table \
    --table-name PhoneBook-AxelAparicio \
    --region eu-west-1 \
    --billing-mode PROVISIONED \
    --provisioned-throughput ReadCapacityUnits=100,WriteCapacityUnits=5000 \
    --attribute-definitions \
        AttributeName=userId,AttributeType=S \
        AttributeName=email,AttributeType=S \
    --key-schema \
        AttributeName=userId,KeyType=HASH \
    --global-secondary-indexes \
        '[
            {
                "IndexName": "email-index",
                "KeySchema": [{"AttributeName": "email", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {"ReadCapacityUnits": 100, "WriteCapacityUnits": 5000}
            }
        ]'

aws dynamodb wait table-exists --table-name PhoneBook-AxelAparicio --region eu-west-1
echo "Table ready!"