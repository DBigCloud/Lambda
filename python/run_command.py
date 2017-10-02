import boto3

client_ssm = boto3.client('ssm')

def lambda_handler(event, context):
    # INIT vars from lambda tags
    instanceid = event['INSTANCEID']
    environment = event['ENVIR']
    timeout = event['TIMEOUT']
    command_run = event['COMMAND']
    command_run = command_run + ' ' + environment + ' >> /opt/scripts/backups.log'
    ServiceRole = event['SERVICEROLE']
    description = "Example of command run from DBigCloud"

    try:
        command = client_ssm.send_command(InstanceIds=[instanceid], DocumentName='AWS-RunShellScript',
            Parameters={"commands" : [command_run], "executionTimeout" : [timeout]}, 
            TimeoutSeconds=30, Comment=description, ServiceRoleArn = ServiceRole
            )
        
        commandid = command['Command']['CommandId']
        response = client_ssm.list_commands(CommandId=commandid)
        
        for item in response['Commands']:
            status = item['Status']
            
         print "Command",commandid, "for provider", values['provider'],"was executed", status
        return "Success"
        
    except Exception as e:
        print "Error running ",e
