from boto3.dynamodb.conditions import Key
import time
import datetime


def now():
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')

    return timestamp


def find_appliance(client, appliance_id):
    response = client.query(
        KeyConditionExpression=Key('id').eq(appliance_id)
    )

    return response['Items']


def create_appliance(client, appliance_id, purpose, model, appliance_type, brand):
    client.put_item(
        Item={
            'id': appliance_id,
            'applianceId': appliance_id,
            'purpose': purpose,
            'model': model,
            'type': appliance_type,
            'brand': brand,
            'connected': True,
            'createdAt': now(),
            'updatedAt': now()
        }
    )


def update_appliance(client, appliance_id):
    client.update_item(
        Key={
            'id': appliance_id
        },
        UpdateExpression='SET updatedAt= :now',
        ExpressionAttributeValues={
            ':now': now()
        }
    )


def disconnect_appliance(client, appliance_id):
    client.update_item(
        Key={
            'id': appliance_id
        },
        UpdateExpression='SET connected= :disconnect',
        ExpressionAttributeValues={
            ':disconnect': False
        }
    )