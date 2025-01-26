from flask import Flask

app = Flask(__name__)

# Initialize counter
counter = 0

@app.route('/pingpong')
def pingpong():
    global counter
    counter += 1
    return f"pong {counter}", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)
