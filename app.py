from flask import Flask, jsonify
import mysql.connector
import os
import time

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "db")
DB_USER = os.environ.get("DB_USER", "appuser")
DB_PASS = os.environ.get("DB_PASS", "apppassword")
DB_NAME = os.environ.get("DB_NAME", "appdb")

def get_db_connection():
    for i in range(10):
        try:
            conn = mysql.connector.connect(
                host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME
            )
            return conn
        except Exception as e:
            print("Waiting for database...", e)
            time.sleep(3)
    raise Exception("Database not ready!")

@app.route('/')
def home():
    return "Flask + MySQL running on Docker Compose (Mac version)!"

@app.route('/init')
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100));")
    conn.commit()
    cursor.close()
    conn.close()
    return "Database initialized!"

@app.route('/add/<name>')
def add_user(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name) VALUES (%s)", (name,))
    conn.commit()
    cursor.close()
    conn.close()
    return f"Added {name}!"

@app.route('/users')
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
