from flask import Flask, jsonify, request, render_template_string
import os
import threading
import time
import json
import urllib.request
import logging

app = Flask(__name__)

# Environment variables
message = os.getenv("MESSAGE", "No message")
pingpong_service_url = "http://pingpong-svc/pingpong"

# Global variables
file_content = ""
hash_value = ""
timestamp_data = ""
pingpong_count = 0

# Read the content of the information.txt file
try:
    with open('/app/config/information.txt', 'r') as file:
        file_content = file.read()
except Exception as e:
    logging.error(f"Failed to read information.txt: {e}")

def calculate_hash():
    global hash_value, timestamp_data
    while True:
        if timestamp_data:
            hash_value = hash(timestamp_data)
        time.sleep(5)

def fetch_pingpong_count():
    global pingpong_count
    try:
        with urllib.request.urlopen(pingpong_service_url) as response:
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
    fetch_pingpong_count()  # Fetch the pingpong count before rendering the HTML
    if hash_value and timestamp_data:
        html_content = f"""
        <html>
            <body>
                <p>file content: {file_content}</p>
                <p>env variable: MESSAGE={message}</p>
                <p>{timestamp_data}: {hash_value}.</p>
                <p>Ping / Pongs: {pingpong_count}</p>
            </body>
        </html>
        """
        return render_template_string(html_content), 200
    else:
        return "Log output service is running", 200

if __name__ == "__main__":
    # Start the hash calculation in a separate thread
    threading.Thread(target=calculate_hash, daemon=True).start()
    app.run(host="0.0.0.0", port=3000)