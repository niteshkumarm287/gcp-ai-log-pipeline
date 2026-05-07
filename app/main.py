from flask import Flask, jsonify
from google.cloud import storage
import uuid
import datetime
import json
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

BUCKET_NAME = os.environ.get("BUCKET_NAME")
if not BUCKET_NAME:
    logger.error("BUCKET_NAME environment variable not set")

storage_client = None

def get_storage_client():
    global storage_client
    if storage_client is None:
        storage_client = storage.Client()
    return storage_client

@app.route("/log")
def generate_log():
    if not BUCKET_NAME:
        logger.error("BUCKET_NAME not configured")
        return jsonify({"status": "error", "message": "BUCKET_NAME not configured"}), 500
    
    try:
        log = {
            "id": str(uuid.uuid4()),
            "service": "log-app",
            "severity": "INFO",
            "message": "Hello from app",
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

        file_name = f"logs/{log['id']}.json"

        client = get_storage_client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(file_name)
        blob.upload_from_string(
            json.dumps(log, ensure_ascii=False),
            content_type="application/json"
        )

        logger.info(f"Log uploaded: {file_name}")
        return jsonify({"status": "logged", "file": file_name}), 200

    except Exception as e:
        logger.error(f"Failed to generate log: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/")
def home():
    return jsonify({"status": "running", "service": "log-app"}), 200

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)