import os
import json
import boto3

def lambda_handler(event, context):
    print(event)
    return {'body': json.dumps(event), 'status_code': 200, 'headers': {'Content-Type': 'application/json'}}