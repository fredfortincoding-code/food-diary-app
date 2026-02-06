from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_NAME = "food_diary.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_name TEXT NOT NULL,
            calories INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Get all entries
    cursor.execute('SELECT id, food_name, calories, timestamp FROM entries ORDER BY timestamp DESC')
    entries = cursor.fetchall()
    
    # Get daily totals for a summary card
    cursor.execute('''
        SELECT DATE(timestamp) as day, SUM(calories) 
        FROM entries 
        WHERE calories IS NOT NULL 
        GROUP BY day 
        ORDER BY day DESC LIMIT 7
    ''')
    daily_totals = cursor.fetchall()
    
    # Current day total
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('SELECT SUM(calories) FROM entries WHERE DATE(timestamp) = ?', (today,))
    today_total = cursor.fetchone()[0] or 0
    
    conn.close()
    return render_template('index.html', entries=entries, daily_totals=daily_totals, today_total=today_total)

@app.route('/add', methods=['POST'])
def add():
    food = request.form.get('food')
    calories = request.form.get('calories')
    if food:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO entries (food_name, calories) VALUES (?, ?)', 
                       (food, int(calories) if calories and calories.isdigit() else None))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:entry_id>')
def delete(entry_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM entries WHERE id = ?', (entry_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
