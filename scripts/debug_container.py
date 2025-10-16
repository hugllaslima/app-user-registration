#!/usr/bin/env python3
"""
Script de debug para verificar configurações dentro do container
"""
import os
import sqlite3
from werkzeug.security import check_password_hash

def check_env_vars():
    """Verifica se as variáveis de ambiente estão carregadas"""
    print("=== VERIFICAÇÃO DE VARIÁVEIS DE AMBIENTE ===")
    env_vars = [
        'FLASK_SECRET_KEY',
        'ADMIN_USERNAME', 
        'ADMIN_PASSWORD',
        'ADMIN_EMAIL',
        'FLASK_ENV',
        'FLASK_DEBUG'
    ]
    
    for var in env_vars:
        value = os.getenv(var, 'NÃO DEFINIDA')
        print(f"{var}: {value}")
    print()

def check_database():
    """Verifica o banco de dados e usuários"""
    print("=== VERIFICAÇÃO DO BANCO DE DADOS ===")
    
    db_path = 'users.db'
    if not os.path.exists(db_path):
        print(f"❌ Banco de dados {db_path} não existe!")
        return
    
    print(f"✅ Banco de dados {db_path} existe")
    
    try:
        with sqlite3.connect(db_path) as conn:
            # Verificar se a tabela users existe
            tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            print(f"Tabelas encontradas: {[table[0] for table in tables]}")
            
            # Verificar usuários
            users = conn.execute("SELECT id, username, is_admin FROM users").fetchall()
            print(f"Usuários encontrados: {len(users)}")
            
            for user in users:
                print(f"  - ID: {user[0]}, Username: {user[1]}, Admin: {bool(user[2])}")
            
            # Verificar especificamente o usuário admin
            admin_user = conn.execute("SELECT username, password, is_admin FROM users WHERE username=?", ('admin',)).fetchone()
            if admin_user:
                print(f"✅ Usuário admin encontrado: {admin_user[0]}")
                print(f"   - É admin: {bool(admin_user[2])}")
                print(f"   - Hash da senha: {admin_user[1][:20]}...")
                
                # Testar a senha
                test_password = os.getenv('ADMIN_PASSWORD', 'admin123')
                if check_password_hash(admin_user[1], test_password):
                    print(f"✅ Senha '{test_password}' confere com o hash!")
                else:
                    print(f"❌ Senha '{test_password}' NÃO confere com o hash!")
            else:
                print("❌ Usuário admin não encontrado!")
                
    except Exception as e:
        print(f"❌ Erro ao acessar banco: {e}")
    print()

def check_files():
    """Verifica arquivos importantes"""
    print("=== VERIFICAÇÃO DE ARQUIVOS ===")
    files_to_check = ['.env', '.env.example', 'app.py', 'users.db']
    
    for file in files_to_check:
        if os.path.exists(file):
            print(f"✅ {file} existe")
        else:
            print(f"❌ {file} não existe")
    print()

if __name__ == "__main__":
    print("🔍 SCRIPT DE DEBUG DO CONTAINER")
    print("=" * 50)
    
    check_files()
    check_env_vars()
    check_database()
    
    print("🏁 Debug concluído!")