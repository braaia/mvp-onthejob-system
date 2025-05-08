import flet as ft
import pyrebase
from backend.temas import tema_claro, tema_escuro
from views.home import home_view
from views.login import login_view
from views.forgot import forgot_view
from views.register import register_view
from views.listacola import lista

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

    def login_route(page):
        global email_login, senha_login  # Torna as variáveis acessíveis globalmente
        email_login, senha_login, layout = login_view(page, btn_login)
        return layout

    def register_route(page):
        global email_register, senha_register  # Torna as variáveis acessíveis globalmente
        email_register, senha_register, layout = register_view(page, btn_register)
        return layout
    
    def forgot_route(page):
        global email_forgot
        email_forgot, layout = forgot_view(page, btn_forgot)
        return layout
    
    def home_route(page):
        global layout
        layout = home_view(page)
        return layout

    routes = {
        "/": home_route,
        "/login": login_route,
        "/register": register_route,
        "/forgot": forgot_route,
        "/lista_cola": lista,
    }

    # Login function - AUTHENTICATION LOGIC CAN BE MODIFIED
    import re

    def btn_login(e):
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
            auth.sign_in_with_email_and_password(email, password)
            page.open(ft.SnackBar(
                content=ft.Text(value="Logado com sucesso!", size=16, color='black', weight='bold', font_family='Arial', italic=True),
                bgcolor="green",
                duration=ft.Duration(seconds=2),
                show_close_icon=True,
                close_icon_color='black',
            ))
            page.go("/")
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
    
    def btn_register(e):
        global email_register, senha_register
        
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
        page.views.clear()

        if page.route not in routes:
            page.go("/login")
            return

        elif page.route in routes:
            page.views.append(routes[page.route](page))

        page.update()

    def view_pop(e):
        page.views.pop()
        page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go('/')

ft.app(target=main)