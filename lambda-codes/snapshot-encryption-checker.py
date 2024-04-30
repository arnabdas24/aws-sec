import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2',region_name="cn-north-1")
    snaps = []
    for snapid in event['Snapshot_Ids_Mapping']:
        snaps.append(snapid['FinalSnapshotID'])
    response = ec2.describe_snapshots(SnapshotIds=snaps)
    for item in response['Snapshots']:
        if item['State'] == 'pending':
            raise RuntimeError("Copying snapshot with KMS key is still not finished")
        elif item['State'] == 'error':
            raise Exception("Snapshot {} errored".format(item['SnapshotId']))
    print("Snaps have been completed")
    return event
