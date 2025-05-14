import flet as ft
from backend.functions.formatting import hover

def register_view(page: ft.Page, signup):
    
    user = ft.TextField(
        expand=True,
        border_color='transparent',
        hint_text='Usuário',
        color=ft.Colors.PRIMARY,
        hint_style=ft.TextStyle(color=ft.Colors.PRIMARY),
        content_padding=0
    )           

    email = ft.TextField(
        expand=True,
        border_color='transparent',
        hint_text='Email',
        color=ft.Colors.PRIMARY,
        hint_style=ft.TextStyle(color=ft.Colors.PRIMARY),
        content_padding=0
    )           

    senha = ft.TextField(
        expand=True,
        password=True,
        can_reveal_password=True,
        border_color='transparent',
        hint_text='Senha',
        color=ft.Colors.PRIMARY,
        hint_style=ft.TextStyle(color=ft.Colors.PRIMARY),
        content_padding=0
    )

    register_layout = ft.View(
        "/register",
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
                                    "Criar conta",
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
                                            name=ft.Icons.PERSON,
                                            color=ft.Colors.PRIMARY,
                                        )
                                    ),
                                    ft.VerticalDivider(
                                        width=1,
                                        color=ft.Colors.PRIMARY
                                    ),
                                    user
                                ])
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
                                width=250,
                                height=50,
                                bgcolor=ft.Colors.SURFACE,
                                padding=10,
                                alignment=ft.alignment.center_left,
                                border_radius=8,
                                content=ft.Row([
                                    ft.Container(
                                        content=ft.Icon(
                                            name=ft.Icons.LOCK,
                                            color=ft.Colors.PRIMARY,
                                        )
                                    ),
                                    ft.VerticalDivider(
                                        width=1,
                                        color=ft.Colors.PRIMARY
                                    ),
                                    senha
                                ])
                            ),
                            ft.Container(
                                width=250,
                                alignment=ft.alignment.center_right,
                                content=ft.Text('Esqueceu a senha?', color='#ef233c', weight='bold', size=16),
                                on_click=lambda _: page.go('/forgot')
                            ),
                            ft.Container(
                                content=ft.ElevatedButton(
                                    text='Registrar',
                                    width=250,
                                    height=50,
                                    on_click=signup,
                                    on_hover=hover
                                ),
                            ),
                            ft.Container(
                                content=ft.Row(
                                    alignment='center',
                                    controls=[
                                    ft.Text(
                                        'Já possui cadastro?',
                                        size=16,
                                        color=ft.Colors.SURFACE,
                                        weight='w320',
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            'Entrar',
                                            color='#ef233c',
                                            size=16,
                                            weight='bold'
                                        ),
                                        on_click=lambda _: page.go('/login')
                                    )
                                ])
                            )
                        ]
                    )
                )
            )
        ]
    )
    
    return user, email, senha, register_layout