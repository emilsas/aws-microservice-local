import jwt
import uuid

from flask import Flask, request, Response
from flask_cors import CORS
from datetime import datetime

from init_db import create_tables, put_items
from lambda_code import lambda_function

try:
    print('Initializing DynamoDB...')
    create_tables()
    put_items()
    print('DynamoDB Table created')
except Exception:
    pass

app = Flask(__name__)
CORS(app)

PREFIX = 'Bearer '

def get_authenticated_user(req):
    auth_header = req.headers.get('Authorization')
    if auth_header and auth_header.startswith(PREFIX):
        return jwt.decode(auth_header[len(PREFIX):], verify=False)

    return None


def parse_request(req, path, proxy):
    now = datetime.now()

    event = {
        "body": str(req.data.decode('utf-8')),
        "resource": f'/{path}' if not proxy else f'/{path}/' + '{proxy+}',
        "path": req.path,
        "httpMethod": req.method,
        "isBase64Encoded": True,
        "queryStringParameters": request.args,
        "pathParameters": {},
        "headers": dict(req.headers),
        "requestContext": {
            "accountId": "123456789012",
            "resourceId": "123456",
            "stage": "prod",
            "requestId": str(uuid.uuid4()),
            "requestTime": now.strftime('%d/%b/%Y:%H:%M:%S +000'),
            "requestTimeEpoch": int(now.timestamp())*1000,
            "identity": {
                "cognitoIdentityPoolId": None,
                "accountId": None,
                "cognitoIdentityId": None,
                "caller": None,
                "accessKey": None,
                "sourceIp": request.remote_addr,
                "cognitoAuthenticationType": None,
                "cognitoAuthenticationProvider": None,
                "userArn": None,
                "userAgent": req.headers.get('User-Agent', ''),
                "user": None
            },
            "path": req.path,
            "resourcePath": f'/{path}' if not proxy else f'/{path}/' + '{proxy+}',
            "httpMethod": req.method,
            "apiId": "1234567890",
            "protocol": "HTTP/1.1"
        }
    }

    user = get_authenticated_user(req)
    if user:
        event['requestContext']['authorizer'] = {
            'claims': user
        }

    if proxy:
        event['pathParameters']['proxy'] = proxy

    return event

    

@app.route('/<path>', methods=['GET', 'POST'])
@app.route('/<path>/<proxy>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def hello(path, proxy=None):
    event = parse_request(request, path, proxy)
    lambda_return = lambda_function.lambda_handler(event, None)
    return lambda_return['body'], lambda_return['status_code'], lambda_return['headers']


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)


