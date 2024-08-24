from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY, description TEXT, amount REAL, currency TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('SELECT * FROM expenses')
    expenses = c.fetchall()
    c.execute('SELECT SUM(amount) FROM expenses')
    total = c.fetchone()[0] or 0
    currency = expenses[0][3] if expenses else 'USD'  # Default to USD if no expenses
    conn.close()
    return render_template('index.html', expenses=expenses, total=total, currency=currency)

@app.route('/add', methods=['POST'])
def add_expense():
    description = request.form['description']
    amount = request.form['amount']
    currency = request.form['currency']  # Get the currency from the form
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('INSERT INTO expenses (description, amount, currency) VALUES (?, ?, ?)', (description, amount, currency))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
