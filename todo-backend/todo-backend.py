import os
import psycopg2
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Initialize database connection
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

@app.route('/todos', methods=['GET'])
def get_todos():
    cur.execute("SELECT id, title FROM todos")  # No "completed" column
    todos = [{"id": row[0], "todo": row[1]} for row in cur.fetchall()]
    print(f"Sending todos: {todos}", flush=True)
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    print(f"Received data: {data}", flush=True)  # Log the received data
    if not data or 'todo' not in data:  
        abort(400, description="Missing 'todo' in request data")
    
    title = data['todo']
    cur.execute("INSERT INTO todos (title) VALUES (%s) RETURNING id", (title,))
    conn.commit()
    todo_id = cur.fetchone()[0]
    
    return jsonify({"id": todo_id}), 201

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)