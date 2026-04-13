#!/bin/bash

aws dynamodb delete-table --table-name PhoneBook-AxelAparicio --region eu-west-1

aws dynamodb wait table-not-exists --table-name PhoneBook-AxelAparicio --region eu-west-1

aws dynamodb create-table \
    --table-name PhoneBook-AxelAparicio \
    --region eu-west-1 \
    --billing-mode PAY_PER_REQUEST \
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
                "Projection": {"ProjectionType": "ALL"}
            }
        ]'