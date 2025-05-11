import flet as ft
import httpx
from views.loadingpage.loading import loading_view
from backend.functions.temas import theme_change
from backend.functions.formatting import hover

API_URL = "http://localhost:8000"

def lista(page: ft.Page):
    page.scroll = ft.ScrollMode.AUTO

    list = ft.Row(
        wrap=True,
        spacing=20,
        run_spacing=20,
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        width=page.window.width,
    )

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
                            ft.Text(f"Admissão: {colab['data_adm'][:10]}"),
                            ft.ElevatedButton(
                                "Ver Detalhes", color=ft.colors.SURFACE, bgcolor=ft.colors.ON_SURFACE, on_hover=hover,
                                on_click=lambda e, cid=colab['id']: page.go(f"/colaborador/{cid}/atividades")
                            )
                        ]),
                    width=370,
                    height=175,
                    border=ft.border.all(1),
                    border_radius=10,
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
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.AppBar(
                leading=ft.IconButton(ft.Icons.HOME, icon_color=ft.colors.SURFACE, on_click=lambda e: page.go("/")),
                leading_width=50,
                toolbar_height=70,
                title=ft.Text("Lista de Colaboradores",size=32, color=ft.Colors.SURFACE),
                center_title=False,
                bgcolor=ft.Colors.ON_SURFACE,
                actions=[
                    ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED, icon_color=ft.colors.SURFACE, on_click=theme_change),
                    ft.PopupMenuButton(
                        icon=ft.Icons.LIST,
                        icon_color=ft.colors.SURFACE,
                        items=[
                            ft.PopupMenuItem('USER', on_click=lambda _: print("User")),
                            ft.PopupMenuItem(),
                            ft.PopupMenuItem('Formulário', on_click=lambda _: page.go("/"))
                        ]
                    ),
                ]
            ),
            ft.Container(
                padding=ft.padding.only(top=20, bottom=20),
                content=list,
            )
        ]
    )

    page.run_task(carregar_colaboradores)

    return layout