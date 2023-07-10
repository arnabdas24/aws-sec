# {
#   "id": "i-0424baa9a6f553984",
#   "region": "us-east-1",
#   "case-id": "3422123",
#   "evidence_bucket_name": "s3://mylambda-dev-us-east-1/",
#   "CapturedSnapshots": [
#     {
#       "SourceSnapshotID": "snap-000adfc2acb5876bc",
#       "SourceVolumeID": "vol-05e6c3eda63921090",
#       "SourceDeviceName": "/dev/xvda",
#       "VolumeSize": 8,
#       "InstanceID": "i-0424baa9a6f553984",
#       "FindingID": "3422123",
#       "Region": "us-east-1"
#     },
#     {
#       "SourceSnapshotID": "snap-0796d2b0fe6c5101f",
#       "SourceVolumeID": "vol-0fd49bc70c7faf965",
#       "SourceDeviceName": "/dev/sdf",
#       "VolumeSize": 15,
#       "InstanceID": "i-0424baa9a6f553984",
#       "FindingID": "3422123",
#       "Region": "us-east-1"
#     }
#   ]
# }


import boto3
import os
import uuid
import json

def lambda_handler(event, context):
        instanceID = event['id']
        region = event['region']
        findingID = event['case-id']
        snaps = []
        for snapshotID in event['CapturedSnapshots']:
            snaps.append(snapshotID['SourceSnapshotID'])

        s3 = boto3.client('s3')
        ec2 = boto3.client('ec2', region_name=region)

        print("Checking Status for snapshots {} in region {}".format(
            snaps,
            region
        ))
        response = ec2.describe_snapshots(
            SnapshotIds=snaps
        )
        for item in response['Snapshots']:
            if item['State'] == 'pending':
                raise RuntimeError("Snapshots not finished")
            elif item['State'] == 'error':
                raise Exception("Snapshot {} errored".format(
                    item['SnapshotId']
                ))
        
        print("Snaps have completed")
        return event
