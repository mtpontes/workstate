---
title: AWS Setup
description: Preparing your AWS environment for Workstate.
---

Workstate uses Amazon S3 to store your environment states safely. Here is how to prepare your account.

## 1. Create an S3 Bucket

While Workstate can create a bucket for you during `workstate configure`, you can also use an existing one.

- **Recommended Region**: Choose a region close to you (e.g., `us-east-1` or `sa-east-1`).
- **Permissions**: Public access should be **blocked**.

## 2. IAM Permissions

The user or role running Workstate needs the following permissions on the target bucket. These allow Workstate to manage files, metadata, and tags (used for branch and system tracking).

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:ListBucket",
                "s3:DeleteObject",
                "s3:GetObjectTagging",
                "s3:PutObjectTagging"
            ],
            "Resource": [
                "arn:aws:s3:::your-bucket-name",
                "arn:aws:s3:::your-bucket-name/*"
            ]
        }
    ]
}
```

## 3. Configuration

Run the configuration command to link Workstate to your bucket:

```bash
workstate configure
```

## 4. Troubleshooting with Doctor

If you encounter issues with permissions or connectivity, run:

```bash
workstate doctor
```

The **doctor** command provides a detailed report of your local environment and AWS connectivity, highlighting exactly what might be misconfigured.
