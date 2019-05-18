# dexcom-lambda
AWS SAM (lambda) function to scrape real time glucose values from dexcom every 5 minutes.

## How does this work.
This aws lambda function impersonates a share app, and asks for the most recent blood glucose value.

## Isnt there already an open source project that can retrieve dexcom date?
Yes! There is! Check it out here: http://www.nightscout.info/  
The reason I decided to make this was for a couple reasons:
- Fun aws lambda project
- data goes in dynamo instead of mlab, which is what nightscout uses
- app is serverless, so may be cheaper than running the full nightscout app on heroku.

## What will it deploy?
- 1 AWS Python Lambda Function
- 1 Dynamo DB Table

## How Can I get Started:

#### Prereqs:
- AWS Acct
- AWS CLI installed
- AWS SAM CLI
- Note: If you run aws --version from your terminal, your executable versions should be at least at these versions: aws-cli/1.16.161 Python/3.7.3 Darwin/18.5.0 botocore/1.12.151

## How to Deploy:
#### Command Line
- make sure your aws credentials are set up, you can type ```aws configure``` to ensure this.
- git clone https://github.com/dddiaz/dexcom-lambda.git
- navigate to the root dir
- create a s3 bucket to put your code into:
```bash
aws s3 mb s3://dev-dexcom-lambda
```
- Package and deploy: (Make sure you update your dexcom user name and password)
```bash
aws cloudformation package --template-file /Users/danieldiaz/github/dexcom-lambda/.aws-sam/build/template.yaml --s3-bucket dev-dexcom-lambda --output-template-file packaged.yaml
 aws cloudformation deploy --template-file /Users/danieldiaz/github/dexcom-lambda/packaged.yaml --stack-name dev-dexcom-lambda --parameter-overrides DEXCOM_ACCOUNT_NAME=<YOUR-DEXCOM-USERNAME-HERE> DEXCOM_PASSWORD=<YOUR-DEXCOM-PASSWORD-HERE>
```
- Done!
- Navigate to your lambda console to see it executing, or go to the dynamodb table Glucose, to check out the data.

#### Pycharm 
- make sure you have the aws extension, 
- clone the project, right click on the template, 
- click deploy serverless template, 
- update the two parameters for dexcom username and password, 
- then Done!

#### Technology GOALS:
- python
- aws lambda
- aws DynamoDB
- Eventually switch to aws timetream?

#### Credit
This project is heavily based on the javascript project located here:
https://github.com/nightscout/share2nightscout-bridge  
BY: Ben West

#### Random Helpful Links
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.03.html