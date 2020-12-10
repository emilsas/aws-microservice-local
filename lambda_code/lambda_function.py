import os
import json
import boto3

dynamo_db = boto3.resource('dynamodb', endpoint_url='http://dynamodb-local:8000')
table = dynamo_db.Table('dummy-table')


def lambda_handler(event, context):
    if event['httpMethod'] == 'GET':
        obj_id = event['pathParameters'].get('proxy')
        if obj_id:
            result = table.get_item(Key={'id': obj_id}).get('Item')
        else:
            result = table.scan()['Items']
        
        return respond(result)

    if event['httpMethod'] == 'POST':
        body = json.loads(event['body'])
        table.put_item(Item=body)
        return respond(body, 201)

    return respond('Method Not Allowed', 405)


def respond(body, status=200):
    return {
        'body': json.dumps(body),
        'status_code': status,
        'headers':{
            'Content-Type': 'application/json'
        }
    }
