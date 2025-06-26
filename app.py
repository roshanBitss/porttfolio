from flask import Flask, render_template, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('test.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

CORS(app)

def init_db():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL,
        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)', (name, email, message))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/admin/messages')
def admin_messages():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('SELECT id, name, email, message, submitted_at FROM contacts ORDER BY submitted_at DESC')
    messages = c.fetchall()
    conn.close()
    html = '''
    <html><head><title>Contact Messages</title>
    <style>
    body { font-family: Arial, sans-serif; background: #f8f9fa; }
    table { border-collapse: collapse; width: 90%; margin: 2rem auto; background: #fff; box-shadow: 0 2px 16px #0001; }
    th, td { border: 1px solid #ecebe9; padding: 10px; text-align: left; }
    th { background: #20c997; color: #fff; }
    tr:nth-child(even) { background: #f2f2f2; }
    </style></head><body>
    <h2 style="text-align:center; color:#20c997;">Contact Messages</h2>
    <table>
      <tr><th>ID</th><th>Name</th><th>Email</th><th>Message</th><th>Submitted At</th></tr>
    '''
    for msg in messages:
        html += f'<tr><td>{msg[0]}</td><td>{msg[1]}</td><td>{msg[2]}</td><td>{msg[3]}</td><td>{msg[4]}</td></tr>'
    html += '</table></body></html>'
    return html

if __name__ == '__main__':
    init_db()
    app.run(debug=True) 