#usage python app3.py

from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DATABASE = 'contacts.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL
            )
        ''')
        conn.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    # runs when POST request
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        
        with sqlite3.connect(DATABASE) as conn: # insert data into database
            cursor = conn.cursor()
            cursor.execute('INSERT INTO contacts (name, email, phone) VALUES (?, ?, ?)', 
                           (name, email, phone))
            conn.commit()
        
        return redirect('/') # redirects to itself
    
    # runs when GET request - pulls data from database and siplays to screen
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM contacts')
        contacts = cursor.fetchall()
    
    return render_template('index.html', contacts=contacts)

if __name__ == '__main__':
    init_db()
    # app.run(debug=True) # this will run on port 5000
    app.run(host="0.0.0.0", port=8001, debug=True)
