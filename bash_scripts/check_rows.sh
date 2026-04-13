#!/bin/bash

aws dynamodb scan \
  --table-name PhoneBook-AxelAparicio \
  --region eu-west-1 \
  --select COUNT \
  --query "Count"