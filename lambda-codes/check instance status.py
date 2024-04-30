import boto3

def lambda_handler(event, context):
    client = boto3.client('ec2',region_name='cn-north-1')
    response = client.describe_instances(InstanceIds=event['ForensicInstances'])
    for data in response['Reservations']:
        for ins in data['Instances']:
            if ins['State']['Name'] != 'running':
                raise RuntimeError("Instances are not ready yet")
    else:
        print('Servers are ready')
    return event
