import boto3
import os
number_of_volumes = os.environ['NO_OF_VOLUMES']

def lambda_handler(event, context):
    account_no=event["account_no"]
    compromised_instance_id=event["compromised_instance_id"]
    instance_id=[event["compromised_instance_id"]]
    
    #### assuming the role to the compromsied account #####

    sts_connection = boto3.client('sts')
    secondary_account = sts_connection.assume_role(
        RoleArn=f"arn:aws-cn:iam::{account_no}:role/LambdaAssumeRole",
        RoleSessionName="cross_account_lambda"
    )
    session=boto3.Session(aws_access_key_id=secondary_account['Credentials']['AccessKeyId'],
    aws_secret_access_key=secondary_account['Credentials']['SecretAccessKey'],aws_session_token=secondary_account['Credentials']['SessionToken'])
    ec2 = session.resource('ec2',region_name="cn-north-1")
    instance = ec2.Instance(compromised_instance_id)
    volume_id_list = [v.id for v in instance.volumes.all()]
    received_length = len(volume_id_list)
    if len(volume_id_list) > 10:
        raise RuntimeError(f"received {received_length} volumes which is greater than {number_of_volumes}")
    else:
        print("Continue with the process")
    event['VolumeNos'] = received_length


    volume_key = [v.kms_key_id for v in instance.volumes.all()]
    client = session.client('kms',region_name="cn-north-1")
    for customkey in volume_key:
        kms_response = [client.describe_key(KeyId=customkey)]
        for data_kms in kms_response:
            kms_owner=(data_kms['KeyMetadata']['KeyManager'])
        print(kms_owner)
        if 'AWS' in kms_owner:
            raise RuntimeError('All Volumes are not encrypted with CMK keys')
    else:
        ("Continue")

    return event
