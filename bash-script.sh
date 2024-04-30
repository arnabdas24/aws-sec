#!/bin/bash
set -e
TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`
instance_id=`curl -H "X-aws-ec2-metadata-token: $TOKEN" -v http://169.254.169.254/latest/meta-data/instance-id`
volume_id=`/usr/local/bin/aws ec2 describe-volumes --filters Name=attachment.instance-id,Values=$instance_id Name=attachment.device,Values=/dev/sdf | jq -r .Volumes[0].Attachments[0] | jq --raw-output .VolumeId`
mkdir -p /root/forensic
mkdir -p /root/forensic/execution_logs
log_location=/root/forensic/execution_logs/script_execution_log_$volume_id.log
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>$log_location 2>&1


devicename=nvme1n1
blockname=$(lsblk --output NAME | grep -o nvme1n1 | head -n 1)
if [ "$blockname" == "$devicename" ]
then
echo "..................... Starting the Workflow ............................"
crontab -r
mkdir -p /root/.aws/
touch config /root/.aws
tee -a /root/.aws/config << END
[profile forensic]
role_arn=arn:aws-cn:iam::$EVIDENCEBUCKET_ACCOUNT:role/S3CrossAccountRole
credential_source=Ec2InstanceMetadata
END
tee  /tmp/message.txt << END
Hi Team,
Evidence Collection has been completed for volume_id:-$volume_id of compromised instance:-   $INSTANCE_ID which belongs to aws_account:-$ACCOUNT_NO , SNOW_ID:-$TICKET_DETAILS.No of volumes attached to the instance is/are $VOLNUMBER , Once you receive total $VOLNUMBER SNS
then only you can go to s3 bucket to verify the logs
END

/usr/local/bin/aws s3 cp s3://$S3_IR/rpms/dc3dd.rpm /tmp/
yum install /tmp/dc3dd.rpm -y
echo "....................................Starting the dd image Creation.................................."
sudo dc3dd if=/dev/nvme1n1 hash=sha512 log=/root/forensic/$volume_id.log of=/root/forensic/$volume_id.dd verb=on
echo ".....................................Copying the dd image and log files to forensic account's s3 bucket.............................."
/usr/local/bin/aws s3 cp /root/forensic/*.log s3://$DESTINATION_BUCKET/$TICKET_DETAILS/Account-$ACCOUNT_NO/Compromised-InstanceID-$INSTANCE_ID/ --profile forensic
/usr/local/bin/aws s3 cp /root/forensic/*.dd s3://$DESTINATION_BUCKET/$TICKET_DETAILS/Account-$ACCOUNT_NO/Compromised-InstanceID-$INSTANCE_ID/  --profile forensic
sleep 10
/usr/local/bin/aws s3 cp $log_location s3://$DESTINATION_BUCKET/$TICKET_DETAILS/Account-$ACCOUNT_NO/Compromised-InstanceID-$INSTANCE_ID/ --profile forensic

/usr/local/bin/aws sns publish --topic-arn $SNS_ARN --subject "Disc Evidence Collection of  $TICKET_DETAILS" --message file:///tmp/message.txt
echo "........................The evidence collection was successful , terminating the instance............................."
sleep 60
sudo init 0
fi
