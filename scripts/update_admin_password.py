import sqlite3

def update_admin_password():
    # Conectar ao banco de dados
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Verificar se o usuário admin existe
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    admin_user = cursor.fetchone()
    
    if admin_user:
        print(f"Usuário admin encontrado: {admin_user}")
        
        # Atualizar a senha do usuário admin para 'admin'
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", ('admin', 'admin'))
        conn.commit()
        
        # Verificar se a atualização foi bem-sucedida
        cursor.execute("SELECT * FROM users WHERE username='admin'")
        updated_user = cursor.fetchone()
        print(f"Usuário admin atualizado: {updated_user}")
        print("Senha do usuário admin atualizada com sucesso para 'admin'")
    else:
        print("Usuário admin não encontrado no banco de dados")
    
    # Fechar a conexão
    conn.close()

if __name__ == "__main__":
    update_admin_password()