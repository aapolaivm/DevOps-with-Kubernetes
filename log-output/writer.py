import time
from datetime import datetime
import urllib.request
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Environment variables
service_url = os.getenv("LOG_OUTPUT_SERVICE_URL", "http://log-output-svc.devops-exercises.svc.cluster.local/timestamp")

def send_timestamp():
    timestamp = datetime.now().isoformat()
    data = json.dumps({"timestamp": timestamp}).encode('utf-8')
    req = urllib.request.Request(service_url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                logging.info(f"Sent timestamp: {timestamp}")
            else:
                logging.error(f"Failed to send timestamp: {response.status}")
    except Exception as e:
        logging.error(f"Error sending timestamp: {e}")

if __name__ == "__main__":
    while True:
        send_timestamp()  # Send the timestamp
        time.sleep(5)      # Wait for 5 seconds before sending the next one