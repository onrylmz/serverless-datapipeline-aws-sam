# -*- coding: utf-8 -*-
from __future__ import print_function
import boto3
import sys
import json


kinesis_client = boto3.client('kinesis')
stream_name = 'sample-eesd-kinesis-stream'

def read_test_file(event_type):
    with open('./tests/{}.json'.format(event_type), 'r') as f:
        data = json.load(f)

    return data

def main(event_type):

    data = read_test_file(event_type)

    records = []
    for i in range(1):
        data["payload"]["applianceId"] = 'A{:>9}'.format(i).replace(' ', '0')
        records.append({
            'Data': json.dumps(data),
            'PartitionKey': '{}'.format(event_type)
        })

    kinesis_client.put_records(
        Records=records,
        StreamName=stream_name
    )


if __name__ == '__main__':
    # Provide requested event in parameters i.e python test_kinesis.py provisioned connected disconnected
    events = sys.argv[1:]

    for e in events:
        getattr(sys.modules[__name__], 'main')(e)

    exit(0)
