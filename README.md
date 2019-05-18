# dexcom-lambda
Cron lambda to scrape real time glucose values from dexcom

## How does this work.
This lambda function impersonates a share app, and asks for the most recent blood glucose value.
This is better than the offical Dexcom API because there is a 3 hour lag time on that one.

## What will it deploy?
- 1 AWS Python Lambda Function
- 1 Dynamo DB Table

## How Can I get Started:
If you have pycharm:  
    - (make sure you have the aws extension), 
    - clone the project, right click on the template, 
    - click deploy serverless template, 
    - update the two parameters for dexcom username and password, 
    - then Done!

# GOALS:
- python
- aws lambda
- aws DynamoDB
- Eventually switch to aws timetream?

#### Credit
This is heavily based on the javascript project located here:
https://github.com/nightscout/share2nightscout-bridge
BY: Ben West

#### Random Helpful Links
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.03.html

#### Useful Commands
 aws s3 mb s3://dev-dexcom-lambda
 aws cloudformation package --template-file /Users/danieldiaz/github/dexcom-lambda/.aws-sam/build/template.yaml --s3-bucket dev-dexcom-lambda --output-template-file packaged.yaml
 aws cloudformation deploy --template-file /Users/danieldiaz/github/dexcom-lambda/packaged.yaml --stack-name dev-dexcom-lambda --parameter-overrides DEXCOM_ACCOUNT_NAME=<YOUR-DEXCOM-USERNAME-HERE> DEXCOM_PASSWORD=<YOUR-DEXCOM-PASSWORD-HERE>
