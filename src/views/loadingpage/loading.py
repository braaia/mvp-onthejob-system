import flet as ft

def loading_view():
    return ft.View(
        "/loading",
        vertical_alignment='center',
        horizontal_alignment='center',
        controls=[
            ft.Column([
                ft.Text("Carregando...", size=20),
                ft.ProgressRing()
            ], 
            alignment='center',
            horizontal_alignment='center',
            expand=True
            )
        ]
    )