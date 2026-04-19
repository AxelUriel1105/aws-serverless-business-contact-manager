#!/bin/bash

aws dynamodb scan \
  --table-name PhoneBook-AxelAparicio \
  --region us-east-1 \
  --select COUNT \
  --query "Count"