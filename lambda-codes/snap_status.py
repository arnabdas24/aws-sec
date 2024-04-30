import boto3
import os
from datetime import date

def lambda_handler(event, context):
    ec2 = boto3.client('ec2',region_name="cn-north-1")
    snaps = []
    for snapid in event['CapturedSnapshots']:
        snaps.append(snapid['SourceSnapshotID'])
    
    response = ec2.describe_snapshots(SnapshotIds=snaps)
    for item in response['Snapshots']:
        if item['State'] == 'pending':
            raise RuntimeError("Copying Snapshots to IR account is still not finished")
        elif item['State'] == 'error':
            raise Exception("Snapshot {} errored".format(item['SnapshotId']))
    print("Snaps have been completed")
    return event
