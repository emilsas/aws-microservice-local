#!/bin/bash

aws dynamodb create-table \
    --table-name test-table \
    --attribute-definitions \
        AttributeName=id,AttributeType=S \
    --key-schema \
        AttributeName=id,KeyType=HASH \
    --endpoint-url http://dynamodb-local:8000 \
--provisioned-throughput \
        ReadCapacityUnits=10,WriteCapacityUnits=5