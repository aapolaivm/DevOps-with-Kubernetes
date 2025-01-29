from flask import Flask, request, jsonify

app = Flask(__name__)

todos = []

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def create_todo():
    todo = request.json.get('todo')
    if todo:
        todos.append(todo)
        return jsonify({"status": "success"}), 201
    return jsonify({"status": "error", "message": "Invalid input"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)