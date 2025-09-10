#!/bin/sh

# Garante que o script pare se algum comando falhar
set -e

# 1. Executa o comando para inicializar o banco de dados
echo "Inicializando o banco de dados..."
flask init-db

# 2. Inicia a aplicação principal usando Gunicorn
echo "Iniciando o servidor Gunicorn..."
exec gunicorn --bind 0.0.0.0:5000 app:app
