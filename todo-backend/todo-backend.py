import os
import psycopg2
import logging
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection
conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT")
)
cur = conn.cursor()

# Drop the old table (if needed) and recreate without "completed"
cur.execute("DROP TABLE IF EXISTS todos")
cur.execute("""
CREATE TABLE todos (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL
)
""")
conn.commit()

@app.before_request
def log_request_info():
    logger.info(f"Received {request.method} request for {request.url} with data: {request.get_json(silent=True)}")

@app.route('/todos', methods=['GET'])
def get_todos():
    cur.execute("SELECT id, title FROM todos")  # No "completed" column
    todos = [{"id": row[0], "todo": row[1]} for row in cur.fetchall()]
    logger.info(f"Sending todos: {todos}")
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def create_todo():
    if request.content_type != 'application/json':
        logger.error("Unsupported Media Type: Content-Type must be 'application/json'")
        abort(415, description="Content-Type must be 'application/json'")
    
    data = request.get_json()
    logger.info(f"Received data: {data}")  # Log the received data
    if not data or 'todo' not in data:
        logger.error("Missing 'todo' in request data")
        abort(400, description="Missing 'todo' in request data")
    
    title = data['todo']
    if len(title) > 140:
        logger.error("Todo must be 140 characters or less")
        abort(400, description="Todo must be 140 characters or less")
    
    cur.execute("INSERT INTO todos (title) VALUES (%s) RETURNING id", (title,))
    conn.commit()
    todo_id = cur.fetchone()[0]
    logger.info(f"Created todo with id: {todo_id}")
    
    return jsonify({"id": todo_id}), 201

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)