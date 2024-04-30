import boto3
import os
import uuid
import time

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    ForensicVolumeID = []
    for voldata in event['Final_Snap_to_Volume_Mapping']:
        ForensicVolumeID.append(voldata['VolumeID'])
    ForensicInstances = event['ForensicInstances']
    if event['VolumeNos']==1:
        vol = ec2.attach_volume(
            Device='/dev/sdf',
            InstanceId=ForensicInstances[0],
            VolumeId=ForensicVolumeID[0]
            )
    if event['VolumeNos']==2:
        vol_1 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[0],
        VolumeId=ForensicVolumeID[0]
        )
        vol_2 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[1],
        VolumeId=ForensicVolumeID[1]
        )
    if event['VolumeNos']==3:
        vol_3 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[0],
        VolumeId=ForensicVolumeID[0]
        )
        vol_4 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[1],
        VolumeId=ForensicVolumeID[1]
        )
        vol_5 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[2],
        VolumeId=ForensicVolumeID[2]
        )
    if event['VolumeNos']==4:
        vol_6 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[0],
        VolumeId=ForensicVolumeID[0]
        )
        vol_7 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[1],
        VolumeId=ForensicVolumeID[1]
        )
        vol_8 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[2],
        VolumeId=ForensicVolumeID[2]
        )
        vol_9 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[3],
        VolumeId=ForensicVolumeID[3]
        )
    if event['VolumeNos']==5:
        vol_10 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[0],
        VolumeId=ForensicVolumeID[0]
        )
        vol_11 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[1],
        VolumeId=ForensicVolumeID[1]
        )
        vol_12 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[2],
        VolumeId=ForensicVolumeID[2]
        )
        vol_13 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[3],
        VolumeId=ForensicVolumeID[3]
        )
        vol_14 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[4],
        VolumeId=ForensicVolumeID[4]
        )
    if event['VolumeNos']==6:
        vol_15 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[0],
        VolumeId=ForensicVolumeID[0]
        )
        vol_16 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[1],
        VolumeId=ForensicVolumeID[1]
        )
        vol_17 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[2],
        VolumeId=ForensicVolumeID[2]
        )
        vol_18 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[3],
        VolumeId=ForensicVolumeID[3]
        )
        vol_19 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[4],
        VolumeId=ForensicVolumeID[4]
        )
        vol_19 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[5],
        VolumeId=ForensicVolumeID[5]
        )
    if event['VolumeNos']==7:
        vol_15 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[0],
        VolumeId=ForensicVolumeID[0]
        )
        vol_16 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[1],
        VolumeId=ForensicVolumeID[1]
        )
        vol_17 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[2],
        VolumeId=ForensicVolumeID[2]
        )
        vol_18 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[3],
        VolumeId=ForensicVolumeID[3]
        )
        vol_19 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[4],
        VolumeId=ForensicVolumeID[4]
        )
        vol_19 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[5],
        VolumeId=ForensicVolumeID[5]
        )
        vol_20 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[6],
        VolumeId=ForensicVolumeID[6]
        )
    if event['VolumeNos']==8:
        vol_15 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[0],
        VolumeId=ForensicVolumeID[0]
        )
        vol_16 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[1],
        VolumeId=ForensicVolumeID[1]
        )
        vol_17 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[2],
        VolumeId=ForensicVolumeID[2]
        )
        vol_18 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[3],
        VolumeId=ForensicVolumeID[3]
        )
        vol_19 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[4],
        VolumeId=ForensicVolumeID[4]
        )
        vol_19 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[5],
        VolumeId=ForensicVolumeID[5]
        )
        vol_20 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[6],
        VolumeId=ForensicVolumeID[6]
        )
        vol_20 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[7],
        VolumeId=ForensicVolumeID[7]
        )
    if event['VolumeNos']==9:
        vol_15 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[0],
        VolumeId=ForensicVolumeID[0]
        )
        vol_16 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[1],
        VolumeId=ForensicVolumeID[1]
        )
        vol_17 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[2],
        VolumeId=ForensicVolumeID[2]
        )
        vol_18 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[3],
        VolumeId=ForensicVolumeID[3]
        )
        vol_19 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[4],
        VolumeId=ForensicVolumeID[4]
        )
        vol_19 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[5],
        VolumeId=ForensicVolumeID[5]
        )
        vol_20 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[6],
        VolumeId=ForensicVolumeID[6]
        )
        vol_20 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[7],
        VolumeId=ForensicVolumeID[7]
        )
        vol_21 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[8],
        VolumeId=ForensicVolumeID[8]
        )
    if event['VolumeNos']==10:
        vol_15 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[0],
        VolumeId=ForensicVolumeID[0]
        )
        vol_16 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[1],
        VolumeId=ForensicVolumeID[1]
        )
        vol_17 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[2],
        VolumeId=ForensicVolumeID[2]
        )
        vol_18 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[3],
        VolumeId=ForensicVolumeID[3]
        )
        vol_19 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[4],
        VolumeId=ForensicVolumeID[4]
        )
        vol_19 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[5],
        VolumeId=ForensicVolumeID[5]
        )
        vol_20 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[6],
        VolumeId=ForensicVolumeID[6]
        )
        vol_20 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[7],
        VolumeId=ForensicVolumeID[7]
        )
        vol_21 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[8],
        VolumeId=ForensicVolumeID[8]
        )
        vol_22 = ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=ForensicInstances[9],
        VolumeId=ForensicVolumeID[9]
        )
    return event
