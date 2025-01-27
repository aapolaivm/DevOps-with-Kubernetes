import time
from datetime import datetime

def log_with_timestamp():
    while True:
        timestamp = datetime.now().isoformat()
        with open('/usr/src/app/files/timestamp.txt', 'w') as f:
            f.write(f"{timestamp}\n")
        print(f"Written timestamp: {timestamp}", flush=True)  # Debugging line
        time.sleep(5)

if __name__ == "__main__":
    log_with_timestamp()
