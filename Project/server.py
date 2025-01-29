from flask import Flask, send_file, make_response, request, jsonify
import os
import time
import threading
import urllib.request
import json

app = Flask(__name__)

IMAGE_URL = "https://picsum.photos/1200"
IMAGE_PATH = "/app/static/image.jpg"
TODO_BACKEND_URL = "http://todo-backend-svc:5000/todos"

def download_image():
    while True:
        try:
            urllib.request.urlretrieve(IMAGE_URL, IMAGE_PATH)
            print("Downloaded new image", flush=True)
        except Exception as e:
            print(f"Failed to download image: {e}", flush=True)
        time.sleep(3600)  # Wait for 60 minutes

@app.route('/todo-app')
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
        <img src="/todo-app/image" alt="Random Image" style="width:300px;height:300px;">
        <form onsubmit="addTodo(event)">
            <input type="text" id="todo" name="todo" maxlength="140">
            <button type="submit">Create TODO</button>
        </form>
        <h2>Existing Todos:</h2>
        <ul id="todo-list"></ul>
        <script>
            async function fetchTodos() {
                try {
                    let response = await fetch("/todo-app/todos");
                    let todos = await response.json();
                    let todoList = document.getElementById("todo-list");
                    todoList.innerHTML = "";
                    todos.forEach(todo => {
                        let li = document.createElement("li");
                        li.textContent = todo;
                        todoList.appendChild(li);
                    });
                } catch (error) {
                    console.error("Error fetching todos:", error);
                }
            }

            async function addTodo(event) {
                event.preventDefault();
                let todoInput = document.getElementById("todo");
                let todoText = todoInput.value.trim();
                if (!todoText) return;
                try {
                    let response = await fetch("/todo-app/todos", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({ todo: todoText })
                    });
                    if (response.ok) {
                        fetchTodos();
                        todoInput.value = "";
                    } else {
                        console.error("Error creating todo:", response.statusText);
                    }
                } catch (error) {
                    console.error("Error creating todo:", error);
                }
            }

            document.addEventListener("DOMContentLoaded", fetchTodos);
        </script>
    </body>
    </html>
    """

@app.route('/todo-app/image')
def image():
    # Serve the cached image with explicit caching headers
    response = make_response(send_file(IMAGE_PATH, mimetype='image/jpeg'))
    response.headers['Cache-Control'] = 'public, max-age=3600'  # Cache for 1 hour
    return response

@app.route('/todo-app/todos', methods=['GET', 'POST'])
def todos():
    if request.method == 'GET':
        try:
            with urllib.request.urlopen(TODO_BACKEND_URL) as response:
                data = json.loads(response.read().decode())
                return jsonify(data)
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    elif request.method == 'POST':
        todo = request.json.get('todo')
        data = json.dumps({"todo": todo}).encode('utf-8')
        req = urllib.request.Request(TODO_BACKEND_URL, data=data, headers={'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req) as response:
                if response.status == 201:
                    return jsonify({"status": "success"}), 201
                else:
                    return jsonify({"status": "error", "message": response.read().decode()}), response.status
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Create the static directory if it doesn't exist
    os.makedirs(os.path.dirname(IMAGE_PATH), exist_ok=True)
    
    # Start the image download thread
    threading.Thread(target=download_image, daemon=True).start()
    
    # Getting port value
    port = int(os.getenv('PORT', 8080))
    print(f"Server started on port {port}")
    app.run(host='0.0.0.0', port=port)