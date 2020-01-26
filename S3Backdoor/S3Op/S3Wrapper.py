import sys, os, socket, boto3, logging, coloredlogs, time, boto3
from random import randint
from urllib.parse import urlparse, unquote
from base64 import b64decode, b64encode
from datetime import datetime
from botocore.exceptions import ClientError, NoCredentialsError
from io import BytesIO

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
coloredlogs.install()


class S3Wrapper:
    def __init__(self, bucket, key):
        self.s3Client = boto3.client("s3")
        self.bucket = bucket
        self.reqKey = "%s_req.txt" % key
        self.respKey = "%s_resp.txt" % key
        self.last_time = datetime.now()
        try:
            self.s3Client.put_object(Body=b"", Bucket=bucket, Key=self.respKey)
        except Exception as err:
            logger.warn(err)
            os._exit(-1)

    def send_data(self, input):
        try:
            input = input + " " * randint(0, 10)
            self.s3Client.put_object(
                Body=b64encode(input.encode()), Bucket=self.bucket, Key=self.reqKey
            )
        except Exception as err:
            logger.warn(err)

    def fetch_response(self):
        try:
            resp = self.s3Client.get_object(
                Bucket=self.bucket, Key=self.respKey, IfModifiedSince=self.last_time
            )
            if resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
                self.last_time = resp["LastModified"]
                content = resp["Body"].read().decode("utf-8")
                if len(content) > 0:
                    print(b64decode(content).decode("utf-8"))
        except ClientError as err:
            if err.response["Error"]["Code"] == "304":
                return
            logger.warn(err)
        except NoCredentialsError as err:
            logger.warn(
                "Please load AWS credentials with S3 privileges over the bucket!"
            )
            os._exit(-1)
        except Exception as err:
            logger.warn(err)
            pass

    def start(self):
        logger.info("Starting a loop fetching results from S3 %s" % self.bucket)
        self.send_data("")
        try:
            while 1:
                self.fetch_response()
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("\nShutting down fetcher per user request.")
