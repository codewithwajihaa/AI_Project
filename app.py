from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create the table if it doesn't exist
def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            time TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Home route to display all tasks
@app.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template('index.html', records=tasks)

# Add new task
@app.route('/add', methods=['POST'])
def add_task():
    name = request.form['name']
    description = request.form['description']
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = get_db_connection()
    conn.execute('INSERT INTO tasks (name, description, time) VALUES (?, ?, ?)', 
                 (name, description, time))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

# Search task
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks WHERE name LIKE ? OR description LIKE ?', 
                         ('%' + query + '%', '%' + query + '%')).fetchall()
    conn.close()
    return render_template('index.html', records=tasks)

# Update task
@app.route('/update/<int:id>', methods=['POST'])
def update_task(id):
    name = request.form['name']
    description = request.form['description']
    
    conn = get_db_connection()
    conn.execute('UPDATE tasks SET name = ?, description = ? WHERE id = ?', 
                 (name, description, id))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

# Delete task
@app.route('/delete/<int:id>', methods=['GET'])
def delete_task(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    create_table()  # Ensure the table is created on startup
    app.run(debug=True)

