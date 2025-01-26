import time
import uuid
from datetime import datetime
from flask import Flask, jsonify

app = Flask(__name__)

# Global variables to store the random string and timestamp
random_string = str(uuid.uuid4())
last_timestamp = datetime.now().isoformat()

def generate_random_string():
    return str(uuid.uuid4())

@app.route("/", methods=["GET"])
def status():
    """Endpoint to return the current random string and timestamp"""
    return jsonify({
        "timestamp": last_timestamp,
        "random_string": random_string
    })

def log_with_timestamp():
    global last_timestamp, random_string
    while True:
        # Update the timestamp every 5 seconds
        last_timestamp = datetime.now().isoformat()
        print(f"{last_timestamp}: {random_string}", flush=True)
        time.sleep(5)

def main():
    # Start the Flask app in a separate thread to serve the status endpoint
    from threading import Thread
    thread = Thread(target=log_with_timestamp)
    thread.daemon = True  # Ensures the thread ends when the main program ends
    thread.start()
    
    # Start the Flask web server
    app.run(host="0.0.0.0", port=3000)

if __name__ == "__main__":
    main()
