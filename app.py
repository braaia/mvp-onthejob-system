import pyrebase
import flet as ft
import httpx
from src.backend.api import API_URL
from src.views import home, lista_cola, adminpage
from src.views.detalhes_atv import view_detalhe_atividade
from src.views.detalhes_cola import view_detalhes
from src.views.loginpage import login, forgot, register
from src.views.loadingpage.loading import loading_view
from src.backend.functions.temas import tema_claro, tema_escuro
from src.backend.auth import login_tokens, registrar_click, get_token

firebaseConfig = {
    'apiKey': "AIzaSyDHhIIK5DtHzk3rBmnjl9wEe-YyAVw6Gh0",
    'authDomain': "login-8c6e5.firebaseapp.com",
    'projectId': "logstoin-8c6e5",
    'storageBucket': "login-8c6e5.firebaserage.app",
    'databaseURL': "https://login.firebaseio.com",
    'messagingSenderId': "122238070396",
    'appId': "1:122238070396:web:481369b81774e5681b63f9",
    'measurementId': "G-E7LJQY1GE0"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

def main(page: ft.Page):

    page.title = 'On the Job'
    page.window.width = 1280
    page.window.height = 720
    page.window.maximizable = False
    page.window.resizable = False
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 0
    page.theme = tema_claro
    page.dark_theme = tema_escuro
    page.theme_mode = 'light'

    token = None
    
    def login_route(page):
        global email_login, senha_login  # Torna as variáveis acessíveis globalmente
        email_login, senha_login, layout = login.login_view(page, btn_login)
        return layout

    def register_route(page):
        global user_register, email_register, senha_register  # Torna as variáveis acessíveis globalmente
        user_register, email_register, senha_register, layout = register.register_view(page, btn_register)
        return layout
    
    def forgot_route(page):
        global email_forgot
        email_forgot, layout = forgot.forgot_view(page, btn_forgot)
        return layout
    
    def home_route(page):
        global layout
        layout = home.home_view(page)
        return layout

    routes = {
        "/": home_route,
        "/login": login_route,
        "/register": register_route,
        "/forgot": forgot_route,
        "/loading": loading_view,
        "/lista_cola": lista_cola.lista,
        "/admin": adminpage.admin,
    }

    # Login function - AUTHENTICATION LOGIC CAN BE MODIFIED
    import re
    async def btn_login(e):
        global email_login, senha_login
        
        email = email_login.value
        password = senha_login.value

        # Validação de email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            page.open(ft.SnackBar(
                content=ft.Text(value="Email inválido!", size=16, color='black', weight='bold', font_family='Arial', italic=True),
                bgcolor="red",
                duration=ft.Duration(seconds=2),
                show_close_icon=True,
                close_icon_color='black',
            ))
            return

        # Validação de senha
        if len(password) < 6:
            page.open(ft.SnackBar(
                content=ft.Text(value="A senha deve ter pelo menos 6 caracteres!", size=16, color='black', weight='bold', font_family='Arial', italic=True),
                bgcolor="red",
                duration=ft.Duration(seconds=2),
                show_close_icon=True,
                close_icon_color='black',
            ))
            return

        try:
            await login_tokens(email, password)

            auth.sign_in_with_email_and_password(email, password)

            page.open(ft.SnackBar(
                content=ft.Text(value="Logado com sucesso!", size=16, color='black', weight='bold', font_family='Arial', italic=True),
                bgcolor="green",
                duration=ft.Duration(seconds=2),
                show_close_icon=True,
                close_icon_color='black',
            ))
            
            async with httpx.AsyncClient() as client:
                r = await client.get(f"{API_URL}/me", headers={"Authorization": f"Bearer {get_token()}"})
                if r.status_code == 200:
                    dados = r.json()
                    if dados['cargo'] == 'admin':
                        page.go('/')
                    else:
                        page.go('/lista_cola')

            email = ''
            password = ''
            page.update()
        except:
            page.open(ft.SnackBar(
                content=ft.Text(value="Email ou senha inválidos!", size=16, color='black', weight='bold', font_family='Arial', italic=True),
                bgcolor="red",
                duration=ft.Duration(seconds=2),
                show_close_icon=True,
                close_icon_color='black',
            ))
            email = ''
            password = ''
            page.update()
    
    async def btn_register(e):
        global user_register, email_register, senha_register
        
        user = user_register.value
        email = email_register.value
        password = senha_register.value

        # Validação de email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            page.open(ft.SnackBar(
                content=ft.Text(value="Email inválido!", size=16, color='black', weight='bold', font_family='Arial', italic=True),
                bgcolor="red",
                duration=ft.Duration(seconds=2),
                show_close_icon=True,
                close_icon_color='black',
            ))
            return

        # Validação de senha
        if len(password) < 6:
            page.open(ft.SnackBar(
                content=ft.Text(value="A senha deve ter pelo menos 6 caracteres!", size=16, color='black', weight='bold', font_family='Arial', italic=True),
                bgcolor="red",
                duration=ft.Duration(seconds=2),
                show_close_icon=True,
                close_icon_color='black',
            ))
            return

        try:
            await registrar_click(user, email, password)

            auth.create_user_with_email_and_password(email, password)
            # Success notification - MESSAGE AND STYLING CAN BE CHANGED
            page.open(ft.SnackBar(
                content=ft.Text(value="Registrado com sucesso!", size=16, color='black', weight='bold', font_family='Arial', italic=True),
                bgcolor="green",
                duration=ft.Duration(seconds=2),
                show_close_icon=True,
                close_icon_color='black',
            ))
            page.go('/login')
            email = ''
            password = ''
            page.update()
        except:
            # Error notification - MESSAGE AND STYLING CAN BE CHANGED
            page.open(ft.SnackBar(
                content=ft.Text(value="Email ou senha inválidos!", size=16, color='black', weight='bold', font_family='Arial', italic=True),
                bgcolor="red",
                duration=ft.Duration(seconds=2),
                show_close_icon=True,
                close_icon_color='black',
            ))
            email = ''
            password = ''
            page.update()
            
    def btn_forgot(e):
        global email_forgot
        
        email = email_forgot.value

        # Validação de email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            page.open(ft.SnackBar(
                content=ft.Text(value="Email inválido!", size=16, color='black', weight='bold', font_family='Arial', italic=True),
                bgcolor="red",
                duration=ft.Duration(seconds=2),
                show_close_icon=True,
                close_icon_color='black',
            ))
            return

        try:
            auth.send_password_reset_email(email)
            # Success notification - MESSAGE AND STYLING CAN BE CHANGED
            page.open(ft.SnackBar(
                content=ft.Text(value="Email enviado com sucesso!", size=16, color='black', weight='bold', font_family='Arial', italic=True),
                bgcolor="green",
                duration=ft.Duration(seconds=2),
                show_close_icon=True,
                close_icon_color='black',
            ))
            page.go('/login')
            email = ''
            page.update()
        except:
            # Error notification - MESSAGE AND STYLING CAN BE CHANGED
            page.open(ft.SnackBar(
                content=ft.Text(value="Email inválido!", size=16, color='black', weight='bold', font_family='Arial', italic=True),
                bgcolor="red",
                duration=ft.Duration(seconds=2),
                show_close_icon=True,
                close_icon_color='black',
            ))
            email = ''
            page.update()

    def route_change(e):
        if page.route.startswith("/colaborador/"):
            parts = page.route.split("/")
            # Exemplo de rota: /colaborador/5/atividades/12
            if len(parts) >= 5 and parts[1] == "colaborador" and parts[2].isdigit() and parts[4].isdigit():
                colab_id = parts[2]
                atividade_id = parts[4]
                # Chame sua view de detalhes da atividade aqui, ex:
                page.views.append(view_detalhe_atividade(page, colab_id, atividade_id))
            elif len(parts) >= 3 and parts[1] == "colaborador" and parts[2].isdigit():
                colab_id = parts[2]
                page.views.append(view_detalhes(page, colab_id))
            else:
                page.go("/")
                return

        elif page.route not in routes:
            page.go("/")
            return

        elif page.route in routes:
            page.views.append(routes[page.route](page))

        page.update()

    page.on_route_change = route_change

    page.go('/login')

ft.app(target=main)