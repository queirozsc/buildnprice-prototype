import os
import json
import http.client
# from aws_xray_sdk.core import xray_recorder
# from aws_xray_sdk.core import patch

# patch(['botocore'])

# @xray_recorder.capture('products/get/{id}')
def get(event, context):
  url = os.environ.get('SUPPLIER_API_HOSTNAME')
  port = os.environ.get('SUPPLIER_API_PORT')
  app_id = os.environ.get('SUPPLIER_API_APPID')
  token = os.environ.get('SUPPLIER_API_TOKEN')
  mode = os.environ.get('SUPPLIER_API_METHOD')
  product_id = event['pathParameters']['id']
  
  conn = http.client.HTTPConnection(url, port)
  payload = "{\n  \"app_id\": \"" + app_id \
    +"\",\n  \"token\": \"" + token \
    +"\",\n  \"mode\": \"" + mode \
    + "\",\n  \"produtos\": [\"" + product_id + "\"]\n}"
  
  print(payload)
  headers = {
    'content-type': "application/json",
    'host': "{}:{}".format(url, port),
    'x-amz-date': "20170807T191827Z",
    'authorization': "AWS4-HMAC-SHA256 Credential=/20170807/us-east-1/execute-api/aws4_request, SignedHeaders=content-type;host;x-amz-date, Signature=0552d73111e76ef923d9379c98dfdbdca45e5231c1ea9b74843fe916cc3d3ff7",
    'cache-control': "no-cache",
    'postman-token': "baf19c2e-6e26-54c1-2b9d-c39bf6614307"
  }
  
  conn.request("POST", "/", payload, headers)
  res = conn.getresponse()
  data = res.read()
  body = data.decode("utf-8")
  # xray_recorder.current_subsegment().put_annotation('http.client.response', body)
  response = {
    "statusCode": 200,
    "body": json.dumps(data.decode("utf-8"))
  }
  return response
