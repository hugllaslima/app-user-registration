# Sistema de Registro de Usuários

Este é um sistema de registro e gerenciamento de usuários desenvolvido em Flask, com suporte a diferentes níveis de acesso (administrador e usuário comum) e métricas Prometheus para monitoramento.

**🎯 Projeto Educacional para DevOps**  
Este projeto foi especialmente preparado para estudantes que estão iniciando na carreira de DevOps, oferecendo exemplos práticos de CI/CD, containerização, monitoramento e boas práticas de segurança.

## 🚀 Funcionalidades

- Sistema de autenticação completo (login/logout) com hash de senhas
- Gerenciamento de usuários (cadastro, visualização)
- Níveis de acesso (administrador e usuário comum)
- Monitoramento com Prometheus
- Interface web responsiva
- Banco de dados SQLite
- Configuração via variáveis de ambiente
- CI/CD com GitHub Actions
- Containerização com Docker

## 📁 Estrutura do Projeto

```
app-user-registration/
├── .github/
│   └── workflows/                  # Arquivos de configuração do GitHub Actions
│       ├── deploy-develop.yml
│       └── deploy-production.yml
├── scripts/                        # Scripts utilitários
│   ├── check_db.py                 # Verificação do banco de dados
│   ├── entrypoint.sh               # Script de inicialização
│   ├── sync-branchs.sh             # Sincronização de branches
│   ├── test_login.py               # Testes de login
│   ├── test_login_admin.py         # Testes de login admin
│   └── update_admin_password.py    # Atualização da senha do admin
├── static/
│   └── css/                        # Arquivos de estilo
│       └── style.css
├── templates/                      # Templates HTML
│   ├── login.html
│   ├── register.html
│   └── users.html
├── app.py                          # Aplicação principal
├── requirements.txt                # Dependências do projeto
├── Dockerfile                      # Configuração do container
└── users.db                        # Banco de dados SQLite
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
- Docker (opcional, para execução em container)

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

5. **Configure as variáveis de ambiente:**
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env com suas configurações
# IMPORTANTE: Altere pelo menos a FLASK_SECRET_KEY e ADMIN_PASSWORD
```

6. Inicialize o banco de dados:
```bash
flask init-db
```

7. Execute a aplicação:
```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000`

### ⚠️ Configurações de Segurança Importantes

**Para Ambiente de Desenvolvimento:**
- Mantenha `FLASK_DEBUG=True` no arquivo `.env`
- Use `SESSION_COOKIE_SECURE=False` (HTTP local)

**Para Ambiente de Produção:**
- **OBRIGATÓRIO**: Altere `FLASK_SECRET_KEY` para uma chave única e segura
- **OBRIGATÓRIO**: Altere `ADMIN_PASSWORD` para uma senha forte
- Configure `FLASK_DEBUG=False`
- Configure `SESSION_COOKIE_SECURE=True` (HTTPS obrigatório)

### Usuário Administrador Padrão

Ao inicializar o banco de dados, um usuário administrador é criado automaticamente usando as variáveis de ambiente:
- Username: Definido em `ADMIN_USERNAME` (padrão: admin)
- Senha: Definida em `ADMIN_PASSWORD` (padrão: admin123)
- Email: Definido em `ADMIN_EMAIL`
- Nome Completo: Definido em `ADMIN_FULLNAME`
- Telefone: Definido em `ADMIN_PHONE`

#### 🔄 Sincronização Automática de Senha

**NOVA FUNCIONALIDADE**: A aplicação agora sincroniza automaticamente a senha do administrador com as variáveis de ambiente a cada inicialização do container:

- **Se o usuário admin não existir**: Será criado com as credenciais das variáveis de ambiente
- **Se o usuário admin já existir**: A senha será automaticamente atualizada para corresponder à variável `ADMIN_PASSWORD`
- **Dados atualizados**: Nome completo, telefone e email também são sincronizados

Isso garante que mudanças nas variáveis de ambiente sejam refletidas no banco de dados, eliminando problemas de autenticação após deploys.

⚠️ **CRÍTICO**: Sempre altere a senha padrão antes de usar em produção!

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

A aplicação possui endpoints Prometheus para monitoramento em tempo real:

### Endpoints Disponíveis
- `/metrics`: Endpoint principal com todas as métricas da aplicação

### Métricas Coletadas
- `login_count_total`: Número total de logins realizados com sucesso
- `login_failed_count_total`: Número de tentativas de login que falharam
- `registration_count_total`: Número de novos usuários registrados
- `app_info`: Informações gerais da aplicação (versão, etc.)

### Como Usar o Monitoramento

1. **Acesse as métricas diretamente:**
   ```bash
   curl http://localhost:5000/metrics
   ```

2. **Configure o Prometheus** (arquivo `prometheus.yml`):
   ```yaml
   scrape_configs:
     - job_name: 'user-registration-app'
       static_configs:
         - targets: ['localhost:5000']
       metrics_path: '/metrics'
       scrape_interval: 15s
   ```

3. **Dashboards sugeridos para Grafana:**
   - Taxa de logins por minuto
   - Percentual de logins falhados
   - Crescimento de usuários registrados
   - Uptime da aplicação

### 🔍 Exemplo de Métricas
```
# HELP login_count_total Número de logins realizados
# TYPE login_count_total counter
login_count_total 42.0

# HELP login_failed_count_total Número de logins falhos
# TYPE login_failed_count_total counter
login_failed_count_total 3.0

# HELP registration_count_total Número de registros realizados
# TYPE registration_count_total counter
registration_count_total 15.0
```

