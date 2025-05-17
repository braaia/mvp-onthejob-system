import flet as ft
import httpx, asyncio
from backend.api import API_URL
from backend.auth import get_me, get_token
from backend.functions.temas import theme_change

def view_detalhe_atividade(page: ft.Page, cid, atvid):

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
        ft.PopupMenuItem('Lista de Colaboradores', on_click=lambda _: page.go("/lista_cola")),
    ]

    layout = ft.View(
        f"/colaborador/{cid}/atividades/{atvid}",
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.AppBar(
                leading=ft.IconButton(ft.Icons.HOME, icon_color=ft.Colors.SURFACE),
                leading_width=50,
                toolbar_height=70,
                title=ft.Text(f"Detalhes da Atividade {atvid} do Colaborador {cid}", size=32, color=ft.Colors.SURFACE),
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
        ]
    )

    return layout