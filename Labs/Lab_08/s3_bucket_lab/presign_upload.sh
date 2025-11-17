#!/bin/bash

if [ $# -ne 3 ]; then
    echo "Usage: $0 <local_file> <bucket_name> <expiration_seconds>"
    exit 1
fi

LOCAL_FILE=$1
BUCKET=$2
EXPIRATION=$3

echo "Uploading $LOCAL_FILE to s3://$BUCKET/ ..."
aws s3 cp "$LOCAL_FILE" "s3://$BUCKET/"

FILENAME=$(basename "$LOCAL_FILE")

echo "Generating presigned URL..."
PRESIGNED_URL=$(aws s3 presign "s3://$BUCKET/$FILENAME" --expires-in $EXPIRATION)

echo "Presigned URL created"
echo "$PRESIGNED_URL"
echo "Expiration: $EXPIRATION seconds"
