import flet as ft
import httpx, asyncio
from backend.api import API_URL
from backend.functions import temas
from backend.auth import get_token

def admin(page: ft.Page):
    alvo_email = ft.TextField(label="Email do usuário", border_color=ft.Colors.ON_SURFACE)
    cargo_alvo = ft.Dropdown(
        label="Novo cargo",
        options=[
            ft.dropdown.Option("admin"),
            ft.dropdown.Option("colaborador"),
        ],
        value="admin"
    )
    status = ft.Text()

    async def mudar_cargo_click(e):
        if not get_token():
            status.value = "Você precisa estar logado."
            page.update()
            return

        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"{API_URL}/set_cargo",
                params={"target_email": alvo_email.value, "novo_cargo": cargo_alvo.value},
                headers={"Authorization": f"Bearer {get_token()}"}
            )
            if r.status_code == 200:
                status.value = r.json()["msg"]
            else:
                status.value = f"Erro: {r.json()['detail']}"
            page.update()
    
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
    
    layout = ft.View(
        "/admin",
        controls=[
            ft.AppBar(
                leading=ft.IconButton(ft.Icons.HOME, icon_color=ft.Colors.SURFACE, on_click=lambda e: page.go("/")),
                leading_width=50,
                toolbar_height=70,
                title=ft.Text("ADMIN",size=32, color=ft.Colors.SURFACE),
                center_title=False,
                bgcolor=ft.Colors.ON_SURFACE,
                actions=[
                    ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED, icon_color=ft.Colors.SURFACE, on_click=temas.theme_change),
                    ft.PopupMenuButton(
                        icon=ft.Icons.LIST, 
                        icon_color=ft.Colors.SURFACE,
                        items=[
                            ft.PopupMenuItem(content=user_name, on_click=lambda _: print(user_name)),
                            ft.PopupMenuItem(),
                            ft.PopupMenuItem('Lista de Colaboradores', on_click=lambda _: page.go("/lista_cola")),
                            ft.PopupMenuItem('Formulário', on_click=lambda _: page.go('/')),
                        ]
                    ),
                ],
            ),
            alvo_email,
            cargo_alvo,
            status,
            ft.ElevatedButton("Alterar Cargo", on_click=mudar_cargo_click),
        ]
    )

    return layout