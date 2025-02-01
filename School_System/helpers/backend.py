from flask import Flask, request, jsonify
import sqlite3
DB_PATH = "/home/kasper/projects/PYside6/test-app/School_System/db/school.db"

app = Flask(__name__)

# Enable CORS (so JavaScript can communicate with this backend)
from flask_cors import CORS
CORS(app)

# Initialize the database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            start TEXT NOT NULL,
            end TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Route to fetch events
@app.route("/events", methods=["GET"])
def get_events():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, start, end FROM events")
    events = [{"id": row[0], "title": row[1], "start": row[2], "end": row[3]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(events)

# Route to add an event
@app.route("/events", methods=["POST"])
def add_event():
    data = request.json
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO events (title, start, end) VALUES (?, ?, ?)",
                   (data["title"], data["start"], data["end"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Event added!"}), 201

# Initialize DB on startup
if __name__ == "__main__":
    init_db()
    app.run(debug=True)

