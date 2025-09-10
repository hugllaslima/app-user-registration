# Aplicação Para Cadastros de Usuários

### Criando Usuários em Ambiente de Testes

**Rode a Aplicação com os comandos abaixo:**
``` 
docker build -t app-user-registration-develop .
docker run -d --restart=always --name app-user-registration-develop -p 8080:5000 app-user-registration-develop:latest
```

**Acesse a Aplicação Pela URL Abaixo:**

http://localhost:8080/register
