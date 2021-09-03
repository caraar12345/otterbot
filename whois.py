import boto3
import json
import logging
from base64 import b64decode
import os

from urllib.parse import parse_qs
from botocore.exceptions import ClientError

from secret_man import get_secret
from python_whois.whois import whois
from slack_bolt import App

logger = logging.getLogger()
logger.setLevel(logging.INFO)

EXPECTED_TOKEN = json.loads(get_secret(os.environ.get('slack_verify_secret_name')))[
    os.environ.get('slack_verify_secret_key')]
BOT_TOKEN = json.loads(get_secret(os.environ.get('slack_bot_secret_name')))[
    os.environ.get('slack_bot_secret_key')]
SLACK_SIGNING_SECRET = json.loads(get_secret(os.environ.get('slack_signing_secret_name')))[
    os.environ.get('slack_signing_secret_key')]

slack_app = App(
    token=BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET
)

def respond(err, host=None, whois_result=None, channel_id=None):
    if not err:
        slack_app.client.files_upload(filename=host, content=whois_result, channels=channel_id)
    return {
        'statusCode': '400' if err else '200',
        'body': err if err else None,
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context): 
    decoded_body = b64decode(event['body'])
    params = parse_qs(decoded_body)
    token = params[b'token'][0].decode('utf8')
    if token != EXPECTED_TOKEN:
        logger.error("Request token does not match expected")
        return respond(err="Request token does not match expected")

    if b'text' in params:
        host = params[b'text'][0].decode('utf8')
    else:
        return respond(err="No whois host provided")

    channel_id = params[b'channel_id'][0].decode('utf8')

    whois_result = whois.whois(host, raw=True)

    title_template = [
        {
            "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f":mag: Whois result for {host}",
                        "emoji": True
                    }
        }
    ]

    payload = {
        "response_type": "in_channel",
        "blocks": json.dumps(title_template)
    }

    return respond(None, host=host, whois_result=whois_result, channel_id=channel_id)
