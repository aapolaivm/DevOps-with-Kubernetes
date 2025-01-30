from flask import Flask, jsonify
import psycopg2
import os

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

# Create table if it doesn't exist
cur.execute("""
CREATE TABLE IF NOT EXISTS counter (
    id SERIAL PRIMARY KEY,
    count INT NOT NULL
)
""")
conn.commit()

# Initialize counter
cur.execute("SELECT count FROM counter WHERE id = 1")
row = cur.fetchone()
if row:
    counter = row[0]
else:
    counter = 0
    cur.execute("INSERT INTO counter (count) VALUES (%s)", (counter,))
    conn.commit()

@app.route('/pingpong')
def get_pingpong():
    global counter
    counter += 1
    cur.execute("UPDATE counter SET count = %s WHERE id = 1", (counter,))
    conn.commit()
    return jsonify({"pingpong_count": counter})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3001)