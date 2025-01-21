import boto3
from dotenv import load_dotenv
import os
import json

load_dotenv()

# static class for AWS
class AwsSdk:
    @staticmethod
    def publish_sns_message(subject: str, message: dict, topic_arn: str = None):
        if topic_arn is None:
            topic_arn = os.getenv("AWS_SNS_TOPIC_ARN")
        
        AWS_REGION = os.getenv("AWS_REGION")
        AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
        AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

        sns = boto3.client("sns", region_name=AWS_REGION, 
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        
        sns.publish(
            TopicArn=topic_arn,
            Message=json.dumps(message),
            Subject=subject,
            MessageAttributes={
                "ContentEncoding": {
                    "DataType": "String",
                    "StringValue": "utf-8"
                },
                "ContentType": {
                    "DataType": "String",
                    "StringValue": "application/json"
                }
            }
        )