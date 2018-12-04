import boto3
import json
import os
import urllib
import logging
from utils import find_appliance, disconnect_appliance


# Get the table name from the Lambda Environment Variable
table_name = os.environ['APPLIANCE_TABLE_NAME']

# Initialize S3 and DynamoDB client
s3_client = boto3.client('s3')
dynamo_client = boto3.resource('dynamodb').Table(table_name)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# --------------- Main Handler ---------------
def lambda_handler(event, context):
    '''
        Extracts appliance information and persists them into DynamoDB.
        '''

    try:
        # Get the object from the event.
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

        obj = s3_client.get_object(Bucket=bucket, Key=key)
        body = json.loads(obj['Body'].read())

        event, payload = body["event"], body["payload"]

        # Extract appliance information
        appliance_id = payload["applianceId"]

        # Check appliance existence
        appliance = find_appliance(client=dynamo_client, appliance_id=appliance_id)
        if appliance:
            disconnect_appliance(client=dynamo_client, appliance_id=appliance_id)
        else:
            logger.warn('Appliance with id {} could not be found.'.format(appliance_id))

    except Exception as e:
        logging.error("Error processing object {} from bucket {}. Exception {}".format(key, bucket, e))
        return 'Failure'