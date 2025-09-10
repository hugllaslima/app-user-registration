from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os


app = Flask(__name__)
app.secret_key = 'mysupersecret' # Troque isso em produção!


DB_NAME = 'users.db'


# Initialize DB
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            fullname TEXT NOT NULL,
                            phone TEXT NOT NULL,
                            email TEXT NOT NULL,
                            username TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL
                        )''')
    print("Tabela 'users' verificada/criada.")


@app.cli.command("init-db")
def init_db_command():
    """Cria as tabelas do banco de dados."""
    init_db()


@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return redirect(url_for('users'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect(DB_NAME) as conn:
            user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)).fetchone()
        if user:
            session['logged_in'] = True
            session['user'] = username
            return redirect(url_for('users'))
        else:
            flash('Usuário ou Senha inválidos')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        username = request.form['username']
        password = request.form['password']
        try:
            with sqlite3.connect(DB_NAME) as conn:
                conn.execute(
                    "INSERT INTO users (fullname, phone, email, username, password) VALUES (?, ?, ?, ?, ?)",
                    (fullname, phone, email, username, password)
                )
            flash('Usuário cadastrado com sucesso!')
            return redirect(url_for('login')) 
        except sqlite3.IntegrityError:
            flash('Nome de usuário já existe!')
    return render_template('register.html')


@app.route('/users')
def users():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    with sqlite3.connect(DB_NAME) as conn:
        users = conn.execute("SELECT fullname, phone, email, username FROM users").fetchall()
    return render_template('users.html', users=users)


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)
