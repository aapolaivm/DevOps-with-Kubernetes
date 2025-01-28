import hashlib
import time
import urllib.request
import json
from flask import Flask, request, jsonify, render_template_string
import threading
from datetime import datetime

app = Flask(__name__)

# Global variable to store the hash value and pingpong count
hash_value = None
pingpong_count = 0
timestamp_data = None

def calculate_hash():
    global hash_value, timestamp_data
    while True:
        time.sleep(5)
        try:
            timestamp_data = datetime.now().isoformat()
            print(f"Generated timestamp: {timestamp_data}", flush=True)  # Debugging line
            hash_value = hashlib.sha256(timestamp_data.encode('utf-8')).hexdigest()
            print(f"Hash: {hash_value}", flush=True)
        except Exception as e:
            print(f"Failed to generate hash: {e}", flush=True)

def fetch_pingpong_count():
    global pingpong_count
    while True:
        time.sleep(5)
        try:
            with urllib.request.urlopen('http://pingpong-svc:5001/pingpong') as response:
                data = json.loads(response.read().decode())
                pingpong_count = data.get('pingpong_count', 0)
                print(f"Pingpong count: {pingpong_count}", flush=True)
        except Exception as e:
            print(f"Failed to fetch pingpong count: {e}", flush=True)

@app.route('/timestamp', methods=['POST'])
def receive_timestamp():
    global timestamp_data
    data = request.json
    timestamp_data = data.get('timestamp')
    return jsonify({"status": "success"}), 200

@app.route('/')
def get_status():
    """Endpoint to return the current hash value and pingpong count in HTML format"""
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
    # Start the hash calculation and pingpong fetch in separate threads
    threading.Thread(target=calculate_hash, daemon=True).start()
    threading.Thread(target=fetch_pingpong_count, daemon=True).start()
    app.run(host="0.0.0.0", port=3000)