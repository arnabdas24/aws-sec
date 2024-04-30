import boto3

def lambda_handler(event, context):
    
    instanceID = event['compromised_instance_id']
    account_no=event["account_no"]
    
    #### assuming the role to the compromsied account

    sts_connection = boto3.client('sts')
    secondary_account = sts_connection.assume_role(
        RoleArn=f"arn:aws-cn:iam::{account_no}:role/LambdaAssumeRole",
        RoleSessionName="cross_account_lambda"
    )
    session=boto3.Session(aws_access_key_id=secondary_account['Credentials']['AccessKeyId'],
    aws_secret_access_key=secondary_account['Credentials']['SecretAccessKey'],aws_session_token=secondary_account['Credentials']['SessionToken'])
    ec2 = session.client('ec2',region_name="cn-north-1")

    snaps = []
    for snapid in event['CapturedSnapshots']:
        snaps.append(snapid['SourceSnapshotID'])

    response = ec2.describe_snapshots(SnapshotIds=snaps)
    for item in response['Snapshots']:
            if item['State'] == 'pending':
                raise RuntimeError("Snapshots not finished")
            elif item['State'] == 'error':
                raise Exception("Snapshot {} errored".format(
                    item['SnapshotId']
                ))
        
    print("Snaps have completed")
    return event
