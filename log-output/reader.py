import hashlib
import time

def calculate_hash():
    while True:
        time.sleep(5)
        try:
            with open('/usr/src/app/files/timestamp.txt', 'r') as f:
                data = f.read()
            print(f"Read data: {data}")  # Debugging line
            hash_value = hashlib.sha256(data.encode('utf-8')).hexdigest()
            print(f"Hash: {hash_value}")
        except FileNotFoundError:
            print("File not found, waiting for writer to generate it...")

if __name__ == "__main__":
    calculate_hash()
