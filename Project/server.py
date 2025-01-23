from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Todo app server is running!"

if __name__ == '__main__':
    # Getting port value
    port = int(os.getenv('PORT', 5000))
    print(f"Server started in port {port}")
    app.run(host='0.0.0.0', port=port)