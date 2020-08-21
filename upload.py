#!/usr/bin/env python3
"""
    Create a simple docker-compose.yml that instantiates a minio service, and a
    python container that connects to minio to upload an object (maybe a small
    sample image you bind mount into the container) into minio and then print to
    standard out a "share url" that includes an expiration that is moderately
    small -- shoot for 24 hours.
"""

import os
from datetime import timedelta

from dotenv import load_dotenv

from minio import Minio
from minio.error import (BucketAlreadyOwnedByYou, BucketAlreadyExists)

load_dotenv()

""" `secure= True` causes SSL issue
    source: https://github.com/minio/minio/issues/8161
    solution: 'You either have to configure a TLS private key + certificate or
        try to access your MinIO container over plain HTTP.'
    temporary fix: access over HTTP
"""
""" `minio:9000` fails minio's is_valid_endpoint based on change in Python3.7.6
    source: https://github.com/minio/minio-py/issues/835
    solution: 'it seems in short time we must stick to python 3.7.5 until this
        resolved in minio-py itself.'
"""
"""
    lines below result in share URL that is only valid within docker
    minioClient = Minio('host.docker.internal:9000',
    minioClient = Minio('minio:9000',
"""
# By providing the host ip, the share url will be valid from the host
minioClient = Minio(os.getenv("HOST_IP")+':9000',
                    access_key=os.getenv("ACCESS_KEY"),
                    secret_key=os.getenv("SECRET_KEY"),
                    secure=False)

if __name__ == "__main__":
    bucket = "photos"
    filename = "hibou.png"

    # Make a bucket
    try:
        print("creating bucket:", bucket)
        minioClient.make_bucket(bucket)
    except (BucketAlreadyOwnedByYou, BucketAlreadyExists) as err:
        pass

    # Upload file
    print("uploading:", filename)
    minioClient.fput_object(bucket, filename, f'/{bucket}/{filename}')

    # Print presignerd URL to STDOUT
    print("generating presigned URL:")
    url = minioClient.presigned_get_object(bucket, filename, timedelta(hours=24))
    print(url)
