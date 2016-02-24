import boto3
import sys

try:
    ec2 = boto3.client('ec2')

except Exception, e1:
    error1 = "Error1: %s" % str(e1)
    print(error1)
    sys.exit(0)

id_instance = 'xxxxxxxx'

def check_instance_status(id):
    try:
        return ec2.describe_instance_status(
            InstanceIds = [id]
         )
    except Exception, e2:
        error2 = "Error2: %s" % str(e2)
        print(error2)
        sys.exit(0)

def startInstance(id):
    print "+++++++++++++++++++++++++++++++"
    print "Starting instance "+ id
    print "+++++++++++++++++++++++++++++++"
    try:
         ec2.start_instances(
            InstanceIds = [id]
         )
    except Exception, e2:
        error2 = "Error2: %s" % str(e2)
        print(error2)
        sys.exit(0)

def lambda_handler(event, context):
    status = check_instance_status(id_instance)
    if not status['InstanceStatuses'] :
        startInstance(id_instance)
    else:
        for stat in status['InstanceStatuses']:
            if stat['InstanceState']['Name'] != 'running' :
                startInstance(id_instance)
            else:
                print 'Instancia con id: ' + id_instance + ' encendida, no es necesario volverla a encender'