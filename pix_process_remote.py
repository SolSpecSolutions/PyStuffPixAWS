#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 12:06:19 2018

@author: michaelokonski
"""

import paramiko
import os

#To do...tie in grab stopped ec2 script. Paths are here for testing
s3_project_folder = 'solspec-test-mo/20180227_54037'

pix_server = 'ec2-18-236-246-157.us-west-2.compute.amazonaws.com'

def pix_process(*args):
    #print(s3_project_folder)
    
    #Connect via SSH and run commands
    #Change this to local key file
    aws_private_key_file = "/Users/michaelokonski/Dropbox/SolSpec/Solspec_Logins/Pix4DProcessingServers.pem"
    k = paramiko.RSAKey.from_private_key_file(aws_private_key_file)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect( hostname = pix_server, username = 'ubuntu', pkey = k )
    print('Sucessfully connected to ' + pix_server + ', ' + 'Pix4D Linux Process Server ' + pix_server)

    bucket_name = s3_project_folder.split(os.sep)[0]
    parent_folder = s3_project_folder.split(os.sep)[1]
    
    #Preparing payload
    #Create working directory on local
    stdin , stdout, stderr = client.exec_command('mkdir -p ' + s3_project_folder)
    print("stdout: " + stdout.read())
    print("stderr: " + stderr.read())
    
    #Sync to local
    stdin , stdout, stderr = client.exec_command('aws s3 ls ' + s3_project_folder)
    print('syncing from s3 to local.........................................................')
    print("stdout: " + stdout.read() + 'Sync from s3 to local completed successfully.')
    print("stderr: " + stderr.read())
    
    #Sync to local server
    stdin , stdout, stderr = client.exec_command('mkdir -p ' + s3_project_folder)
    print("stdout: " + stdout.read())
    print("stderr: " + stderr.read())

    stdin , stdout, stderr = client.exec_command('aws s3 sync s3://' + s3_project_folder + ' ' + s3_project_folder)
    print('syncing from s3 to local.........................................................')
    print("stdout: " + stdout.read() + 'Sync from s3 to local completed successfully.')
    print("stderr: " + stderr.read())
    
    #Pix4D Stuff
    #Login
    stdin , stdout, stderr = client.exec_command('pix4dmapper -c --email teamsolspec2@duraroot.com --password H2@2014!')
    print("stdout: " + stdout.read())
    print("stderr: " + stderr.read())
    
    #Create project
    start_text = 'pix4dmapper -c -n --image-dir '
    out_path = 'process_jobs/' #Local process server workspace

    stdin , stdout, stderr = client.exec_command(start_text + s3_project_folder + ' ' + out_path + s3_project_folder + '.p4d')
    print("stdout: " + stdout.read() + '............Project created successfully............')
    print("stderr: " + stderr.read())
    
    #Run project
    stdin , stdout, stderr = client.exec_command('pix4dmapper -c -r ' + out_path + bucket_name + '/' + parent_folder + '.p4d')
    print('Project started at: ' + stdout.read())
    print("stderr: " + stderr.read())
    
    #Sync to s3
    stdin , stdout, stderr = client.exec_command('cd ' + bucket_name + ' && ' + 'aws s3 sync . s3://' + bucket_name)
    print("stdout: " + stdout.read())
    print("stderr: " + stderr.read())
    
pix_process()
