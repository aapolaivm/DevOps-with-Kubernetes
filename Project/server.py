from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Todo App</title>
    </head>
    <body>
        <h1>Welcome to the Todo App!</h1>
        <p>This is a simple HTML response served by Flask.</p>
    </body>
    </html>
    """

if __name__ == '__main__':
    # Getting port value
    port = int(os.getenv('PORT', 5000))
    print(f"Server started in port {port}")
    app.run(host='0.0.0.0', port=port)