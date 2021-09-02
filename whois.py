import boto3
import json
import logging
import os
from base64 import b64decode

from urllib.parse import parse_qs
from botocore.exceptions import ClientError

from secret_man import get_secret

logger = logging.getLogger()
logger.setLevel(logging.INFO)

expected_token = json.loads(get_secret())['otterbot_slack_verification']


def respond(err, res=None):
    print(json.dumps(res).encode('utf8'))
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res).encode('utf8'),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    decoded_body = b64decode(event['body'])
    params = parse_qs(decoded_body)
    token = params[b'token'][0].decode('utf8')
    if token != expected_token:
        logger.error("Request token (%s) does not match expected", token)
        return(Exception())
    user = params[b'user_name'][0].decode('utf8')
    command = params[b'command'][0].decode('utf8')
    channel = params[b'channel_name'][0].decode('utf8')
    print(params)
    if b'text' in params:
        command_text = params[b'text'][0].decode('utf8')
    else:
        command_text = ''

    payload = {
        "response_type": "in_channel",
        "text": f"{user} invoked {command} in {channel} with the following text: {command_text}"
    }

    return respond(None, payload)
