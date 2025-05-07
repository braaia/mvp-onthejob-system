import flet as ft

def hover(e):
        if e.data == "true":
            e.control.scale = 1.06  # Scale up on hover
            e.control.opacity = 0.8  # Slightly transparent on hover
        else:
            e.control.scale = 1.0  # Normal scale
            e.control.opacity = 1.0  # Full opacity
        e.control.update()

def forgot_view(page: ft.Page):
    
    email = ft.TextField(
        expand=True,
        border_color='transparent',
        hint_text='Email',
        color=ft.colors.ON_BACKGROUND,
        hint_style=ft.TextStyle(color=ft.colors.ON_BACKGROUND),
        content_padding=0
    )

    return ft.View(
        "/login",
        vertical_alignment='center',
        horizontal_alignment='center',
        controls=[
            ft.Container(
                bgcolor=ft.colors.ON_BACKGROUND,
                width=400,
                height=400,
                border_radius=24,
                shadow=ft.BoxShadow(blur_radius=18, color=ft.Colors.with_opacity(0.8, ft.colors.ON_BACKGROUND)),
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
                                    color=ft.colors.SURFACE,
                                    size=38,
                                    weight='bold',
                                    font_family='MontSerrat'
                                )
                            ),
                            ft.Container(
                                width=250,
                                height=50,
                                bgcolor=ft.colors.SURFACE,
                                padding=10,
                                alignment=ft.alignment.center_left,
                                border_radius=8,
                                content=ft.Row([
                                    ft.Container(
                                        content=ft.Icon(
                                            name=ft.Icons.EMAIL,
                                            color=ft.colors.ON_BACKGROUND,
                                        )
                                    ),
                                    ft.VerticalDivider(
                                        width=1,
                                        color=ft.colors.ON_BACKGROUND
                                    ),
                                    email
                                ])
                            ),
                            ft.Container(
                                content=ft.ElevatedButton(
                                    text='Enviar email',
                                    width=250,
                                    height=50,
                                    # on_click=signin,
                                    on_hover=hover
                                ),
                            ),
                            ft.IconButton(
                                icon=ft.Icons.NAVIGATE_BEFORE,
                                icon_color=ft.colors.ON_BACKGROUND,
                                bgcolor=ft.colors.SURFACE,
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