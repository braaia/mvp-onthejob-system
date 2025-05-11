import httpx

API_URL = "http://localhost:8000"

# Aqui você pode armazenar o token em memória
token = None
user_info = {}

async def registrar_click(email, password):
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{API_URL}/register", params={"email": email, "senha": password})
    if r.status_code == 200:
        return True, r.json()['msg']
    else:
        return False, r.json()['detail']

async def login_tokens(email, password):
    global token, user_info
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{API_URL}/login", data={"username": email, "password": password})
    if r.status_code == 200:
        token = r.json()["access_token"]
        user_info = get_me()
        return True, "Login bem-sucedido!"
    else:
        return False, r.json()["detail"]

def get_token():
    return token

async def get_me():
    if not token:
        return None
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{API_URL}/me", headers={"Authorization": f"Bearer {token}"})
    if r.status_code == 200:
        return r.json()
    return None
