npm init -f
npm install --save serverless-python-requirements
npm install --save raven
npm install --save serverless-sentry-lib
npm install --save-dev serverless-sentry
npm install --save-dev serverless-plugin-canary-deployments
npm install --save-dev serverless-kms-secrets
aws ssm put-parameter --name SUPPLIER_API_HOSTNAME --type String --overwrite --value api.apotiguar.com.br
aws ssm put-parameter --name SUPPLIER_API_PORT     --type String --overwrite --value 64462
aws ssm put-parameter --name SUPPLIER_API_METHOD   --type String --overwrite --value bnp_mdlog_get_list
aws ssm put-parameter --name SUPPLIER_API_APPID    --type SecureString --overwrite --value e03ad982449af87ade1899ffbc259eee
aws ssm put-parameter --name SUPPLIER_API_TOKEN    --type SecureString --overwrite --value 47320fd4d355f668a37a5895c15f509720a33a355a8fcac0f18c6f68da243b27
pip install raven
pip freeze > requirements.txt
sls deploy