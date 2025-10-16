from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from prometheus_flask_exporter import PrometheusMetrics
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__, static_url_path='/static')

# Configurações de segurança usando variáveis de ambiente
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'fallback-key-change-in-production')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_COOKIE_SECURE'] = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Configuração do Prometheus
metrics = PrometheusMetrics(app)
# Métricas estáticas sobre a aplicação
metrics.info('app_info', 'Informações da aplicação', version='1.0.0')

# Métricas personalizadas
login_counter = metrics.counter(
    'login_count_total', 'Número de logins realizados'
)
login_failed_counter = metrics.counter(
    'login_failed_count_total', 'Número de logins falhos'
)
registration_counter = metrics.counter(
    'registration_count_total', 'Número de registros realizados'
)

# Definir funções auxiliares para incrementar contadores com segurança
def increment_login_counter():
    global login_counter
    try:
        if hasattr(login_counter, 'inc'):
            login_counter.inc()
        else:
            print("Contador de login não possui método inc")
    except Exception as e:
        print(f"Erro ao incrementar contador de login: {e}")

def increment_login_failed_counter():
    global login_failed_counter
    try:
        if hasattr(login_failed_counter, 'inc'):
            login_failed_counter.inc()
        else:
            print("Contador de login falho não possui método inc")
    except Exception as e:
        print(f"Erro ao incrementar contador de login falho: {e}")

def increment_registration_counter():
    global registration_counter
    try:
        if hasattr(registration_counter, 'inc'):
            registration_counter.inc()
        else:
            print("Contador de registro não possui método inc")
    except Exception as e:
        print(f"Erro ao incrementar contador de registro: {e}")


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
        
        # Se não existir nenhum admin, criar um usuário admin padrão com senha hash
        if admin_exists == 0:
            admin_username = os.getenv('ADMIN_USERNAME', 'admin')
            admin_password = os.getenv('ADMIN_PASSWORD', 'admin')
            admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
            admin_fullname = os.getenv('ADMIN_FULLNAME', 'Administrador')
            admin_phone = os.getenv('ADMIN_PHONE', '(00) 00000-0000')
            
            hashed_password = generate_password_hash(admin_password)
            
            conn.execute(
                "INSERT OR IGNORE INTO users (fullname, phone, email, username, password, is_admin) VALUES (?, ?, ?, ?, ?, ?)",
                (admin_fullname, admin_phone, admin_email, admin_username, hashed_password, 1)
            )
            print("Usuário administrador padrão criado com senha hash.")
    
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
        
        # Validação básica de entrada
        if not username or not password:
            flash('Usuário e senha são obrigatórios')
            return render_template('login.html')
        
        with sqlite3.connect(DB_NAME) as conn:
            user = conn.execute("SELECT id, username, password, is_admin FROM users WHERE username=?", (username,)).fetchone()
            
        if user and check_password_hash(user[2], password):
            session.clear()  # Limpa qualquer sessão anterior
            session['logged_in'] = True
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['is_admin'] = bool(user[3])
            
            # Incrementa o contador de login bem-sucedido
            increment_login_counter()
            
            return redirect(url_for('users'))
        else:
            # Incrementa o contador de login falho
            increment_login_failed_counter()
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
        fullname = request.form.get('fullname', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        is_admin = 'is_admin' in request.form
        
        # Validação básica
        if not all([fullname, email, phone, username, password]):
            flash('Todos os campos são obrigatórios!')
            return render_template('register.html')
        
        # Validação de senha forte
        if len(password) < 8:
            flash('A senha deve ter pelo menos 8 caracteres!')
            return render_template('register.html')
        
        # Hash da senha
        hashed_password = generate_password_hash(password)
        
        try:
            with sqlite3.connect(DB_NAME) as conn:
                conn.execute(
                    "INSERT INTO users (fullname, phone, email, username, password, is_admin) VALUES (?, ?, ?, ?, ?, ?)",
                    (fullname, phone, email, username, hashed_password, is_admin)
                )
            # Incrementa o contador de registros
            increment_registration_counter()
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
    # Configurações de produção mais seguras
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    
    app.run(host=host, port=port, debug=debug_mode)
