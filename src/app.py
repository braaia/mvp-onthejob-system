import flet as ft
from temas import tema_claro, tema_escuro
# from views.home import home_view
from views.login import login_view
from views.forgot import forgot_view
from views.register import register_view

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

    routes = {
        "/login": login_view,
        "/forgot": forgot_view,
        "/register": register_view,
        # "/": home_view,
    }

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

    page.go(page.route)

ft.app(target=main)