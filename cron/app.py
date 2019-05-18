import json
import os
import re
import requests
import datetime
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# This is a param of the AWS SAM template, and will be configured there.
DEXCOM_ACCOUNT_NAME = os.environ['DEXCOM_ACCOUNT_NAME']
DEXCOM_PASSWORD = os.environ['DEXCOM_PASSWORD']
REGION = os.getenv('REGION', 'us-west-1')

# I want lambda to try and use the already computed session id if it has already tried logging in during a prev
# execution. This value may be stale or invalid, so need to recover from that case
SESSION_ID = None


def authorize():
    """
    Authorize againsts the dexcom api and save the global session ID
    :return:
    """
    logger.info("Attempting to authorize against the dexcom server and obtain a new session id...")
    url = "https://share1.dexcom.com/ShareWebServices/Services/General/LoginPublisherAccountByName"
    auth_body = dict(password=DEXCOM_PASSWORD,
                     applicationId="d89443d2-327c-4a6f-89e5-496bbb0317db",
                     accountName=DEXCOM_ACCOUNT_NAME)
    headers = {
        'User-Agent': "Dexcom Share/3.0.2.11 CFNetwork/711.2.23 Darwin/14.0.0",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    result = requests.post(url, json=auth_body, headers=headers)
    assert result.status_code == 200
    return result.text.replace('"', '')


def refresh_token():
    """
    Refresh Session ID for dexcom if the global value is None
    :return:
    """
    global SESSION_ID
    if SESSION_ID:
        logger.info("Session ID is not none, so will not attempt to authenticate.")
    else:
        logger.info("Session ID is none, so will need to authorize.")
        SESSION_ID = authorize()
    return


def fetch(minutes=1440, max_count=1):
    """
    Fetch a dexcom glucose reading from the server.
    :param minutes:
    :param max_count:
    :return:
    """
    global SESSION_ID
    querystring = f'https://share1.dexcom.com/ShareWebServices/Services/Publisher/ReadPublisherLatestGlucoseValues' \
        f'?sessionID={SESSION_ID}&minutes={minutes}&maxCount={max_count}'
    headers = {'User-Agent': "Dexcom Share/3.0.2.11 CFNetwork/711.2.23 Darwin/14.0.0",
               'Content-Type': 'application/json',
               'Accept': 'application/json'}
    body = {}
    logger.info("Attempting to fetch data from dexcom with this querystring: " + querystring)
    result = requests.post(querystring, json=body, headers=headers)
    if result.status_code == 200:
        logger.info("Response Text:" + result.text)
        return result.text
    elif result.status_code == 500:
        # 500 means sessionnotvalid
        # Note: There is a possibility here that I may miss a value whenever the token expires. I'm not sure how often
        # the token expires, so depending on the freq i may need to come back to this. For now, i just refresh the token,
        # and assume I will get a good value on the next invocation.
        logger.info("Setting Session ID to None")
        SESSION_ID = None
        refresh_token()
        pass
    else:
        logger.error("Bad Response. Status Code:" + str(result.status_code))


def convert(response):
    """Convert the response text from dexcom into something a little more friendly
    I expect the response text to be of the format:
    [ { DT: '/Date(1426292016000-0700)/',
    ST: '/Date(1426295616000)/',
    Trend: 4,
    Value: 101,
    WT: '/Date(1426292039000)/' } ]
    """
    dexcom_directions = [
        "NONE",
        "DoubleUp",
        "SingleUp",
        "FortyFiveUp",
        "Flat",
        "FortyFiveDown",
        "SingleDown",
        "DoubleDown",
        "NOT COMPUTABLE",
        "RATE OUT OF RANGE"
    ]
    # match on a string of variable len numbers
    m = re.findall(r'(\d+)', response)
    # TODO add some data validation here
    # What happens when data falls outside these expectations, add some failure logic here
    # TODO add hash
    data = {
        'timestamp': int(m[0]),
        'datetime': datetime.datetime.fromtimestamp(int(m[0]) / 1000).strftime("%m/%d/%Y, %H:%M:%S"),
        'trend': int(m[3]),
        'direction': dexcom_directions[int(m[3])],
        'value': int(m[4])
    }
    logger.info(data)
    return data


def post_to_dynamo(glucose_data):
    """Post the data structure to DynamoDB"""
    dynamodb = boto3.resource('dynamodb', region_name=REGION)
    table = dynamodb.Table('Glucose')
    response = table.put_item(
        Item=glucose_data
    )
    logger.info("Put Item succeeded:")
    logger.info(json.dumps(response, indent=4))


def run():
    refresh_token()
    data = convert(fetch())
    post_to_dynamo(data)


def lambda_handler(event, context):
    """AWS Lambda Handler
    """
    run()
