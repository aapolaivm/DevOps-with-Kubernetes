# Script to create an application that generates a random string on startup, 
# stores this string into memory, and outputs it every 5 seconds with a timestamp.

import time
import uuid
from datetime import datetime

def generate_random_string():
    return str(uuid.uuid4())

def log_with_timestamp(random_string):
    while True:
        timestamp = datetime.now().isoformat()
        print(f"{timestamp}: {random_string}", flush=True)
        time.sleep(5)

def main():
    random_string = generate_random_string()
    log_with_timestamp(random_string)

if __name__ == "__main__":
    main()