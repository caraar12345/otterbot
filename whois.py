import json
import logging
import os
from base64 import b64decode
from urllib.parse import parse_qs
from slack_bolt import App
from slack_sdk.oauth.state_store import file
from python_whois.whois import whois
from secret_man import get_secret

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

def respond(err, payload=None):
    return {
                'statusCode': '400' if err else '200',
                'body': err if err else json.dumps(payload).encode('utf8'),
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
    slack_app.client.conversations_join(channel=channel_id)
    file_info = slack_app.client.files_upload(title=host, content=whois_result)['file']
    file_link = file_info['permalink']
    print(file_info)

    msg_template = [
        {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"*Whois result for {host}* <{file_link}|this should be the file link>"
			}
		}
    ]

    payload = {
        "response_type": "in_channel",
        "blocks": json.dumps(msg_template),
        "unfurl_links": True
    }

    return respond(None, payload=payload)
