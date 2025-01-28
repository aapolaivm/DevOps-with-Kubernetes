from flask import Flask, jsonify
import threading
import time

app = Flask(__name__)

pingpong_count = 0

def increment_pingpong():
    global pingpong_count
    while True:
        pingpong_count += 1
        time.sleep(5)

@app.route('/pingpong')
def get_pingpong():
    return jsonify({"pingpong_count": pingpong_count})

if __name__ == "__main__":
    threading.Thread(target=increment_pingpong, daemon=True).start()
    app.run(host='0.0.0.0', port=5001)