import flet as ft

def loading_view():
    return ft.View(
        "/loading",
        controls=[
            ft.Column([
                ft.Text("Carregando...", size=20),
                ft.ProgressRing()
            ], 
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
            )
        ]
    )