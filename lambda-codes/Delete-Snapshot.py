import boto3
from datetime import datetime, timezone, date
from pprint import pp
import os
retention_days = int(os.environ['SNAPSHOT_RETENTION_DAYS'])

def lambda_handler(event, context):
    today_date = date.today()
    snapshot_to_be_deleted=[]
    client = boto3.client('ec2')
    response = client.describe_snapshots(Filters=[{'Name':'tag:Snapshot_type','Values': ['compromised_snapshot']}])
    for data in response['Snapshots']:
        for snaptime in (data['Tags']):
            if snaptime['Key'] == "Snapshot_copy_date": 
                formatted_date=datetime.strptime(snaptime['Value'],'%Y-%m-%d').date()
                if abs((today_date-formatted_date).days) > retention_days:
                    snapshot_to_be_deleted.append(data['SnapshotId'])
    for snap_del in snapshot_to_be_deleted:
        response = client.delete_snapshot(SnapshotId=snap_del)
        print(f"{snapshot_to_be_deleted} have been deleted successfully")
