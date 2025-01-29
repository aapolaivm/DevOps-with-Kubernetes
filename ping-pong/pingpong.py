from flask import Flask, jsonify

app = Flask(__name__)

# Initialize counter
counter = 0

@app.route('/pingpong')
def get_pingpong():
    global counter
    counter += 1
    return jsonify({"pingpong_count": counter})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3001)