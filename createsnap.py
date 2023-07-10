import json
import boto3
import os
def lambda_handler(event, context):
    instanceID = event['id']
    region = event['region']
    findingID = event['case-id']
    event['evidence_bucket_name'] = "s3://mylambda-dev-us-east-1/"
    ec2 = boto3.client('ec2','us-east-1')
    print("Received request to create snapshots for instance {} in region {}".format(instanceID,region))
    response = ec2.describe_instances(InstanceIds=[instanceID])
    Output = event
    Output['CapturedSnapshots'] = []
    for res in response['Reservations']:
            for item in res['Instances']:
                for vol in item['BlockDeviceMappings']:
                    if vol['Ebs']['Status'] == 'attached':
                        # create snapshot
                        print("Initiating snapshot creation for volume {} on instance {} in region {}".format(
                            vol['Ebs']['VolumeId'],
                            instanceID,
                            region
                        ))

                        snap = ec2.create_snapshot(
                            Description="Automated Snapshot creation: {}".format(findingID),
                            VolumeId=vol['Ebs']['VolumeId'],
                            TagSpecifications=[
                                {
                                    'ResourceType': 'snapshot',
                                    'Tags': [
                                        {
                                            'Key': 'Name',
                                            'Value': 'Forensic Automated Snapshot creation - ' + instanceID
                                        },
                                        {
                                            'Key': 'CompromisedInstanceID',
                                            'Value': instanceID
                                        },
                                        {
                                            'Key': 'SourceVolumeID',
                                            'Value': vol['Ebs']['VolumeId']
                                        },
                                        {
                                            'Key': 'FindingID',
                                            'Value': findingID
                                        },
                                        {
                                            'Key': 'SourceDeviceName',
                                            'Value': vol['DeviceName']
                                        }
                                    ]
                                }
                            ]
                        )
                        Output['CapturedSnapshots'].append({'SourceSnapshotID': snap['SnapshotId'], 
                            'SourceVolumeID': snap['VolumeId'], 'SourceDeviceName': vol['DeviceName'], 
                             'VolumeSize': snap['VolumeSize'], 'InstanceID': instanceID, 
                             'FindingID': findingID, 'Region': region})
    return Output


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
