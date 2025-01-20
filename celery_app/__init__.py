from dotenv import load_dotenv
import os
from celery import Celery
from kombu.utils.url import safequote

# Load environment variables from .env
load_dotenv()

# Read AWS credentials and other settings from environment variables
AWS_ACCESS_KEY_ID = safequote(os.getenv("AWS_ACCESS_KEY_ID"))
AWS_SECRET_ACCESS_KEY = safequote(os.getenv("AWS_SECRET_ACCESS_KEY"))
AWS_REGION = os.getenv("AWS_REGION")
AWS_SQS_URL = os.getenv("AWS_SQS_URL")

# Initialize Celery app
app = Celery(
    "celery_app",
    broker=f"sqs://{AWS_ACCESS_KEY_ID}:{AWS_SECRET_ACCESS_KEY}@",
    backend=None,  # Add result backend if required
    include=["celery_app.tasks.crawling"]  # List of modules to import tasks from
)

# Set Celery configuration for SQS
app.conf.update(
    broker_transport_options={
        "region": AWS_REGION,
        "predefined_queues": {
            "celery": {
                "url": AWS_SQS_URL
            },
        }
    },
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)