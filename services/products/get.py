import os
import json
import datetime
import logging
from botocore.vendored import requests

log = logging.getLogger()
log.setLevel(logging.DEBUG)

def handler(event, context):
  log.debug('Received event {}'.format(json.dumps(event)))
  ## Configuration parameters
  SUPPLIER_API_HOSTNAME = os.environ.get('SUPPLIER_API_HOSTNAME')
  SUPPLIER_API_PORT = os.environ.get('SUPPLIER_API_PORT')
  SUPPLIER_API_APPID = os.environ.get('SUPPLIER_API_APPID')
  SUPPLIER_API_TOKEN = os.environ.get('SUPPLIER_API_TOKEN')
  SUPPLIER_API_METHOD = os.environ.get('SUPPLIER_API_METHOD')
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
  current_time = datetime.datetime.now().time()
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
    "timestamp": str(current_time)
  }

  response = {
    "statusCode": 200,
        "body": json.dumps(body)
  }
  return response
