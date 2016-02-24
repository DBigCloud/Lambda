import boto3
import sys

try:
    ec2 = boto3.client('ec2')

except Exception, e1:
    error1 = "Error1: %s" % str(e1)
    print(error1)
    sys.exit(0)

id_instance = 'xxxxxxx'

def check_instance_status(id):
    try:
        return ec2.describe_instance_status(
            InstanceIds = [id]
         )
    except Exception, e2:
        error2 = "Error2: %s" % str(e2)
        print(error2)
        sys.exit(0)

def stopInstance(id):
    print "++++++++++++++++++"
    print "Stopping instance"
    print "++++++++++++++++++"
    try:
         ec2.stop_instances(
            InstanceIds = [id]
         )
    except Exception, e2:
        error2 = "Error2: %s" % str(e2)
        print(error2)
        sys.exit(0)

def lambda_handler(event, context):
    status = check_instance_status(id_instance)
    for stat in status['InstanceStatuses']:
        if stat['InstanceState']['Name'] != 'stopped' :
            stopInstance(id_instance)
        else:
            print 'Instancia con id: ' + id_instance + ' apagada, no es necesario volverla a apagar'