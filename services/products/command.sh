npm init -f
npm install --save serverless-python-requirements
npm install --save raven
npm install --save serverless-sentry-lib
npm install --save-dev serverless-sentry
npm install --save-dev serverless-plugin-canary-deployments
pip install raven
pip freeze > requirements.txt
sls deploy