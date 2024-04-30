import boto3
import os
import uuid
import random
import urllib3
import json


AMI_ID = os.environ['AMI_ID']
instanceProfile = os.environ['INSTANCE_PROFILE_NAME']
targetVPC = os.environ['VPC_ID']
securityGroup = os.environ['SECURITY_GROUP']
EvidenceBucket = os.environ['EVIDENCE_BUCKET']
EvidencebucketS3account = os.environ['S3EVIDENCE_ACCOUNT']
SubnetID = os.environ['EC2_SUBNET']
KeyPair = os.environ['KEYPAIR']
instance_type = os.environ['INSTANCE_TYPE']
ir_bucket = os.environ['IR_BUCKET']
sns_notification = os.environ['SNS_NOTIFICATION_ARN']

#ami_url = os.environ['AMI_URL']
    # http = urllib3.PoolManager()
    # resp = http.request("GET", f"{ami_url}")
    # final_response = resp.data
    # json_response = eval(json.loads(final_response.decode('utf-8'))['ami_ids'])
    # AMI_ID = json_response['cn-north-1']
    # print(AMI_ID)

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    INSTANCE_ID = event['compromised_instance_id']
    ACCOUNT_NO = event['account_no']
    TICKET_DETAILS=event['ticket_details']
    VOL_NOS=event['VolumeNos']
    emp=[]
    for data in event['CapturedSnapshots']:
        emp.append(data['VolumeSize'])
    max_storage=max(emp)
    if max_storage < 20:
         required_storage=40
    else:
         required_storage = max_storage+50

    userData = f"""#!/bin/bash\n
    echo DESTINATION_BUCKET={EvidenceBucket} >> /etc/environment
    echo INSTANCE_ID={INSTANCE_ID} >> /etc/environment
    echo TICKET_DETAILS={TICKET_DETAILS} >> /etc/environment
    echo VOLNUMBER={VOL_NOS} >> /etc/environment
    echo ACCOUNT_NO={ACCOUNT_NO} >> /etc/environment
    echo S3_IR={ir_bucket} >> /etc/environment
    echo SNS_ARN={sns_notification} >> /etc/environment
    echo EVIDENCEBUCKET_ACCOUNT={EvidencebucketS3account} >> /etc/environment
    /usr/local/bin/aws s3 cp s3://{ir_bucket}/cloudwatch_config/cloudwatchConfig.json /opt/aws/amazon-cloudwatch-agent/bin/
    sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/opt/aws/amazon-cloudwatch-agent/bin/cloudwatchConfig.json -s
    yum install unzip -y
    yum install jq -y
    aws s3 cp s3://{ir_bucket}/script/forensic.sh /root/
    chmod +x /root/forensic.sh
    crontab -l > mycron
    echo "* * * * * /root/forensic.sh" >> mycron
    crontab mycron
    """
    response = ec2.run_instances(
        BlockDeviceMappings=[
              {
            'DeviceName': '/dev/sda1',
            'Ebs': {
                'DeleteOnTermination': True,
                'VolumeSize': required_storage,
                'Encrypted': True,
                'Iops': 3000,
                'Throughput': 150,
                'VolumeType': 'gp3'
            },

            },
        ],
        ImageId=AMI_ID,
        InstanceType=instance_type,
        MaxCount = event['VolumeNos'],
        MinCount = event['VolumeNos'],
        SecurityGroupIds = [securityGroup],
        SubnetId = SubnetID,
        UserData=userData,
        KeyName=KeyPair,
        EbsOptimized=True,
        IamInstanceProfile={'Name': instanceProfile},
        InstanceInitiatedShutdownBehavior='terminate',
        TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'Forensic-instance'
                        },
                        {
                            'Key': 'Instance_type',
                            'Value': 'forensic_instance'
                        },
                    ]
                },
            ],
    )
    event['ForensicInstances'] = []
    for item in response['Instances']:
            event['ForensicInstances'].append(item['InstanceId'])
    return event
