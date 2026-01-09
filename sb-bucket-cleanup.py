import boto3
import json
from datetime import datetime, timezone, timedelta
from botocore.exceptions import ClientError

# CONFIGURE THESE
BUCKET_NAME = "rajav-cleanup-demo-bucket"   
RETENTION_DAYS = 30

def lambda_handler(event, context):
    s3 = boto3.client("s3")
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=RETENTION_DAYS)

    print(f"Starting cleanup for bucket: {BUCKET_NAME}")
    print(f"Deleting objects older than: {cutoff.isoformat()}")

    deleted_keys = []
    kept_keys = []

    continuation_token = None

    try:
        while True:
            if continuation_token:
                response = s3.list_objects_v2(
                    Bucket=BUCKET_NAME,
                    ContinuationToken=continuation_token
                )
            else:
                response = s3.list_objects_v2(Bucket=BUCKET_NAME)

            # If bucket is empty
            if "Contents" not in response:
                print("Bucket is empty or no objects found.")
                break

            objects_to_delete = []

            for obj in response["Contents"]:
                key = obj["Key"]
                last_modified = obj["LastModified"]  # timezone-aware datetime

                if last_modified < cutoff:
                    print(f"Marked for delete: {key} (LastModified: {last_modified})")
                    objects_to_delete.append({"Key": key})
                    deleted_keys.append(key)
                else:
                    print(f"Keep: {key} (LastModified: {last_modified})")
                    kept_keys.append(key)

            # Delete up to 1000 objects at once
            if objects_to_delete:
                delete_response = s3.delete_objects(
                    Bucket=BUCKET_NAME,
                    Delete={"Objects": objects_to_delete}
                )
                print(f"Deleted batch: {[d['Key'] for d in delete_response.get('Deleted', [])]}")

            # Pagination
            if response.get("IsTruncated"):
                continuation_token = response.get("NextContinuationToken")
            else:
                break

    except ClientError as e:
        print(f"Error processing bucket {BUCKET_NAME}: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

    print(f"Cleanup complete. Deleted {len(deleted_keys)} objects, kept {len(kept_keys)} objects.")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "bucket": BUCKET_NAME,
            "deleted_count": len(deleted_keys),
            "deleted_objects": deleted_keys,
            "kept_count": len(kept_keys)
        })
    }
