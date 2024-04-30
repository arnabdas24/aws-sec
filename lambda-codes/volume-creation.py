import boto3
import os
from datetime import date

encryptionKey = os.environ['KMS_KEY']
supported_az = os.environ['SUPPORTED_AZS']
def lambda_handler(event, context):
    event['Final_Snap_to_Volume_Mapping'] = []
    today_date=date.today()
    instanceID = event['compromised_instance_id']
    ec2 = boto3.client('ec2')
    for snap_id in event['Snapshot_Ids_Mapping']:
        response = ec2.create_volume(
        SnapshotId=snap_id['FinalSnapshotID'],
        Iops=3000,
        VolumeType='gp3',
        Encrypted=True,
        AvailabilityZone = supported_az,
        KmsKeyId=encryptionKey,
        TagSpecifications=[
                {
                    "ResourceType": "volume",
                    "Tags": [
                        {
                            'Key': 'Name',
                            'Value': 'Forensic Volume of instance {}'.format(instanceID)
                        },
                        {
                            'Key': 'SourceInstanceID',
                            'Value': event['compromised_instance_id']
                        },
                        {
                            'Key': 'Volume_Creation_Date',
                            'Value': f'{today_date}'
                        },
                        {
                            'Key': 'Volumetype',
                            'Value': 'Forensic_Volume'
                        },
                        {
                            'Key': 'SourceAccount',
                            'Value': event['account_no']
                        },
                    ]
                }
            ])
        event['Final_Snap_to_Volume_Mapping'].append({'FinalSnapshotID': response['SnapshotId'],'VolumeID': response['VolumeId']})
    return event
