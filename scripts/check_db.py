import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Consultar todos os usuários
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

print("Todos os usuários:")
for user in users:
    print(user)

# Consultar especificamente o usuário admin
cursor.execute("SELECT * FROM users WHERE username='admin'")
admin_user = cursor.fetchone()

print("\nUsuário admin:")
print(admin_user)

conn.close()