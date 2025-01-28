from flask import Flask, send_file, make_response
import os
import time
import threading
import urllib.request

app = Flask(__name__)

IMAGE_URL = "https://picsum.photos/1200"
IMAGE_PATH = "/app/static/image.jpg"

def download_image():
    while True:
        try:
            urllib.request.urlretrieve(IMAGE_URL, IMAGE_PATH)
            print("Downloaded new image", flush=True)
        except Exception as e:
            print(f"Failed to download image: {e}", flush=True)
        time.sleep(3600)  # Wait for 60 minutes

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
        <img src="/image" alt="Random Image" style="width:300px;height:500px;">
        <form>
            <input type="text" id="todo" name="todo" maxlength="140">
            <button type="button">Create TODO</button>
        </form>
        <ul>
            <li>TODO 1</li>
            <li>TODO 2</li>
        </ul>
    </body>
    </html>
    """

@app.route('/image')
def image():
    # Serve the cached image with explicit caching headers
    response = make_response(send_file(IMAGE_PATH, mimetype='image/jpeg'))
    response.headers['Cache-Control'] = 'public, max-age=3600'  # Cache for 1 hour
    return response

if __name__ == '__main__':
    # Create the static directory if it doesn't exist
    os.makedirs(os.path.dirname(IMAGE_PATH), exist_ok=True)
    
    # Start the image download thread
    threading.Thread(target=download_image, daemon=True).start()
    
    # Getting port value
    port = int(os.getenv('PORT', 5000))
    print(f"Server started on port {port}")
    app.run(host='0.0.0.0', port=port)