import hashlib
import time
from flask import Flask, jsonify
from threading import Thread

app = Flask(__name__)

# Shared data (timestamp and hash)
timestamp_data = {
    "timestamp": "",
    "hash": ""
}

def calculate_hash():
    global timestamp_data
    while True:
        try:
            # Read the timestamp file
            with open('/usr/src/app/files/timestamp.txt', 'r') as f:
                data = f.read().strip()
            
            if data:
                # Update timestamp and calculate hash
                timestamp_data["timestamp"] = data
                timestamp_data["hash"] = hashlib.sha256(data.encode('utf-8')).hexdigest()
                
                # Print the timestamp and hash to logs
                print(f"Timestamp: {data}", flush=True)
                print(f"Hash: {timestamp_data['hash']}", flush=True)
            
            time.sleep(5)
        except FileNotFoundError:
            print("File not found, waiting for writer to generate it...", flush=True)

@app.route("/", methods=["GET"])
def status():
    """Endpoint to return the current timestamp and hash in JSON format"""
    return jsonify(timestamp_data)

def run_flask():
    # Start the Flask app to serve the status endpoint
    app.run(host='0.0.0.0', port=3000)

if __name__ == "__main__":
    # Start the hash calculation in a separate thread
    hash_thread = Thread(target=calculate_hash)
    hash_thread.daemon = True  # Ensure the thread ends when the main program ends
    hash_thread.start()

    # Start the Flask app in the main thread
    run_flask()