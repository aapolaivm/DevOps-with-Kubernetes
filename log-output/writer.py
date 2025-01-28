import time
from datetime import datetime
import urllib.request
import json

def log_with_timestamp():
    while True:
        timestamp = datetime.now().isoformat()
        data = json.dumps({"timestamp": timestamp}).encode('utf-8')
        req = urllib.request.Request('http://log-output-svc:3000/timestamp', data=data, headers={'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    print(f"Sent timestamp: {timestamp}", flush=True)  # Debugging line
                else:
                    print(f"Failed to send timestamp: {response.status}", flush=True)
        except Exception as e:
            print(f"Error sending timestamp: {e}", flush=True)
        time.sleep(5)

if __name__ == "__main__":
    log_with_timestamp()