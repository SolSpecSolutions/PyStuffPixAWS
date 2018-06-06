#!/usr/bin/python2.7
#Import libraries
import boto3
import subprocess
import time
import paramiko
from scp import SCPClient

#Variables
s3In = raw_input("Enter full Project path: ")
key = paramiko.RSAKey.from_private_key_file("E:\SolSpec\jmooreh\Documents\AWS\PEM\Pix4DProcessingServers.pem")
conn = paramiko.SSHClient()
conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
user = "ubuntu"
lclPath = s\\'E:\\SolSpec\\jmooreh\\Documents\\GitHub\\Scripts\\Bash\\ProcessingScript'
script1 = 'LS_NoGeoFile_PixScript_v2.0.sh'
script2 = 'LS_GeoFile_PixScript_v2.0.sh'
remPath = '/home/ubuntu/pix4d/'
#commands = ["echo $PATH", "cat /etc/fstab"]

#Query AWS for all available Processing server (by Role tag and state code = 80 - stopped)
ec2 = boto3.resource('ec2')
instances = ec2.instances.filter(
    Filters=[
        {'Name': 'tag:Role', 'Values': ['ProcessingTestJohn']},
        {'Name': 'instance-state-code', 'Values': ['80']}
    ]
)

#Read variable into a list (should be able to query servers directly into list)
available = []
for instance in instances:
    available.append(instance)

#Verify list isn't empty and set the Instance variable to first server in the list
if len(available) == 0:
    print("No servers are available at this time")
    exit(1)
else:
    server = available[0] #This variable allows it to be using in the local processing script
    inst = server.instance_id
    instDNSName = server.private_dns_name
    for tag in server.tags:
        if 'ServerName' in tag['Key']:
            serverName = tag['Value']
            #print(serverName)
    connStr = "ubuntu@" + instDNSName

commands = {"sudo chmod +x " "{0}{1}".format(remPath, script1), "sudo chmod +x " "{0}{1}".format(remPath, script2),
            "{0}{1} {2} {3} {4} {5}".format(remPath, script1, s3In, inst, script1, serverName)}

print("Starting server " + serverName)
subprocess.call(['aws', 'ec2', 'start-instances', '--instance-ids', inst])

#Wait 2 mins for server to start - rewrite to loop through state code until "running"
print("Waiting 2 mins for server to start")
time.sleep(120)

conn.connect(hostname = instDNSName, username = user, pkey = key)
print("Copying local processing scripts to remote server")
with SCPClient(conn.get_transport()) as scp:
    scp.put(lclPath + script1, remPath + script1)
    scp.put(lclPath + script2, remPath + script2)

for command in commands:
    print "Executing {}".format(command)
    stdin, stdout, stderr = conn.exec_command(command)
    print stdout.read()
    print("Errors")
    print stderr.read()
conn.close()

