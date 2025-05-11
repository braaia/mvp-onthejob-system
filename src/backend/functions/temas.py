# temas.py
import flet as ft


def theme_change(e):
    page = e.page
    page.theme_mode = "dark" if page.theme_mode == "light" else "light"
    page.update()


# Tema claro
tema_claro = ft.Theme(
    color_scheme=ft.ColorScheme(
        primary=ft.colors.BLACK,
        on_primary=ft.colors.WHITE,
        background=ft.colors.GREY_300,
        on_background=ft.colors.BLACK,
        surface=ft.colors.WHITE,
        on_surface=ft.colors.BLACK,
    )
)

# Tema escuro
tema_escuro = ft.Theme(
    color_scheme=ft.ColorScheme(
        primary=ft.colors.WHITE,
        on_primary=ft.colors.BLACK,
        background=ft.colors.BLACK,
        on_background=ft.colors.WHITE,
        surface=ft.colors.BLACK,
        on_surface=ft.colors.WHITE,
    )
)
