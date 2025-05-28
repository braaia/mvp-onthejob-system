import flet as ft

async def logout(page: ft.Page, e=None):
    try:
        from src.backend.auth import set_token
        set_token(None)
    except Exception:
        pass
    page.go('/login')
    page.open(ft.SnackBar(
        content=ft.Text(value="Logout realizado com sucesso!", size=16, color='black', weight='bold', font_family='Arial', italic=True),
        bgcolor="green",
        duration=ft.Duration(seconds=2),
        show_close_icon=True,
        close_icon_color='black',
    ))
    page.update()