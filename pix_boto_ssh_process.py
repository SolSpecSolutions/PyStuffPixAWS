#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 12:31:53 2018

@author: michaelokonski
"""

import boto3
import paramiko
#import time
import os
import io
import pandas as pd

#To do......describe aws instances and lift all DNS from response

#Linux Server List. Add additional instances below and make sure to add to conditional below.
linux_1_private_dns = 'ip-172-31-47-242.us-west-2.compute.internal'
linux_2_private_dns = 'ip-172-31-46-248.us-west-2.compute.internal'
linux_3_private_dns = 'ip-172-31-45-161.us-west-2.compute.internal'
linux_4_private_dns = 'ip-172-31-47-73.us-west-2.compute.internal'
linux_5_private_dns = 'ip-172-31-45-185.us-west-2.compute.internal'
linux_6_private_dns = 'ip-172-31-42-27.us-west-2.compute.internal'
linux_7_private_dns = 'ip-172-31-40-20.us-west-2.compute.internal'
linux_8_private_dns = 'ip-172-31-46-54.us-west-2.compute.internal'
linux_9_private_dns = 'ip-172-31-40-175.us-west-2.compute.internal'
linux_10_private_dns = 'ip-172-31-33-58.us-west-2.compute.internal'
linux_11_private_dns = 'ip-172-31-46-249.us-west-2.compute.internal'
linux_12_private_dns = 'ip-172-31-35-228.us-west-2.compute.internal'
linux_13_private_dns = 'ip-172-31-46-124.us-west-2.compute.internal'
linux_14_private_dns = 'ip-172-31-37-229.us-west-2.compute.internal'
linux_15_private_dns = 'ip-172-31-33-1.us-west-2.compute.internal'
linux_16_private_dns = 'ip-172-31-33-1.us-west-2.compute.internal'
linux_17_private_dns = 'ip-172-31-34-193.us-west-2.compute.internal'
linux_18_private_dns = 'ip-172-31-41-135.us-west-2.compute.internaal'
linux_19_private_dns = 'ip-172-31-41-171.us-west-2.compute.internal'
linux_20_private_dns = 'ip-172-31-42-67.us-west-2.compute.internal'

linux_7_public_dns = 'ec2-54-244-133-194.us-west-2.compute.amazonaws.com'
linux_8_public_dns = 'ec2-54-186-251-208.us-west-2.compute.amazonaws.com'
linux_9_public_dns = 'ec2-54-212-234-43.us-west-2.compute.amazonaws.com'
linux_20_public_dns = 'ec2-54-214-222-14.us-west-2.compute.amazonaws.com'

#Choose server
pix_server = raw_input('Enter a server number between 1 and 20: ')

if pix_server == '1':
    selected_server = linux_1_private_dns
elif pix_server == '2':
    selected_server = linux_2_private_dns
elif pix_server == '3':
    selected_server = linux_3_private_dns
elif pix_server == '4':
    selected_server = linux_4_private_dns
elif pix_server == '5':
    selected_server = linux_5_private_dns
elif pix_server == '6':
    selected_server = linux_6_private_dns
elif pix_server == '7':
    selected_server = linux_7_private_dns
    
#elif pix_server == '8':
#    selected_server = linux_8_private_dns
#elif pix_server == '9':
#    selected_server = linux_9_private_dns 

#Public instances names for testing
elif pix_server == '7':
    selected_server = linux_7_public_dns   
elif pix_server == '8':
    selected_server = linux_8_public_dns
elif pix_server == '9':
    selected_server = linux_9_public_dns
elif pix_server == '20':
    selected_server = linux_20_public_dns


elif pix_server == '10':
    selected_server = linux_10_private_dns
elif pix_server == '11':
    selected_server = linux_11_private_dns
elif pix_server == '12':
    selected_server = linux_12_private_dns
elif pix_server == '13':
    selected_server = linux_13_private_dns
elif pix_server == '14':
    selected_server = linux_14_private_dns
elif pix_server == '15':
    selected_server = linux_15_private_dns
elif pix_server == '16':
    selected_server = linux_16_private_dns
elif pix_server == '17':
    selected_server = linux_17_private_dns
elif pix_server == '18':
    selected_server = linux_18_private_dns
elif pix_server == '19':
    selected_server = linux_19_private_dns
#elif pix_server == '20':
#    selected_server = linux_20_private_dns


else:
    selected_server = None
    print('Invalid choice. Please run again and choose a valid number between 1 and 20.')

linux_1_instance_id = 'i-04adbf6bd736ccfc2'
linux_2_instance_id = 'i-077015546d5be1c59'
linux_3_instance_id = 'i-0aec30aefce006a7d'
linux_4_instance_id = 'i-0be35c9980cc4deed'
linux_5_instance_id = 'i-0f06c4a2d9d7c63e5'
linux_6_instance_id = 'i-0da998439610ade74'
linux_7_instance_id = 'i-02173d786cd322233'
linux_8_instance_id = 'i-070df12df86332a0a'
linux_9_instance_id = 'i-094cf906d9e93cb65'
linux_10_instance_id = 'i-0bac8ae67e32657f8'
linux_11_instance_id = 'i-0c86f92788b1cf247'
linux_12_instance_id = 'i-0d278c6c9e882d237'
linux_13_instance_id = 'i-0039ff54eaea0e29b'
linux_14_instance_id = 'i-01e3fccdec28e922c'
linux_15_instance_id = 'i-02072d30e2a663577'
linux_16_instance_id = 'i-05cb95a18a70cee96'
linux_17_instance_id = 'i-06d9d376a9e783d6a'
linux_18_instance_id = 'i-0a8082c89b968e252'
linux_19_instance_id = 'i-0b118b6e07d098809'
linux_20_instance_id = 'i-0c6dd1d5c938305be'

#Start EC2 instance
#client = boto3.client('ec2')
#response = client.start_instances(InstanceIds=['i-0c86f92788b1cf247'], AdditionalInfo='string', DryRun=False)

#Create new instancs(s) using AMI id ami-e806df90 (Linux Processing Server)????????

#Connect via SSH and run commands
#Change this to local key file
aws_private_key_file = "/Users/michaelokonski/Dropbox/SolSpec/Solspec_Logins/Pix4DProcessingServers.pem"
k = paramiko.RSAKey.from_private_key_file(aws_private_key_file)
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect( hostname = selected_server, username = 'ubuntu', pkey = k )
print('Sucessfully connected to ' + selected_server + ', ' + 'Pix4D Linux Process Server ' + pix_server)

##Payload Variables
s3_project_folder = raw_input('Enter the full key value in s3: ')
bucket_name = s3_project_folder.split(os.sep)[0]
parent_folder = s3_project_folder.split(os.sep)[1]

#s3 out location
#out_location = raw_input('Enter the full bucket/key path/directory where you want the project written to: ')

#Convert geolocation file. Needs a local workspace as s3 objects are immutable
ext = '.csv'
s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3')
local_temp_folder = '/Users/michaelokonski/Desktop/solspec-test-mo/20180227_54037'

def pd_read_csv_s3(path, *args, **kwargs):
    path = path.replace('s3://', '')
    bucket, key = path.split('/', 1)
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    return pd.read_csv(io.BytesIO(obj['Body'].read()), *args, **kwargs)

file = pd_read_csv_s3(s3_project_folder + '/' + parent_folder  + '.tgs', header=None)
file[0] = file[0] + '.jpg'

outfile = local_temp_folder + '/' + parent_folder + ext
write_outfile = file.to_csv(outfile, sep=',', index=False, header=False)
s3_client.upload_file(outfile, bucket_name, parent_folder + '/' + parent_folder + ext)

#Remove file from local system
os.remove(outfile)
print('Geolocation file conversion completed and copied successfully.')

#Sync to local server
stdin , stdout, stderr = c.exec_command('mkdir -p ' + s3_project_folder)
print("stdout: " + stdout.read())
print("stderr: " + stderr.read())

#To do......change buffer size on console ssh output. Currently waits until operation has complete to print to console.

stdin , stdout, stderr = c.exec_command('aws s3 sync s3://' + s3_project_folder + ' ' + s3_project_folder)
print('syncing from s3 to local.........................................................')
print("stdout: " + stdout.read() + 'Sync from s3 to local completed successfully.')
print("stderr: " + stderr.read())

##Pix4D starts here 
stdin , stdout, stderr = c.exec_command('pix4dmapper -c --email teamsolspec2@duraroot.com --password H2@2014!')
print("stdout: " + stdout.read())
print("stderr: " + stderr.read())

start_text = 'pix4dmapper -c -n --image-dir '
geo_file_text = ' --geolocation-format pix4d-lat-long --geolocation-file '
out_path = 'process_jobs/'

stdin , stdout, stderr = c.exec_command(start_text + s3_project_folder + geo_file_text + s3_project_folder + '/' + parent_folder + ext + ' ' + out_path + s3_project_folder + '.p4d')
print("stdout: " + stdout.read() + '............Project created successfully............')
print("stderr: " + stderr.read())

##Run project
stdin , stdout, stderr = c.exec_command('pix4dmapper -c -r ' + out_path + s3_project_folder.split(os.sep)[0] + '/' + parent_folder + '.p4d')
print('Project started at: ' + stdout.read())
print("stderr: " + stderr.read())

stdin , stdout, stderr = c.exec_command('cd' + ' ' + bucket_name + ' && ' + 'pwd' + ' && ' + 'aws s3 sync . s3://' + bucket_name)
print("stdout: " + stdout.read())
print("stderr: " + stderr.read())

#Sync to out_location
stdin , stdout, stderr = c.exec_command('aws s3 sync . s3://' + bucket_name)
print('syncing from local to s3.........................................................')
print("stdout: " + stdout.read() + 'Sync from  local to s3 completed successfully.')
print("stderr: " + stderr.read())

#To do......sync/cp derivative folders to discrete s3 or ec2 locations e.g. ortho to ortho folder/key, 3d folder to 3d folder out etc.
#c.close()

#Stop EC2 instance
#client = boto3.client('ec2')
#response = client.start_instances(InstanceIds=['i-0c86f92788b1cf247'], AdditionalInfo='string', DryRun=False)

#Terminate EC2 instance?????????

