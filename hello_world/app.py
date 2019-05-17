import json
import os

import requests

# Configure ME
# TODO add some validation here
DEXCOM_ACCOUNT_NAME = os.environ['DEXCOM_ACCOUNT_NAME']
DEXCOM_PASSWORD = os.environ['DEXCOM_PASSWORD']

# TODO cache api token here outside of funtion
# SESSION_ID = None
SESSION_ID = "b3e7f4f2-3a43-4110-a359-39edd63f53c6"


def authorize():
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
    return result.text


def refresh_token():
    global SESSION_ID
    if SESSION_ID:
        return
    else:
        SESSION_ID = authorize()


def fetch(minutes=1440, max_count=1):
    querystring = f'https://share1.dexcom.com/ShareWebServices/Services/Publisher/ReadPublisherLatestGlucoseValues' \
        f'?sessionID={SESSION_ID}&minutes={minutes}&maxCount={max_count}'
    headers = { 'User-Agent': "Dexcom Share/3.0.2.11 CFNetwork/711.2.23 Darwin/14.0.0",
                'Content-Type': 'application/json',
                'Accept': 'application/json'}
    body = {}
    result = requests.post(querystring, json=body, headers=headers)
    # TODO catch auth error which means session is invalid
    return result.text


# // ?sessionID=e59c836f-5aeb-4b95-afa2-39cf2769fede&minutes=1440&maxCount=1"

DEFAULTS = {
    "applicationId": "d89443d2-327c-4a6f-89e5-496bbb0317db",
    "agent": "Dexcom Share/3.0.2.11 CFNetwork/711.2.23 Darwin/14.0.0",
    "login": 'https://' + "share1.dexcom.com" + '/ShareWebServices/Services/General/LoginPublisherAccountByName',
    "accept": 'application/json',
    'content-type': 'application/json',
    "LatestGlucose": 'https://' + "share1.dexcom.com" + '/ShareWebServices/Services/Publisher/ReadPublisherLatestGlucoseValues',
    "nightscout_upload": '/api/v1/entries.json',
    "nightscout_battery": '/api/v1/devicestatus.json',
    "MIN_PASSPHRASE_LENGTH": 12
}

DIRECTIONS = {
    "NONE": 0,
    "DoubleUp": 1,
    "SingleUp": 2,
    "FortyFiveUp": 3,
    "Flat": 4,
    "FortyFiveDown": 5,
    "SingleDown": 6,
    "DoubleDown": 7,
    "NOT COMPUTABLE": 8,
    "RATE OUT OF RANGE": 9
}


# login_body = {
#     "password": opts.password,
#     "applicationId" : opts.applicationId || Defaults.applicationId,
#     "accountName": opts.accountName
# }



def lambda_handler(event, context):
    """TBD
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
