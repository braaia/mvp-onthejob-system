# temas.py
import flet as ft


def theme_change(e):
    page = e.page
    page.theme_mode = "dark" if page.theme_mode == "light" else "light"
    page.update()


# Tema claro
tema_claro = ft.Theme(
    color_scheme=ft.ColorScheme(
        primary=ft.Colors.BLACK,
        on_primary=ft.Colors.WHITE,
        background=ft.Colors.GREY_300,
        on_background=ft.Colors.BLACK,
        surface=ft.Colors.WHITE,
        on_surface=ft.Colors.BLACK,
    )
)

# Tema escuro
tema_escuro = ft.Theme(
    color_scheme=ft.ColorScheme(
        primary=ft.Colors.WHITE,
        on_primary=ft.Colors.BLACK,
        background=ft.Colors.BLACK,
        on_background=ft.Colors.WHITE,
        surface=ft.Colors.BLACK,
        on_surface=ft.Colors.WHITE,
    )
)
