import json
import boto3
def lambda_handler(event, context):
    instanceID = event['id']
    region = event['region']
    ec2 = boto3.client('ec2','us-east-1')
    snapshot_complete_waiter = ec2.get_waiter('snapshot_completed')
    response = ec2.describe_instances(InstanceIds=[instanceID])
    Output = event
    Output['CapturedSnapshots'] = []
    snapwaiter=[]
    snaps = ec2.create_snapshots(
            Description="Automated Snapshot creation: ",
            InstanceSpecification={
                'InstanceId': instanceID,
                'ExcludeBootVolume': False
            }
        )
    for snap in snaps['Snapshots']:
        snapwaiter.append(snap['SnapshotId'])
    #for snap_data in snapwaiter:
    snapshot_complete_waiter.wait(SnapshotIds=snapwaiter)
