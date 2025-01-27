import hashlib
import time
from flask import Flask, render_template_string
import threading

app = Flask(__name__)

# Global variable to store the hash value and pingpong count
hash_value = None
pingpong_count = 0
timestamp_data = None

def calculate_hash():
    global hash_value, pingpong_count, timestamp_data
    while True:
        time.sleep(5)
        try:
            with open('/usr/src/app/files/timestamp.txt', 'r') as f:
                data = f.read()
            timestamp_data = data
            print(f"Read data: {data}", flush=True)  # Debugging line
            hash_value = hashlib.sha256(data.encode('utf-8')).hexdigest()
            print(f"Hash: {hash_value}", flush=True)
        except FileNotFoundError:
            print("File not found, waiting for writer to generate it...", flush=True)
        
        try:
            with open('/usr/src/app/files/pingpong.txt', 'r') as f:
                pingpong_count = int(f.read())
            print(f"Pingpong count: {pingpong_count}", flush=True)
        except FileNotFoundError:
            print("Pingpong file not found, waiting for pingpong to generate it...", flush=True)

@app.route('/')
def get_status():
    """Endpoint to return the current hash value and pingpong count in JSON format"""
    if hash_value:
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