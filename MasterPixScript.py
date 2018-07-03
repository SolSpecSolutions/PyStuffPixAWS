#!/usr/bin/env python

#Import libraries
import boto3
import subprocess
import time
import paramiko
from scp import SCPClient

#Variables
s3In = raw_input("Enter full Project path: ")
key = paramiko.RSAKey.from_private_key_file("/home/ubuntu/Documents/Pix4DProcessingServers.pem")
conn = paramiko.SSHClient()
conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
user = "ubuntu"
lclPath = '/home/ubuntu/Documents/Scripts/'
#script1 = 'LS_NoGeoFile_PixScript_v2.0.sh'
#script2 = 'LS_GeoFile_PixScript_v2.0.sh'
remPath = '/home/ubuntu/pix4d/'
#commands = ["echo $PATH", "cat /etc/fstab"]

#Determine which script to use - drone or waldo
if "drone" in s3In:
	script = 'LS_NoGeoFile_PixScript_v2.1.sh'
elif "waldo" in s3In:
	script = 'LS_GeoFile_PixScript_v2.1.sh'
else:
	print("Project path is not correct. Please use correct Drone or Waldo folder path.")
	exit(1)

#Query AWS for all available Processing server (by Role tag and state code = 80 - stopped)
ec2 = boto3.resource('ec2')
instances = ec2.instances.filter(
    Filters=[
        {'Name': 'tag:Role', 'Values': ['ProcessingTest']},
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

#commands = {"sudo chmod +x " "{0}{1}".format(remPath, script),
#            "{0}{1} {2} {3} {4} {5}".format(remPath, script, s3In, inst, script, serverName)}

print("Starting server " + serverName)
subprocess.call(['aws', 'ec2', 'start-instances', '--instance-ids', inst])

#Wait 2 mins for server to start - rewrite to loop through state code until "running"
print("Waiting 2 mins for server to start")
time.sleep(120)

conn.connect(hostname = instDNSName, username = user, pkey = key)
print("Copying local processing scripts to remote server")
with SCPClient(conn.get_transport()) as scp:
    scp.put(lclPath + script, remPath + script)
    #scp.put(lclPath + script2, remPath + script2)

print("Make local script executable")
print("Executing {}".format("sudo chmod +x " "{0}{1}".format(remPath, script)))
stdin, stdout, stderr = conn.exec_command("sudo chmod +x " "{0}{1}".format(remPath, script))
print stdout.read()
print("Errors")
print stderr.read()

print("Executing script on remote Pix server")
print("Executing {}".format("{0}{1} {2} {3} {4} {5}".format(remPath, script, s3In, inst, script, serverName)))
stdin, stdout, stderr = conn.exec_command("{0}{1} {2} {3} {4} {5}".format(remPath, script, s3In, inst, script, serverName))
print stdout.read()
print("Errors")
print stderr.read()

#for command in commands:
#    print "Executing {}".format(command)
#    stdin, stdout, stderr = conn.exec_command(command)
#    print stdout.read()
#    print("Errors")
#    print stderr.read()
conn.close()
exit(0)

