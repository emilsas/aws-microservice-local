# AWS Microservice Local
This repo emulates the AWS stack for building microservices based on Lambda, API Gateway and DynamoDB.

**NOTE:** Only supports Python environment for Lambda.

## Init (using DynamoDB table)
In ``api-gateway/init_db.py`` you can create many tables as you wish as well as put initial items in them.

Remember to keep ``endpoint-url=http://dynamodb-local:8000`` option in boto3 client or resource to commit changes in your local db.

## Develop
1. Write your code in ``lambda_code/lambda_function.py`` (Keep this names, please :) )
2. Run ``docker-compose up`` in root directory of the project.
3. Make a request to http://localhost:5000/path

## Extras
- If you want to use other AWS Services in local lambda function, provide AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in ``docker-compose.yml``. DynamoDB local does not verify keys.
- You can change your local port mapping in ``docker-compose.yml``. By default Flask uses port 5000.
- If you set Authorization header with a Bearer token, the API decodes JWT token (without verifying it) as API Gateway Authorizers do with Cognito UserPool's users.
