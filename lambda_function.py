import boto3
import json

def lambda_handler(event, context):
    # Use US East (N. Virginia) - matches your instance links
    region = "us-east-1"
    
    ec2 = boto3.client("ec2", region_name=region)
    
    print(f"Starting EC2 management in region: {region}")
    
    # 1. FIND AND STOP instances tagged Action=Auto-Stop that are RUNNING
    print("Looking for Auto-Stop instances...")
    stop_filters = [
        {"Name": "tag:Action", "Values": ["Auto-Stop"]},
        {"Name": "instance-state-name", "Values": ["running"]}
    ]
    
    stop_response = ec2.describe_instances(Filters=stop_filters)
    stop_instance_ids = []
    
    for reservation in stop_response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            stop_instance_ids.append(instance_id)
            print(f"Found running Auto-Stop instance: {instance_id}")
    
    if stop_instance_ids:
        print(f"Stopping {len(stop_instance_ids)} instances: {stop_instance_ids}")
        ec2.stop_instances(InstanceIds=stop_instance_ids)
        print("Stop command sent successfully")
    else:
        print("No running Auto-Stop instances found")
    
    # 2. FIND AND START instances tagged Action=Auto-Start that are STOPPED
    print("Looking for Auto-Start instances...")
    start_filters = [
        {"Name": "tag:Action", "Values": ["Auto-Start"]},
        {"Name": "instance-state-name", "Values": ["stopped"]}
    ]
    
    start_response = ec2.describe_instances(Filters=start_filters)
    start_instance_ids = []
    
    for reservation in start_response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            start_instance_ids.append(instance_id)
            print(f"Found stopped Auto-Start instance: {instance_id}")
    
    if start_instance_ids:
        print(f"Starting {len(start_instance_ids)} instances: {start_instance_ids}")
        ec2.start_instances(InstanceIds=start_instance_ids)
        print("Start command sent successfully")
    else:
        print("No stopped Auto-Start instances found")
    
    # Return summary for test results
    return {
        "statusCode": 200,
        "body": json.dumps({
            "region": region,
            "stopped_instances": stop_instance_ids,
            "started_instances": start_instance_ids,
            "message": "EC2 management completed"
        })
    }
