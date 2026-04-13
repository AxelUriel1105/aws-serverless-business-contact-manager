#!/bin/bash

aws cognito-idp initiate-auth \
    --auth-flow USER_PASSWORD_AUTH \
    --client-id 2l3k16d6ij467j4bdgfdsenhqe \
    --auth-parameters USERNAME=axel@test.com,PASSWORD=Test1234! \
    --region eu-west-1