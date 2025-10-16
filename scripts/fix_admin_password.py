#!/usr/bin/env python3
"""
Script para corrigir a senha do usuário admin existente
"""
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def fix_admin_password():
    """Atualiza a senha do usuário admin existente"""
    
    db_name = 'users.db'
    admin_username = os.getenv('ADMIN_USERNAME', 'admin')
    admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
    
    print(f"🔧 Corrigindo senha do usuário: {admin_username}")
    print(f"   Nova senha: {admin_password}")
    
    try:
        with sqlite3.connect(db_name) as conn:
            # Verificar se o usuário existe
            user = conn.execute("SELECT id, username, password FROM users WHERE username=?", (admin_username,)).fetchone()
            
            if not user:
                print(f"❌ Usuário '{admin_username}' não encontrado!")
                return False
                
            print(f"✅ Usuário encontrado - ID: {user[0]}")
            
            # Verificar se a senha atual já está correta
            if check_password_hash(user[2], admin_password):
                print("✅ Senha já está correta! Nenhuma alteração necessária.")
                return True
            
            # Gerar novo hash da senha
            new_hash = generate_password_hash(admin_password)
            print(f"🔑 Novo hash gerado: {new_hash[:30]}...")
            
            # Atualizar a senha no banco
            conn.execute("UPDATE users SET password=? WHERE username=?", (new_hash, admin_username))
            
            # Verificar se a atualização funcionou
            updated_user = conn.execute("SELECT password FROM users WHERE username=?", (admin_username,)).fetchone()
            
            if check_password_hash(updated_user[0], admin_password):
                print("✅ Senha atualizada com sucesso!")
                return True
            else:
                print("❌ Erro: Senha não foi atualizada corretamente!")
                return False
                
    except Exception as e:
        print(f"❌ Erro ao atualizar senha: {e}")
        return False

if __name__ == "__main__":
    print("🔧 CORREÇÃO DA SENHA DO ADMIN")
    print("=" * 40)
    
    success = fix_admin_password()
    
    if success:
        print("\n🎉 Correção concluída com sucesso!")
        print("Agora você pode fazer login com as credenciais:")
        print(f"   Usuário: {os.getenv('ADMIN_USERNAME', 'admin')}")
        print(f"   Senha: {os.getenv('ADMIN_PASSWORD', 'admin123')}")
    else:
        print("\n❌ Falha na correção. Verifique os logs acima.")