# Imagem base 
FROM python:3.11-slim

# Executado neste diretório dentro do container
WORKDIR /usr/src/app

# Copia o arquivo "requirements.txt"
COPY requirements.txt .

# Instala as dependências do arquivo "requirements.txt"
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos do diretório atual para o container
COPY . .

# aplicação usa a porta 5000 
EXPOSE 5000

# Define o comando padrão que será executado quando o container iniciar
CMD ["python", "app.py"]