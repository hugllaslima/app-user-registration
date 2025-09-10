# Aplicação Para Cadastros de Usuários

### Arquitetura da Aplicação

├── .github/workflows/ 

│ ├── deploy-develop.yml  # (Para Ambiente de Testes)

│ └── deploy-production.yml  # (Para Ambiente de Stage)

├── scripts/

│ ├── sync-branchs.sh  # (Sincronizar as branchs após pull request)

│ └── entrypoint.sh #  (Script de inicialização dentro do Docker)

├── static/

│ ├── css/

│ │ └── style.css

├── templates/

│ ├── login.html

│ ├── register.html

│ └── users.html

├── .gitgnore

├── app.py

├── Dockerfile

├── LICENSE.md

├── README.md

├── requirements.txt

└── SECURITY.md

### Criando Usuários em Ambiente de Testes

**Rode a Aplicação com os comandos abaixo:**
``` 
docker build -t app-user-registration-develop .
docker run -d --restart=always --name app-user-registration-develop -p 8080:5000 app-user-registration-develop:latest
```

**Acesse a Aplicação Pela URL Abaixo:**

http://localhost:8080/register
