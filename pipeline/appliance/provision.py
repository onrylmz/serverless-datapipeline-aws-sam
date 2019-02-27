from utils import find_appliance, create_appliance, update_appliance
from thundra.thundra_agent import Thundra
import boto3
import json
import os
import urllib
import logging


# Get the table name from the Lambda Environment Variable
table_name = os.environ['APPLIANCE_TABLE_NAME']

# Initialize S3 and DynamoDB client
s3_client = boto3.client('s3')
dynamo_client = boto3.resource('dynamodb').Table(table_name)

# Initialize thundra
thundra = Thundra(api_key=os.environ['THUNDRA_KEY'])

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# --------------- Main Handler ---------------
@thundra
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
        purpose = payload["purpose"]
        model = payload["model"]
        appliance_type = payload["type"]
        brand = payload["brand"]

        # Check appliance existence
        appliance = find_appliance(client=dynamo_client, appliance_id=appliance_id)
        if appliance:
            update_appliance(client=dynamo_client, appliance_id=appliance_id)
            logger.info('Appliance {} already provisioned.'.format(appliance_id))
        else:
            create_appliance(
                client=dynamo_client,
                appliance_id=appliance_id,
                purpose=purpose,
                model=model,
                appliance_type=appliance_type,
                brand=brand
            )

        return 'Success'
    except Exception as e:
        logging.error("Error processing object {} from bucket {}. Exception {}".format(key, bucket, e))
        return 'Failure'
