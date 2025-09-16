import requests
import re

BASE_URL = 'http://127.0.0.1:5000'

def test_login():
    print("Obtendo página de login...")
    # Obter a página de login para pegar o token CSRF se existir
    session = requests.Session()
    response = session.get(f"{BASE_URL}/login")
    print(f"Status: {response.status_code}")
    
    # Extrair token CSRF se existir
    csrf_token = None
    if 'csrf_token' in response.text:
        match = re.search(r'<input[^>]*name="csrf_token"[^>]*value="([^"]+)"', response.text)
        if match:
            csrf_token = match.group(1)
            print(f"CSRF Token encontrado: {csrf_token}")
    
    # Preparar dados de login
    login_data = {
        'username': 'admin',
        'password': 'admin'
    }
    
    # Adicionar token CSRF se encontrado
    if csrf_token:
        login_data['csrf_token'] = csrf_token
    
    print("\nEnviando requisição de login...")
    # Enviar requisição de login
    response = session.post(
        f"{BASE_URL}/login", 
        data=login_data,
        allow_redirects=False  # Não seguir redirecionamentos automaticamente
    )
    
    print(f"Status: {response.status_code}")
    print(f"Headers: {response.headers}")
    
    # Verificar se houve redirecionamento (código 302)
    if response.status_code == 302:
        redirect_url = response.headers.get('Location')
        print(f"Redirecionamento para: {redirect_url}")
        
        # Seguir o redirecionamento manualmente
        print("\nSeguindo redirecionamento...")
        response = session.get(f"{BASE_URL}{redirect_url}")
        print(f"Status: {response.status_code}")
        print(f"URL final: {response.url}")
        
        # Verificar se chegamos à página de usuários
        if "/users" in response.url and response.status_code == 200:
            print("\nLogin bem-sucedido! Chegamos à página de usuários.")
            return True
        else:
            print("\nFalha no login! Não chegamos à página de usuários.")
            print(f"Conteúdo da resposta: {response.text[:200]}...")
            return False
    else:
        print("\nFalha no login! Não houve redirecionamento.")
        print(f"Conteúdo da resposta: {response.text[:200]}...")
        return False

if __name__ == "__main__":
    test_login()