import flet as ft
import httpx
from views.loadingpage.loading import loading_view

API_URL = "http://localhost:8000"

def lista(page: ft.Page):
    def theme_change(e):
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        page.update()

    list = ft.Column(scroll=ft.ScrollMode.AUTO)

    async def carregar_colaboradores():
        # Mostra a tela de loading
        page.views.clear()
        page.views.append(loading_view())
        page.update()

        try:
            # Faz a requisição para a API
            async with httpx.AsyncClient() as client:
                r = await client.get(f"{API_URL}/colaboradores")
                colaboradores = r.json()

            list.controls.clear()

            for colab in colaboradores:
                card = ft.Container(
                    content=ft.Column(
                        alignment='center',
                        horizontal_alignment='center',
                        controls=[
                            ft.Text(f"Nome: {colab['colaborador']}"),
                            ft.Text(f"Cargo: {colab['cargo']}"),
                            ft.Text(f"Gestor: {colab['nome_gestor']}"),
                            ft.ElevatedButton(
                                "Ver Detalhes",
                                on_click=lambda e, cid=colab['id']: page.go(f"/colaborador/{cid}/atividades")
                            )
                        ]),
                    padding=10,
                    border=ft.border.all(1),
                    border_radius=10,
                    margin=5
                )
                list.controls.append(card)

        except Exception as e:
            list.controls.append(ft.Text(f"Erro ao carregar colaboradores: {str(e)}"))

        # Atualiza a página com os dados carregados
        page.views.clear()
        page.views.append(layout)
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
                            ft.PopupMenuItem('USER', on_click=lambda _: print("User")),
                            ft.PopupMenuItem(),
                            ft.PopupMenuItem('Formulário', on_click=lambda _: page.go("/"))
                        ]
                    ),
                    ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED, icon_color=ft.colors.SURFACE, on_click=theme_change),
                ]
            ),
            list,
        ]
    )

    page.run_task(carregar_colaboradores)

    return layout