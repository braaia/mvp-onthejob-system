import flet as ft

def lista(page: ft.Page):

    def theme_change(e):
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        page.update()

    layout = ft.View(
        '/lista_cola',
        vertical_alignment='center',
        horizontal_alignment='center',
        controls=[
            ft.AppBar(
                leading=ft.Icon(ft.Icons.HOME, color=ft.colors.SURFACE),
                leading_width=50,
                toolbar_height=70,
                title=ft.Text("Lista de Colaboradores",size=32, color=ft.Colors.SURFACE),
                center_title=False,
                bgcolor=ft.Colors.ON_SURFACE,
                actions=[
                    ft.PopupMenuButton(
                        icon=ft.Icons.LIST, 
                        icon_color=ft.colors.SURFACE,
                        items=[
                            ft.PopupMenuItem('Formulário', on_click=lambda _: page.go("/"))
                        ]
                    ),
                    ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED, icon_color=ft.colors.SURFACE, on_click=theme_change),
                ]
            )
        ]
    )

    return layout