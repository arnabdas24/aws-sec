import boto3
import os
from datetime import date
encryption_key = os.environ['KMS_KEY']
source_region = os.environ['SOURCE_REGION']

def lambda_handler(event, context):
    instanceID = event['compromised_instance_id']
    ec2 = boto3.client('ec2',region_name="cn-north-1")
    today_date=date.today()
    event['Snapshot_Ids_Mapping'] = []
    snap_details=[]
    for data in event['CapturedSnapshots']:
        snap_details.append(data['SourceSnapshotID'])
    for snap_final in snap_details:
        response = ec2.copy_snapshot(
        Description="Forensic Copy Automated Snapshot creation of Instance {}".format(instanceID),
        Encrypted = True,
        KmsKeyId = encryption_key,
        SourceSnapshotId = snap_final,
        SourceRegion = source_region,
        TagSpecifications = [
            {
                'ResourceType': 'snapshot',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'Automated_Snapshot_of_Compromised_Instance: {}'.format(instanceID)
                    },
                    {
                        'Key': 'Compromised_original_instance_id',
                        'Value': event['compromised_instance_id']
                    },
                    {
                        'Key': 'Compromised_original_instance_os',
                        'Value': event['operating_system']
                    },
                    {
                        'Key': 'Source_Account',
                        'Value' : event['account_no']
                    },
                    {
                        'Key': 'Snapshot_copy_date',
                        'Value' : f'{today_date}'
                    },
                    {
                        'Key': 'Snapshot_type',
                        'Value' : 'compromised_snapshot'
                    }
                 ]
            }
        ])
        event['Snapshot_Ids_Mapping'].append(({'FinalSnapshotID': response['SnapshotId'],'SourceSnapshotID': snap_final}))
    return event
