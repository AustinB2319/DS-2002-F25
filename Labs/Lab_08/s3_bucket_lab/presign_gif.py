#!/usr/bin/env python

import sys
import os
from urllib.parse import urlparse
import urllib.request
import boto3


def main():
    if len(sys.argv) != 4:
        print(f"Usage: python {sys.argv[0]} <file_url> <bucket_name> <expires_in_seconds>")
        sys.exit(1)

    file_url = sys.argv[1]
    bucket_name = sys.argv[2]
    try:
        expires_in = int(sys.argv[3])
    except ValueError:
        print("expires_in_seconds must be an integer.")
        sys.exit(1)

    
    print(f"Downloading file from URL: {file_url}")

    parsed = urlparse(file_url)
    
    filename = os.path.basename(parsed.path)

    
    if not filename or "." not in filename:
        filename = "downloaded.gif"

    local_path = filename

    try:
        urllib.request.urlretrieve(file_url, local_path)
    except Exception as e:
        print(f"Error downloading file: {e}")
        sys.exit(1)

    print(f"Saved file as: {local_path}")

   
    print(f"Uploading {local_path} to bucket {bucket_name}...")

    s3 = boto3.client("s3", region_name="us-east-1")

    try:
        s3.upload_file(local_path, bucket_name, filename)
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        sys.exit(1)

    print("Upload complete.")    
    print("Generating presigned URL...")

    try:
        presigned_url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": filename},
            ExpiresIn=expires_in,
        )
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        sys.exit(1)

    print("Presigned URL created")
    print(f"\nExpiration: {expires_in} seconds")


if __name__ == "__main__":
    main()

