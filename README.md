# Sistema de Registro de Usuários

Este é um sistema de registro e gerenciamento de usuários desenvolvido em Flask, com suporte a diferentes níveis de acesso (administrador e usuário comum) e métricas Prometheus para monitoramento.

## 🚀 Funcionalidades

- Sistema de autenticação completo (login/logout)
- Gerenciamento de usuários (cadastro, visualização)
- Níveis de acesso (administrador e usuário comum)
- Monitoramento com Prometheus
- Interface web responsiva
- Banco de dados SQLite

## 📁 Estrutura do Projeto

```
app-user-registration/
├── .github/
│   └── workflows/           # Arquivos de configuração do GitHub Actions
│       ├── deploy-develop.yml
│       └── deploy-production.yml
├── scripts/                 # Scripts utilitários
│   ├── check_db.py         # Verificação do banco de dados
│   ├── entrypoint.sh       # Script de inicialização
│   ├── sync-branchs.sh     # Sincronização de branches
│   ├── test_login.py       # Testes de login
│   ├── test_login_admin.py # Testes de login admin
│   └── update_admin_password.py
├── static/
│   └── css/                # Arquivos de estilo
│       └── style.css
├── templates/              # Templates HTML
│   ├── login.html
│   ├── register.html
│   └── users.html
├── app.py                  # Aplicação principal
├── requirements.txt        # Dependências do projeto
├── Dockerfile             # Configuração do container
└── users.db               # Banco de dados SQLite
```

## 🌿 Branches

O projeto utiliza duas branches principais:

- `main`: Branch de produção, contendo código estável e testado
- `develop`: Branch de desenvolvimento, onde novas features são implementadas e testadas

### Fluxo de Trabalho

1. Todo desenvolvimento deve ser feito na branch `develop`
2. Pull requests devem ser criados para merge na `main`
3. Após aprovação e testes, o código é mesclado na `main`

## 🛠️ Configuração do Ambiente Local

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/app-user-registration.git
cd app-user-registration
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

5. Inicialize o banco de dados:
```bash
flask init-db
```

6. Execute a aplicação:
```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000`

### Usuário Administrador Padrão

Ao inicializar o banco de dados, um usuário administrador padrão é criado:
- Username: admin
- Senha: admin

⚠️ **Importante**: Altere a senha do administrador após o primeiro acesso em ambiente de produção.

## 🐳 Executando com Docker

1. Construa a imagem:
```bash
docker build -t user-registration-app .
```

2. Execute o container:
```bash
docker run -p 5000:5000 user-registration-app
```

## 📊 Monitoramento

A aplicação possui endpoints Prometheus para monitoramento:

- `/metrics`: Endpoint com métricas da aplicação

Métricas disponíveis:
- `login_count_total`: Número total de logins realizados
- `login_failed_count_total`: Número de tentativas de login falhas
- `registration_count_total`: Número de registros realizados

## 🔒 Segurança

- Todas as rotas sensíveis requerem autenticação
- Apenas administradores podem cadastrar novos usuários
- Usuários comuns só podem ver seus próprios dados
- Sessões são gerenciadas de forma segura

## 🚀 Deploy

O projeto utiliza GitHub Actions para CI/CD:

- `deploy-develop.yml`: Pipeline para ambiente de desenvolvimento
- `deploy-production.yml`: Pipeline para ambiente de produção

## 👥 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença especificada no arquivo [LICENSE.md](LICENSE.md).

## 🤝 Suporte

Para reportar bugs ou solicitar features, por favor abra uma issue no repositório.
