import boto3
import json
from datetime import datetime, timezone, timedelta
from botocore.exceptions import ClientError

# CONFIGURE THESE
REGION = "us-east-1"                     
VOLUME_ID = "0d90d604d44ddce97"      
RETENTION_DAYS = 30                      

def lambda_handler(event, context):
    ec2 = boto3.client("ec2", region_name=REGION)
    now = datetime.now(timezone.utc)

    print(f"Starting snapshot job for volume {VOLUME_ID} in {REGION}")
    print(f"Retention: {RETENTION_DAYS} days")

    # 1) CREATE SNAPSHOT
    try:
        snap_resp = ec2.create_snapshot(
            VolumeId=VOLUME_ID,
            Description=f"Auto backup of {VOLUME_ID} at {now.isoformat()}"
        )
        new_snapshot_id = snap_resp["SnapshotId"]
        print(f"Created snapshot: {new_snapshot_id}")
    except ClientError as e:
        print(f"Error creating snapshot for {VOLUME_ID}: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Snapshot creation failed", "detail": str(e)})
        }

    # 2) FIND OLD SNAPSHOTS FOR THIS VOLUME
    cutoff = now - timedelta(days=RETENTION_DAYS)
    print(f"Deleting snapshots older than: {cutoff.isoformat()}")

    try:
        snaps = ec2.describe_snapshots(
            OwnerIds=["self"],
            Filters=[
                {"Name": "volume-id", "Values": [VOLUME_ID]}
            ]
        )
    except ClientError as e:
        print(f"Error describing snapshots: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Describe snapshots failed", "detail": str(e)})
        }

    to_delete = []
    for snap in snaps["Snapshots"]:
        snap_id = snap["SnapshotId"]
        start_time = snap["StartTime"]      # datetime with timezone
        if start_time < cutoff:
            print(f"Marked for delete: {snap_id} (created {start_time})")
            to_delete.append(snap_id)
        else:
            print(f"Keep: {snap_id} (created {start_time})")

    # 3) DELETE OLD SNAPSHOTS
    deleted = []
    for snap_id in to_delete:
        try:
            ec2.delete_snapshot(SnapshotId=snap_id)
            print(f"Deleted snapshot: {snap_id}")
            deleted.append(snap_id)
        except ClientError as e:
            print(f"Failed to delete {snap_id}: {e}")

    print(f"Snapshot job complete. Created: {new_snapshot_id}, Deleted: {len(deleted)}")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "new_snapshot": new_snapshot_id,
            "deleted_snapshots": deleted,
            "deleted_count": len(deleted),
            "volume_id": VOLUME_ID,
            "retention_days": RETENTION_DAYS
        })
    }
