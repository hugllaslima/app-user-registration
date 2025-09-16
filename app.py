from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
app.secret_key = 'mysupersecret' # Troque isso em produção!

# Configuração do Prometheus
metrics = PrometheusMetrics(app)
# Métricas estáticas sobre a aplicação
metrics.info('app_info', 'Informações da aplicação', version='1.0.0')

# Métricas personalizadas
login_counter = metrics.counter(
    'login_count', 'Número de logins realizados',
    labels={'status': lambda: 'success' if session.get('logged_in') else 'failed'}
)
registration_counter = metrics.counter(
    'registration_count', 'Número de registros realizados'
)


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
                            password TEXT NOT NULL,
                            is_admin BOOLEAN DEFAULT 0
                        )''')
        
        # Verificar se existe algum usuário admin
        admin_exists = conn.execute("SELECT COUNT(*) FROM users WHERE is_admin = 1").fetchone()[0]
        
        # Se não existir nenhum admin, criar um usuário admin padrão
        if admin_exists == 0:
            conn.execute(
                "INSERT OR IGNORE INTO users (fullname, phone, email, username, password, is_admin) VALUES (?, ?, ?, ?, ?, ?)",
                ("Administrador", "(00) 00000-0000", "admin@example.com", "admin", "admin123", 1)
            )
            print("Usuário administrador padrão criado.")
    
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
            user = conn.execute("SELECT id, username, is_admin FROM users WHERE username=? AND password=?", (username, password)).fetchone()
        if user:
            session['logged_in'] = True
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['is_admin'] = bool(user[2])
            # Incrementa o contador de login bem-sucedido
            login_counter.labels(status='success').inc()
            return redirect(url_for('users'))
        else:
            # Incrementa o contador de login falho
            login_counter.labels(status='failed').inc()
            flash('Usuário ou Senha inválidos')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Verificar se o usuário está logado e é administrador
    if not session.get('logged_in'):
        flash('Você precisa estar logado para acessar esta página')
        return redirect(url_for('login'))
    
    if not session.get('is_admin'):
        flash('Apenas administradores podem cadastrar novos usuários')
        return redirect(url_for('users'))
    
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        username = request.form['username']
        password = request.form['password']
        is_admin = 'is_admin' in request.form  # Checkbox para definir se o usuário é admin
        
        try:
            with sqlite3.connect(DB_NAME) as conn:
                conn.execute(
                    "INSERT INTO users (fullname, phone, email, username, password, is_admin) VALUES (?, ?, ?, ?, ?, ?)",
                    (fullname, phone, email, username, password, is_admin)
                )
            # Incrementa o contador de registros
            registration_counter.inc()
            flash('Usuário cadastrado com sucesso!')
            return redirect(url_for('users')) 
        except sqlite3.IntegrityError:
            flash('Nome de usuário já existe!')
    return render_template('register.html')


@app.route('/users')
def users():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    with sqlite3.connect(DB_NAME) as conn:
        if session.get('is_admin'):
            # Administradores veem todos os usuários e podem gerenciá-los
            users = conn.execute("SELECT id, fullname, phone, email, username, is_admin FROM users").fetchall()
        else:
            # Usuários comuns veem apenas seus próprios dados
            users = conn.execute("SELECT id, fullname, phone, email, username FROM users WHERE id = ?", 
                               (session.get('user_id'),)).fetchall()
    
    return render_template('users.html', users=users, is_admin=session.get('is_admin'))


@app.route('/metrics')
def metrics():
    # Esta rota será gerenciada automaticamente pelo PrometheusMetrics
    pass

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', debug=True)
