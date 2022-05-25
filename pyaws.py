import subprocess
from urllib import response
import boto3,paramiko
from requests import session
ec2_client = boto3.client("ec2", region_name="us-east-2")
ec2 = boto3.resource('ec2')
def create_instance():
    instances = ec2.create_instances(
        ImageId = "ami-0fb653ca2d3203ac1",
        MinCount = 1,
        MaxCount = 1,
        InstanceType = "t2.micro",
        KeyName="hung0302"
    )
create_instance()
def get_running_instances():
    
    reservations = ec2_client.describe_instances(Filters=[
        {
            "Name": "instance-state-name",
            "Values": ["running"],
        }
    ]).get("Reservations")

    for reservation in reservations:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            instance_type = instance["InstanceType"]
            public_ip = instance["PublicIpAddress"]
            private_ip = instance["PrivateIpAddress"]
            print(f"{instance_id}, {instance_type}, {public_ip}, {private_ip}")
            return instance_id,public_ip
get_running_instances()
node_ip = get_running_instances()[1]
instance_id = get_running_instances()[0]
print(node_ip)
print(instance_id)
def stop_instances():
    response = ec2_client.stop_instances(
        InstanceIds=[
           instance_id 
        ]
    )
    print("Instance %s stopped"%instance_id)

def connect_to_instance():
    ec2client = boto3.client('ec2')
