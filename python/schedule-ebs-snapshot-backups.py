############################################################################################################################
#### The first version of this script was read in http://serverlesscode.com/post/lambda-schedule-ebs-snapshot-backups/ #####
############################################################################################################################
import boto3
from datetime import date

#Return dateBackup
BackupDate = date.today()
ec = boto3.client('ec2')

#Return TagName Value
def TagName(i):
    for tag in i:
        if tag[u'Key']=='Name':
            return tag[u'Value']

def lambda_handler(event,context):
    reservations = ec.describe_instances(
            Filters=[
                {'Name': 'tag-key', 'Values': ['backup', 'Backup']},
            ]
        )['Reservations']
    
    instances = sum(
        [
            [i for i in r['Instances']]
            for r in reservations
        ], [])

    for instance in instances:
        InstanceName=TagName(instance['Tags'])
        for dev in instance['BlockDeviceMappings']:
            if dev.get('Ebs', None) is None:
                # skip non-EBS volumes
                continue
            vol_id = dev['Ebs']['VolumeId']
            print "Found EBS volume %s on instance %s" % (
                vol_id, instance['InstanceId'])
            #Create Snapshot
            ec.create_snapshot(
                VolumeId=vol_id,
                Description='Backup done '+ str(BackupDate) +' Instance ' + InstanceName + ' : ' + instance['InstanceId']
            )
