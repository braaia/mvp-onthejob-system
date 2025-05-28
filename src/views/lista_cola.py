import flet as ft
import httpx, asyncio
from src.backend.api import API_URL
from functools import partial
from src.backend.functions.logout import logout
from src.views.loadingpage.loading import loading_view
from src.backend.functions.temas import theme_change
from src.backend.functions.formatting import hover
from src.backend.auth import get_me, get_token

def lista(page: ft.Page):
    page.scroll = ft.ScrollMode.AUTO

    list = ft.Row(
        wrap=True,
        spacing=20,
        run_spacing=20,
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        width=page.window.width,
    )
    
    user_name = ft.Text("Carregando...")  # Placeholder

    async def carregar_nome_usuario():
        nome = "Desconhecido"
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(f"{API_URL}/me", headers={"Authorization": f"Bearer {get_token()}"} )
                if r.status_code == 200:
                    dados = r.json()
                    nome = dados.get("user", "Desconhecido")
        except Exception as e:
            nome = "Erro"
        user_name.value = nome
        page.update()

    # Chame a função para carregar o nome ao abrir a home
    asyncio.run(carregar_nome_usuario())

    popup_items = [
        ft.PopupMenuItem(content=user_name, on_click=lambda _: print(user_name)),
        ft.PopupMenuItem(),
        ft.PopupMenuItem('Sair', on_click=lambda e: page.run_task(partial(logout, page, e)))
    ]

    async def popmenu():
        dados = await get_me()  # Tenta obter os dados do usuário autenticado

        if dados and dados['cargo'] == 'admin':
            popup_items.extend([
                ft.PopupMenuItem(),
                ft.PopupMenuItem('Formulário', on_click=lambda _: page.go("/")),
                ft.PopupMenuItem('Admin', on_click=lambda _: page.go('/admin')),
            ])
        return popup_items


    async def carregar_colaboradores():
        # Mostra a tela de loading
        page.views.clear()
        page.views.append(loading_view())
        page.update()

        try:
            # Faz a requisição para a API
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    f"{API_URL}/colaboradores",
                    headers={"Authorization": f"Bearer {get_token()}"}
                )
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
                                "Ver Detalhes", color=ft.Colors.SURFACE, bgcolor=ft.Colors.ON_SURFACE, on_hover=hover,
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
                leading=ft.IconButton(ft.Icons.HOME, icon_color=ft.Colors.SURFACE),
                leading_width=50,
                toolbar_height=70,
                title=ft.Text("Lista de Colaboradores",size=32, color=ft.Colors.SURFACE),
                center_title=False,
                bgcolor=ft.Colors.ON_SURFACE,
                actions=[
                    ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED, icon_color=ft.Colors.SURFACE, on_click=theme_change),
                    ft.PopupMenuButton(
                        icon=ft.Icons.LIST,
                        icon_color=ft.Colors.SURFACE,
                        items=popup_items
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
    page.run_task(popmenu)

    return layout