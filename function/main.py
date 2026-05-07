import base64
import json
from google.cloud import storage
from google.cloud import aiplatform
import os
import logging
import functions_framework

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

PROJECT_ID = os.environ.get("PROJECT_ID")
BUCKET_NAME = os.environ.get("BUCKET_NAME")

storage_client = None

def get_storage_client():
    global storage_client
    if storage_client is None:
        storage_client = storage.Client()
    return storage_client

def process_log(data):
    logger.info(f"Processing log: {data.get('file')}")


@functions_framework.cloud_event
def pubsub_trigger(cloud_event):
    try:
        client = get_storage_client()
        
        pubsub_message = base64.b64decode(cloud_event.data['message']['data']).decode('utf-8')
        message = json.loads(pubsub_message)
        
        logger.info(f"Received event for bucket: {message.get('bucket')}, file: {message.get('name')}")

        bucket_name = message.get('bucket')
        file_name = message.get('name')

        if not bucket_name or not file_name:
            logger.warning("Missing bucket or file name in message")
            return

        if not file_name.startswith("logs/"):
            logger.info("Skipping non-log file")
            return

        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_name)

        if not blob.exists():
            logger.error(f"Blob does not exist: {file_name}")
            return

        content = blob.download_as_text()

        log_data = {
            "file": file_name,
            "content": content
        }

        process_log(log_data)

        # TODO: ingest into Vertex AI Data Store / RAG
        logger.info("Ready for ingestion into AI index")

    except Exception as e:
        logger.error(f"Failed to process event: {str(e)}", exc_info=True)
        raise