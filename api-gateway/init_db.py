import boto3

def create_tables():
    dynamo_db = boto3.resource('dynamodb', endpoint_url='http://dynamodb-local:8000')

    # Create DynamoDB Table
    dynamo_db.create_table(
        TableName='dummy-table',
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        BillingMode='PROVISIONED',
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        },
    )


def put_items():
    dynamo_db = boto3.resource('dynamodb', endpoint_url='http://dynamodb-local:8000')
    
    # PutItems in DynamoDB
    initial_data = [
        {
            'id': '1',
            'firstName': 'Jhon',
            'lastName': 'Parker',
            'email': 'jparker@example.com'
        },
        {
            'id': '2',
            'firstName': 'Mary',
            'lastName': 'Hops',
            'email': 'mhops@example.com'
        }
    ]

    table = dynamo_db.Table('dummy-table')

    for item in initial_data:
        table.put_item(Item=item)

