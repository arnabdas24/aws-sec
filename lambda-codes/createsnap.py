import boto3
from datetime import date

def lambda_handler(event, context):
    account_no=event["account_no"]
    compromised_instance_id=event["compromised_instance_id"]
    ticket_details=event['ticket_details']
    
    #### assuming the role to the compromsied account #####

    sts_connection = boto3.client('sts')
    secondary_account = sts_connection.assume_role(
        RoleArn=f"arn:aws-cn:iam::{account_no}:role/LambdaAssumeRole",
        RoleSessionName="cross_account_lambda"
    )
    session=boto3.Session(aws_access_key_id=secondary_account['Credentials']['AccessKeyId'],
    aws_secret_access_key=secondary_account['Credentials']['SecretAccessKey'],aws_session_token=secondary_account['Credentials']['SessionToken'])
    ec2 = session.client('ec2',region_name="cn-north-1")
    print("Received request to create snapshots for instance {}".format(compromised_instance_id))
    response = ec2.describe_instances(InstanceIds=[compromised_instance_id])
    
    today_date=date.today()

    ec2_resource = session.resource('ec2',region_name="cn-north-1")
    instance = ec2_resource.Instance(f'{compromised_instance_id}')
    operating_system = instance.platform_details
    event['operating_system'] = operating_system
    for edx, tag in enumerate(instance.tags):
         if tag['Key'] == 'Name':
            compromised_instance_name = tag['Value']
            event['compromised_instance_name'] = compromised_instance_name
         else:
             print("No instance name found")

    Output = event
    Output['CapturedSnapshots'] = []
    volume_details=instance.volumes.all()
    print(volume_details)


    snaps = ec2.create_snapshots(
            Description="Automated Snapshot creation for compromised instance: {}".format(compromised_instance_id),
            InstanceSpecification={
                'InstanceId': compromised_instance_id,
                'ExcludeBootVolume': False
            }
        )
    for snap in snaps['Snapshots']:
        Output['CapturedSnapshots'].append({'SourceSnapshotID': snap['SnapshotId'], 
        'SourceVolumeID': snap['VolumeId'], 'VolumeSize': snap['VolumeSize'], 'InstanceID': compromised_instance_id})
    return Output
