from logging import Logger
import boto3
import json
import os
from base64 import b64decode
from urllib.parse import parse_qs

from secret_man import get_secret

EXPECTED_TOKEN = json.loads(get_secret(os.environ.get('slack_verify_secret_name')))[
    os.environ.get('slack_verify_secret_key')]

lambda_client = boto3.client('lambda')

def lambda_handler(event,context):
  decoded_body = b64decode(event['body'])
  params = parse_qs(decoded_body)
  token = params[b'token'][0].decode('utf8')
  slash_command = params[b'command'][0].decode('utf8')

  if token != EXPECTED_TOKEN:
    Logger.error("Request token does not match expected")
    return respond(err="Request token does not match expected")
  
  if slash_command == "/whois":
    arn = os.environ.get('whois_lambda_arn')
  else:
    return respond(err="No command")

  invoke_lambda(arn)


def invoke_lambda(arn, params):
  response = lambda_client.invoke(
    FunctionName = arn,
    InvocationType = 'Event',
    Payload = json.dumps(params)
  )


def respond():
  pass