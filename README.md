# ****** Assignment 1: Automated Instance Management Using AWS Lambda and Boto3 ******

# Step 1:

# Create two EC2 instances with the tag "Auto-Start and Auto-Stop."

Output:

<img width="1907" height="845" alt="image" src="https://github.com/user-attachments/assets/922b2d54-fe9c-425f-a637-5bfcd656f5ab" />

<img width="1911" height="851" alt="image" src="https://github.com/user-attachments/assets/0f2d1fd2-3ef9-442d-a6aa-af6110e1d6a9" />

# Step 2

Create an IAM role and Lambda Function 

Output:

<img width="1907" height="845" alt="image" src="https://github.com/user-attachments/assets/f5e87953-ce2a-437e-a6d6-d1273858329a" />

<img width="1903" height="870" alt="image" src="https://github.com/user-attachments/assets/a19f49f9-4975-46e3-8255-a930c44ddb64" />

# Step 3

# Lambda function tested successfully,

Output:

<img width="1906" height="852" alt="image" src="https://github.com/user-attachments/assets/05f34946-02eb-48ef-9285-777b15c9b05f" />

# In Lambda, CloudWatch Logs :
<img width="1906" height="848" alt="image" src="https://github.com/user-attachments/assets/b16a1362-1870-4686-863d-6766a1ba1055" />

# Result :

<img width="1917" height="848" alt="image" src="https://github.com/user-attachments/assets/05b69784-a290-4c4d-9471-330f11417655" />










# ****** Assignment 2: Analyze Sentiment of User Reviews Using AWS Lambda, Boto3, and Amazon Comprehend ******


# Step 1

# IAM Role Creation

Output:

<img width="1900" height="822" alt="image" src="https://github.com/user-attachments/assets/d6cba7f5-7c1e-4c67-b597-a722eaed2de7" />

# Step 2

# Lambda Function Created and tested successfully 

Output:

<img width="1907" height="821" alt="image" src="https://github.com/user-attachments/assets/326389c2-eaf3-4d77-a378-78e731db72b8" />

# Positive Review Test-Case

<img width="1872" height="847" alt="image" src="https://github.com/user-attachments/assets/ad5b099d-bc6c-4e8c-a9e2-09ed70b63bd7" />

# Negative Review Test-Case

<img width="1887" height="802" alt="image" src="https://github.com/user-attachments/assets/1cf2ebd3-e890-47fa-85be-413c1e099e2c" />

# Neutral Review Test-Case

<img width="1887" height="858" alt="image" src="https://github.com/user-attachments/assets/ea1251c9-8ae9-473e-ae7b-b4b496394b99" />









# ****** Assignment 3: Automatic EBS Snapshot and Cleanup Using AWS Lambda and Boto3 ******

# Step 1

# EBS Volume Creation

<img width="1897" height="770" alt="image" src="https://github.com/user-attachments/assets/1ca5d408-d583-4f50-9be6-64c1608b215e" />

# Step 2

<img width="1892" height="807" alt="image" src="https://github.com/user-attachments/assets/09dce20a-5da7-473d-828a-f441673df727" />

# Step 3

# Schedule with EventBridge

<img width="1910" height="863" alt="image" src="https://github.com/user-attachments/assets/f4773466-26d2-4dd0-b926-004cb99bc3b5" />

<img width="1888" height="816" alt="image" src="https://github.com/user-attachments/assets/ad920ad7-aee8-4586-93da-ea79a1f6ccd6" />









# ****** Assignment 4: Automated S3 Bucket Cleanup Using AWS Lambda and Boto3 ******

# Step 1

# S3 Bucket Creations

<img width="1901" height="835" alt="image" src="https://github.com/user-attachments/assets/f8c56d85-c77d-41ab-ad75-07e9f77c0f7d" />

# Step 2

Files are uploading to the bucket :

<img width="1902" height="860" alt="image" src="https://github.com/user-attachments/assets/3c062e72-8745-4eee-b65e-f77966752c32" />

<img width="1846" height="807" alt="image" src="https://github.com/user-attachments/assets/62f36835-84b0-4d01-bcf9-d8ea22c0f364" />

# Step 2

# Lambda IAM Role Setup

<img width="1897" height="811" alt="image" src="https://github.com/user-attachments/assets/75af7af0-9098-4063-aa52-90b8d00f7425" />

<img width="1905" height="812" alt="image" src="https://github.com/user-attachments/assets/6b047e0e-fa12-4a71-a466-7ff3e241b552" />

<img width="1883" height="862" alt="image" src="https://github.com/user-attachments/assets/74fa59b4-19da-46fc-b158-453cb0c8f419" />

# Step 3

# Output Screen

Status: Succeeded
Test Event Name: test-bucket

Response:
{
  "statusCode": 200,
  "body": "{\"bucket\": \"rajav-cleanup-demo-bucket\", \"deleted_count\": 0, \"deleted_objects\": [], \"kept_count\": 3}"
}

The area below shows the last 4 KB of the execution log.

Function Logs:
START RequestId: 0069b6b2-718e-45e6-8c20-5b83186d210a Version: $LATEST
Starting cleanup for bucket: rajav-cleanup-demo-bucket
Deleting objects older than: 2025-12-09T17:08:58.854698+00:00
Keep: Docker .pdf (LastModified: 2026-01-08 16:54:47+00:00)
Keep: EC2-S3-AMIs.pdf (LastModified: 2026-01-08 16:54:46+00:00)
Keep: Screenshot 2025-10-21 101458.png (LastModified: 2026-01-08 16:54:45+00:00)
Cleanup complete. Deleted 0 objects, kept 3 objects.
END RequestId: 0069b6b2-718e-45e6-8c20-5b83186d210a
REPORT RequestId: 0069b6b2-718e-45e6-8c20-5b83186d210a	Duration: 322.18 ms	Billed Duration: 323 ms	Memory Size: 128 MB	Max Memory Used: 94 MB

Request ID: 0069b6b2-718e-45e6-8c20-5b83186d210a

# Step 4

**Observation**: All files remained in S3 bucket after Lambda execution.
**Root Cause**: No objects had LastModified timestamp older than 30 days from current date.
**Lambda logic executed correctly**










