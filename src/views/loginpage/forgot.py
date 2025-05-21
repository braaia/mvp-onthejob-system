import flet as ft
from src.backend.functions.formatting import hover

def forgot_view(page: ft.Page, forgot):
    
    email = ft.TextField(
        expand=True,
        border_color='transparent',
        hint_text='Email',
        color=ft.Colors.PRIMARY,
        hint_style=ft.TextStyle(color=ft.Colors.PRIMARY),
        content_padding=0
    )

    forgot_layout = ft.View(
        "/forgot",
        vertical_alignment='center',
        horizontal_alignment='center',
        controls=[
            ft.Container(
                bgcolor=ft.Colors.PRIMARY,
                width=400,
                height=450,
                border_radius=24,
                shadow=ft.BoxShadow(blur_radius=18, color=ft.Colors.with_opacity(0.8, ft.Colors.PRIMARY)),
                content=ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Column(
                        spacing=15,
                        horizontal_alignment='center',
                        alignment='center',
                        controls=[
                            ft.Container(
                                ft.Text(
                                    "Redefinir senha",
                                    color=ft.Colors.SURFACE,
                                    size=38,
                                    weight='bold',
                                    font_family='MontSerrat'
                                )
                            ),
                            ft.Container(
                                width=250,
                                height=50,
                                bgcolor=ft.Colors.SURFACE,
                                padding=10,
                                alignment=ft.alignment.center_left,
                                border_radius=8,
                                content=ft.Row([
                                    ft.Container(
                                        content=ft.Icon(
                                            name=ft.Icons.EMAIL,
                                            color=ft.Colors.PRIMARY,
                                        )
                                    ),
                                    ft.VerticalDivider(
                                        width=1,
                                        color=ft.Colors.PRIMARY
                                    ),
                                    email
                                ])
                            ),
                            ft.Container(
                                content=ft.ElevatedButton(
                                    text='Enviar email',
                                    width=250,
                                    height=50,
                                    on_click=forgot,
                                    on_hover=hover
                                ),
                            ),
                            ft.IconButton(
                                icon=ft.Icons.NAVIGATE_BEFORE,
                                icon_color=ft.Colors.PRIMARY,
                                bgcolor=ft.Colors.SURFACE,
                                width=50,
                                height=50,
                                on_click=lambda _: page.go('/login')
                            )
                        ]
                    )
                )
            )
        ]
    )
    
    return email, forgot_layout