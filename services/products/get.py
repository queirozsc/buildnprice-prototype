import os
import json
import http.client
import logging
from botocore.vendored import requests

log = logging.getLogger()
log.setLevel(logging.DEBUG)

def handler(event, context):
  log.debug('Received event {}'.format(json.dumps(event)))

  SUPPLIER_API_HOSTNAME = os.environ.get('SUPPLIER_API_HOSTNAME')
  SUPPLIER_API_PORT = os.environ.get('SUPPLIER_API_PORT')
  SUPPLIER_API_APPID = os.environ.get('SUPPLIER_API_APPID')
  SUPPLIER_API_TOKEN = os.environ.get('SUPPLIER_API_TOKEN')
  SUPPLIER_API_METHOD = os.environ.get('SUPPLIER_API_METHOD')
  product_id = event['pathParameters']['id']
  
  conn = http.client.HTTPConnection(SUPPLIER_API_HOSTNAME, SUPPLIER_API_PORT)
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
  
  conn.request("POST", "/", payload, headers)
  res = conn.getresponse()
  data = res.read()
  body = data.decode("utf-8")

  # data = {'api_option': 'paste',
  #         'api_user_key': '',
  #         'api_paste_private': '0',
  #         'api_paste_name': 'AWS Lambda python modules',
  #         'api_paste_expire_date': '1D',
  #         'api_paste_format': 'text',
  #         'api_dev_key': SUPPLIER_API_TOKEN,
  #         'api_paste_code': body}
  # r = requests.post("http://pastebin.com/api/api_post.php", data=data)

  log.debug('Get response: {}'.format(json.dumps(body)))
  response = {
    "statusCode": 200,
    "body": json.dumps(data.decode("utf-8"))
  }
  return response
