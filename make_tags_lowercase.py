from __future__ import print_function

import json
import boto3
import logging

#setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

#define the connection region
ec2 = boto3.resource('ec2', region_name="us-east-1")
client = boto3.client('ec2')
tags = ["Name", "business_unit", "description", "application_code", "application_criticality", "application_role", "application_name", "environment", "backup", "contact"]
#Set this to True if you don't want the function to perform any actions
debugMode = False

def lambda_handler(event, context):
    #List all EC2 instances
    base = ec2.instances.all()
    #loop through by running instances
    for instance in base:
        instanceid = str(instance)
        instanceSlice = slice(17,36)
        instanceNumber = instanceid[instanceSlice]
        response = client.describe_tags(
            DryRun=False,
            Filters=[
                {
                    'Name': 'resource-id',
                    'Values': [
                        instanceNumber,
                    ]
                },
            ],
            MaxResults=123,
            NextToken='string'
        )
        for i in response["Tags"]:
            val = i['Value']
            key = i['Key']
            if val != val.lower():
                response = ec2.create_tags(
                    DryRun=False,
                    Resources=[
                        instanceNumber,
                    ],
                    Tags=[
                        {
                            'Key': key,
                            'Value': val.lower()
                        },
                    ]
                )
            else:
                print("The Key: %s value is lowercase" % (key))