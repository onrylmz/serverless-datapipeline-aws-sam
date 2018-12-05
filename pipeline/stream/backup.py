from thundra.thundra_agent import Thundra
import boto3
import os
import base64
import json
import logging


# Initialize S3 client
s3_client = boto3.client('s3')

# Get the bucket name from the Lambda Environment Variable
backup_bucket = os.environ['BACKUP_BUCKET']

# Initialize thundra
thundra = Thundra(api_key=os.environ['THUNDRA_KEY'])

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# --------------- Main Handler ---------------
@thundra
def lambda_handler(event, context):
    '''
    Emits kinesis stream to backup events in S3.
    '''

    try:
        for record in event['Records']:
            # Kinesis data is base64 encoded so decode here
            data = json.loads(base64.b64decode(record["kinesis"]["data"]))

            # Prepare file key i.e. appliance/[provisioned, connected, disconnected, ..]/{event_id}
            file_key = '{}/{}/{}'.format(
                data["event"]["source"].lower(),
                data["event"]["type"].lower(),
                record["eventID"]
            )

            # Upload the kinesis data to backup bucket
            s3_client.put_object(
                Body=json.dumps(data),
                Bucket=backup_bucket,
                Key=file_key
            )
            logging.info("File has been uploaded with key {}.".format(file_key))

        return 'Success'
    except Exception as e:
        logging.error("File could not be uploaded, {}".format(e))
        return 'Failure'