import os
import json
import datetime
import logging
import boto3
from botocore.vendored import requests
from raven import Client # Offical `raven` module
from raven_python_lambda import RavenLambdaWrapper

log = logging.getLogger()
log.setLevel(logging.DEBUG)

## Parameter Store
ssm = boto3.client('ssm')

def get_secret(key):
  resp = ssm.get_parameter(
    Name=key,
    WithDecryption=True
  )
  return resp['Parameter']['value']
## Configuration parameters
SUPPLIER_API_HOSTNAME = get_secret('SUPPLIER_API_HOSTNAME')
SUPPLIER_API_PORT = get_secret('SUPPLIER_API_PORT')
SUPPLIER_API_APPID = get_secret('SUPPLIER_API_APPID')
SUPPLIER_API_TOKEN = get_secret('SUPPLIER_API_TOKEN')
SUPPLIER_API_METHOD = get_secret('SUPPLIER_API_METHOD')


@RavenLambdaWrapper()
def handler(event, context):
  print('Received event {}'.format(json.dumps(event)))
  product_id = event['pathParameters']['id']
  #Call API from supplier
  url = "http://{0}:{1}/".format(SUPPLIER_API_HOSTNAME, SUPPLIER_API_PORT)

  payload = "{\n  \"app_id\": \"" + SUPPLIER_API_APPID \
      + "\",\n  \"token\": \"" + SUPPLIER_API_TOKEN \
      + "\",\n  \"mode\": \"" + SUPPLIER_API_METHOD \
    + "\",\n  \"produtos\": [\"" + product_id + "\"]\n}"

  headers = {
    'content-type': "application/json",
    'host': "{}:{}".format(SUPPLIER_API_HOSTNAME, SUPPLIER_API_PORT),
    'x-amz-date': "20170807T191827Z",
    'authorization': "AWS4-HMAC-SHA256 Credential=/20170807/us-east-1/execute-api/aws4_request, SignedHeaders=content-type;host;x-amz-date, Signature=0552d73111e76ef923d9379c98dfdbdca45e5231c1ea9b74843fe916cc3d3ff7",
    'cache-control': "no-cache",
    'postman-token': "baf19c2e-6e26-54c1-2b9d-c39bf6614307"
  }
  r = requests.request("POST", url, data=payload, headers=headers).text
  #Formats JSON response
  products = json.loads(r)
  log.debug(products)
  body = {
    "product": products['data'][0]['data'][0]['DESCRICAO'],
    "barcode": products['data'][0]['data'][0]['EAN'],
    "price": products['data'][0]['data'][0]['PRECO1'],
    "manufacturer": products['data'][0]['data'][0]['RAZAO_SOCIAL'],
    "available": products['data'][0]['data'][0]['ESTOQUE1'] \
      + products['data'][0]['data'][0]['ESTOQUE2'] \
      + products['data'][0]['data'][0]['ESTOQUE3'] \
      + products['data'][0]['data'][0]['ESTOQUE4'] \
      + products['data'][0]['data'][0]['ESTOQUE5'],
    "timestamp": str(datetime.datetime.now()),
    "version": '0.3'
  }

  response = {
    "statusCode": 200,
        "body": json.dumps(body)
  }
  return response