## 🔒 Segurança

Este projeto implementa várias camadas de segurança essenciais para aplicações web:

### Autenticação e Autorização
- ✅ **Hash de senhas**: Todas as senhas são armazenadas com hash usando Werkzeug
- ✅ **Validação de entrada**: Campos obrigatórios e validação de tamanho de senha
- ✅ **Controle de acesso**: Apenas administradores podem cadastrar novos usuários
- ✅ **Sessões seguras**: Configuração adequada de cookies de sessão

### Configuração Segura
- ✅ **Variáveis de ambiente**: Secrets e configurações sensíveis via `.env`
- ✅ **Secret key dinâmica**: Chave secreta configurável via ambiente
- ✅ **Debug desabilitado**: Modo debug controlado por variável de ambiente
- ✅ **Cookies seguros**: HTTPOnly e SameSite configurados

### Banco de Dados
- ✅ **Queries parametrizadas**: Proteção contra SQL Injection
- ✅ **Validação de integridade**: Constraints de unicidade no banco

### Infraestrutura
- ✅ **Containers isolados**: Aplicação executada em containers Docker
- ✅ **Secrets no CI/CD**: Credenciais AWS armazenadas como GitHub Secrets
- ✅ **Princípio do menor privilégio**: Usuários com permissões mínimas necessárias

### ⚠️ Recomendações Adicionais para Produção

**Implementar em produção:**
- [ ] HTTPS obrigatório (TLS/SSL)
- [ ] Rate limiting para login
- [ ] Logs de auditoria
- [ ] Backup automático do banco
- [ ] Monitoramento de segurança
- [ ] Firewall de aplicação web (WAF)
- [ ] Rotação regular de secrets

**Nunca fazer:**
- ❌ Commitar arquivos `.env` no repositório
- ❌ Usar senhas padrão em produção
- ❌ Executar com debug=True em produção
- ❌ Expor métricas sem autenticação em produção

## 🚀 Deploy e CI/CD

O projeto utiliza GitHub Actions para CI/CD automatizado com duas pipelines:

### Pipelines Disponíveis

- **`deploy-develop.yml`**: Pipeline para ambiente de desenvolvimento
  - Trigger: Push na branch `develop`
  - Executa em: Self-hosted runner com label `develop-runner`
  - Deploy: Container local na porta 80

- **`deploy-production.yml`**: Pipeline para ambiente de produção
  - Trigger: Push na branch `main`
  - Executa em: Self-hosted runner com label `production-runner`
  - Deploy: AWS ECR + Container local

### 🔧 Configuração de Self-Hosted Runners

Para que os workflows funcionem, você precisa configurar Self-Hosted Runners no GitHub:

#### 1. Acesse as Configurações do Repositório
- Vá para `Settings` > `Actions` > `Runners`
- Clique em `New self-hosted runner`

#### 2. Configure o Runner de Desenvolvimento
```bash
# No servidor de desenvolvimento
mkdir actions-runner && cd actions-runner

# Baixe o runner (substitua pela versão mais recente)
curl -o actions-runner-linux-x64-2.311.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz

# Extraia o arquivo
tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz

# Configure o runner
./config.sh --url https://github.com/SEU-USUARIO/app-user-registration --token SEU-TOKEN

# Adicione a label 'develop-runner' durante a configuração
# Quando perguntado sobre labels, digite: develop-runner

# Execute o runner
./run.sh
```

#### 3. Configure o Runner de Produção
```bash
# No servidor de produção
mkdir actions-runner && cd actions-runner

# Repita os passos acima, mas use a label 'production-runner'
# Durante a configuração, adicione a label: production-runner
```

#### 4. Configuração de Secrets para Produção

No GitHub, vá para `Settings` > `Secrets and variables` > `Actions` e adicione:

```
AWS_ACCESS_KEY_ID=sua-access-key
AWS_SECRET_ACCESS_KEY=sua-secret-key
AWS_REGION=us-east-1
AWS_ECR_REGISTRY=123456789012.dkr.ecr.us-east-1.amazonaws.com
AWS_ECR_REPOSITORY=app-user-registration
```

#### 5. Pré-requisitos nos Servidores

**Servidor de Desenvolvimento:**
- Docker instalado
- Usuário com permissões para executar Docker

**Servidor de Produção:**
- Docker instalado
- AWS CLI configurado
- Usuário com permissões para Docker e sudo

### 📋 Checklist de Deploy

**Antes do primeiro deploy:**
- [ ] Self-hosted runners configurados e rodando
- [ ] Secrets do AWS configurados (produção)
- [ ] Variáveis de ambiente configuradas nos servidores
- [ ] Portas 80 liberadas nos firewalls
- [ ] Repositório ECR criado na AWS (produção)

**Para cada deploy:**
- [ ] Código testado localmente
- [ ] Variáveis de ambiente atualizadas se necessário
- [ ] Runners online e funcionando

## 📝 Mudanças Recentes

### Versão 1.1.0 - Sincronização Automática do Admin
- **Nova funcionalidade**: A senha do usuário administrador agora é sincronizada automaticamente com as variáveis de ambiente a cada inicialização
- **Correção crítica**: Eliminado problema de autenticação após mudanças nas variáveis de ambiente
- **Melhoria**: Dados do admin (nome, telefone, email) também são atualizados automaticamente

### Como Fazer Commit das Alterações
```bash
# Adicionar arquivos modificados
git add app.py README.md

# Commit com mensagem descritiva
git commit -m "feat: implementa sincronização automática da senha do admin"

# Push para o repositório
git push origin main
```

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
