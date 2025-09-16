import requests
import re

# URL base da aplicação
base_url = 'http://127.0.0.1:5000'

# Função para extrair o CSRF token do HTML (se existir)
def extract_csrf_token(html_content):
    csrf_match = re.search(r'<input[^>]*name="csrf_token"[^>]*value="([^"]+)"', html_content)
    if csrf_match:
        return csrf_match.group(1)
    return None

# Criar uma sessão para manter os cookies
session = requests.Session()

# Passo 1: Obter a página de login para capturar cookies e possível token CSRF
print("Obtendo página de login...")
login_page = session.get(f"{base_url}/login")
print(f"Status: {login_page.status_code}")

# Extrair token CSRF se existir
csrf_token = extract_csrf_token(login_page.text)
if csrf_token:
    print(f"Token CSRF encontrado: {csrf_token}")

# Preparar dados de login
login_data = {
    'username': 'admin',
    'password': 'admin123'
}

# Adicionar token CSRF se encontrado
if csrf_token:
    login_data['csrf_token'] = csrf_token

# Passo 2: Enviar requisição de login
print("\nEnviando requisição de login...")
login_response = session.post(
    f"{base_url}/login", 
    data=login_data,
    allow_redirects=False  # Não seguir redirecionamentos para analisar a resposta
)

print(f"Status: {login_response.status_code}")
print(f"Headers: {dict(login_response.headers)}")

# Verificar se houve redirecionamento (código 302)
if login_response.status_code == 302:
    redirect_url = login_response.headers.get('Location')
    print(f"Redirecionamento para: {redirect_url}")
    
    # Seguir o redirecionamento manualmente
    print("\nSeguindo redirecionamento...")
    redirect_response = session.get(f"{base_url}{redirect_url}")
    print(f"Status: {redirect_response.status_code}")
    print(f"URL final: {redirect_response.url}")
    
    # Verificar se chegamos à página de usuários
    if "/users" in redirect_response.url:
        print("\nLogin bem-sucedido! Chegamos à página de usuários.")
    else:
        print("\nFalha no login: Não chegamos à página de usuários.")
else:
    print("\nFalha no login: Não houve redirecionamento.")
    print(f"Conteúdo da resposta: {login_response.text[:500]}...")