import boto3
from datetime import datetime, timezone
import os

volume_retention = int(os.environ['VOLUME_RETENTION_HOURS'])

def lambda_handler(event, context):
    now = datetime.now(timezone.utc)
    client = boto3.client('ec2')
    vol_deleted=[]
    response = client.describe_volumes()
    for data in response['Volumes']:
        vol_create_time=(data['CreateTime'])
        time_difference=int(((now-vol_create_time).total_seconds())/3600)

        status=data['State']
        for vol_a in range(len(data['Tags'])):
            if data['Tags'][vol_a]['Value']=='Forensic_Volume' and status != 'in-use' and status != 'creating' and time_difference>volume_retention:
                new_data=data['VolumeId']
                vol_deleted.append(new_data)
    else:
        print('No Volume to be deleted')
    for vol_del in vol_deleted:
        client.delete_volume(VolumeId=vol_del)
        print(f"{vol_del} has been deleted")
