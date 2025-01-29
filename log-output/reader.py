from flask import Flask, jsonify, render_template_string, request
import os
import threading
import time
import urllib.request
import json
import hashlib
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

hash_value = None
timestamp_data = None
pingpong_count = 0

def calculate_hash():
    global hash_value, timestamp_data
    while True:
        time.sleep(5)
        if timestamp_data:
            try:
                logging.debug(f"Generated timestamp: {timestamp_data}")
                hash_value = hashlib.sha256(timestamp_data.encode('utf-8')).hexdigest()
                logging.debug(f"Hash: {hash_value}")
            except Exception as e:
                logging.error(f"Failed to generate hash: {e}")

def fetch_pingpong_count():
    global pingpong_count
    try:
        with urllib.request.urlopen('http://pingpong-svc.devops-exercises.svc.cluster.local:3001/pingpong') as response:
            data = json.loads(response.read().decode())
            pingpong_count = data.get('pingpong_count', 0)
            logging.debug(f"Pingpong count: {pingpong_count}")
    except Exception as e:
        logging.error(f"Failed to fetch pingpong count: {e}")

@app.route('/timestamp', methods=['POST'])
def receive_timestamp():
    global timestamp_data
    if request.is_json:
        data = request.get_json()
        timestamp_data = data.get('timestamp')
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"error": "Unsupported Media Type"}), 415

@app.route('/')
def get_status():
    """Endpoint to return the current hash value and pingpong count in HTML format"""
    # Call fetch_pingpong_count in the background to avoid blocking the request
    threading.Thread(target=fetch_pingpong_count, daemon=True).start()

    if hash_value and timestamp_data:
        html_content = f"""
        <html>
            <body>
                <p>{timestamp_data}: {hash_value}.</p>
                <p>Ping / Pongs: {pingpong_count}</p>
            </body>
        </html>
        """
        return render_template_string(html_content), 200
    else:
        return "Hash not calculated yet", 404

if __name__ == "__main__":
    # Start the hash calculation in a separate thread
    threading.Thread(target=calculate_hash, daemon=True).start()
    app.run(host="0.0.0.0", port=3000)
