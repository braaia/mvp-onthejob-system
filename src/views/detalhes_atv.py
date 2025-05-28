import flet as ft
import httpx, asyncio, webbrowser
from src.views.loadingpage.loading import loading_view
from src.backend.api import API_URL
from src.backend.auth import get_me, get_token
from src.backend.functions.formatting import hover
from src.backend.functions.temas import theme_change
from functools import partial
from src.backend.functions.logout import logout

def view_detalhe_atividade(page: ft.Page, cid: int, atvid: int):

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

    nome_colaborador = ft.Text("Carregando...")

    async def carregar_nome_colaborador():
        nome = "Carregando..."
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(f"{API_URL}/colaboradores/{cid}", headers={"Authorization": f"Bearer {get_token()}"} )
                if r.status_code == 200:
                    dados = r.json()
                    if isinstance(dados, list) and len(dados) > 0:
                            nome = dados[0].get("colaborador", "Desconhecido")
                    else:
                        nome = "Desconhecido"
        except Exception as e:
            nome = "Erro"
        nome_colaborador.value = nome
        page.update()
    
    asyncio.run(carregar_nome_colaborador())

    popup_items = [
        ft.PopupMenuItem(content=user_name, on_click=lambda _: print(user_name)),
        ft.PopupMenuItem(),
        ft.PopupMenuItem('Lista de Colaboradores', on_click=lambda _: page.go("/lista_cola")),
        ft.PopupMenuItem(),
        ft.PopupMenuItem('Sair', on_click=lambda e: page.run_task(partial(logout, page, e)))
    ]

    chk_colab = ft.Checkbox(label="Assinatura do colaborador")
    chk_gestor = ft.Checkbox(label="Assinatura do gestor", visible=False)

    async def handle_admin():
        dados = await get_me()  # Tenta obter os dados do usuário autenticado

        if dados and dados['cargo'] == 'admin':
            popup_items.extend([
                ft.PopupMenuItem(),
                ft.PopupMenuItem('Formulário', on_click=lambda _: page.go("/")),
                ft.PopupMenuItem('Admin', on_click=lambda _: page.go('/admin')),
            ])

            chk_gestor.visible = True
            chk_colab.visible = False
            page.update()

        return popup_items

    status = ft.Text(color=ft.Colors.RED)
    atividades = ft.Container(expand=True)
    comentario_field = ft.TextField(label="Adicione um comentário")
    status_atividade = ft.Dropdown(
        label="Atualize o Status da Atividade",
        options=[
            ft.dropdown.Option("Concluída"),
            ft.dropdown.Option("Em andamento"),
            ft.dropdown.Option("Pendente"),
        ],
        width=400,
    )

    async def carregar_atividade():
        page.views.clear()
        page.views.append(loading_view())
        page.update()

        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(f"{API_URL}/colaboradores/{cid}/atividades/{atvid}")
                if r.status_code == 200:
                    colab = r.json()
                    atividades.content = ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment='center_left',
                        controls=[
                            ft.Text(f"Atividade: {colab['descricao']}"),
                            ft.Text(
                                f"Comentario do Colaborador: "
                                f"{'adicione um comentario primeiro' if not colab['comentario_colaborador'] or colab['comentario_colaborador'] == 'string' else colab['comentario_colaborador']}"
                            ),
                            ft.Text(f"Status = {colab['status']}"),
                            ft.Text(f"Data = {colab['data'][:10]}"),
                        ]
                    )
                else:
                    status.value = "Atividade não encontrada."
        except Exception as e:
            status.value = f"Erro: {e}"
        
        page.views.clear()
        page.views.append(layout)
        page.update()
        
    async def salvar_edicao(e):
        ass_colab = "Assinado" if chk_colab.value else "Não Assinado"
        ass_gestor = "Assinado" if chk_gestor.value else "Não Assinado"
        try:
            # Busque os dados atuais da atividade para preencher os campos obrigatórios
            async with httpx.AsyncClient() as client:
                r_get = await client.get(f"{API_URL}/colaboradores/{cid}/atividades/{atvid}")
                if r_get.status_code == 200:
                    colab = r_get.json()
                    payload = {
                        "colaborador_id": cid,
                        "descricao": colab["descricao"],
                        "comentario_colaborador": comentario_field.value,
                        "status": status_atividade.value,
                        "assinatura_colab": ass_colab,
                        "assinatura_gestor": ass_gestor,
                        "data": colab["data"]
                    }
                    r = await client.put(
                        f"{API_URL}/colaboradores/{cid}/atividades/{atvid}",
                        json=payload,
                        headers={"Authorization": f"Bearer {get_token()}"}
                    )
                    if r.status_code == 200:
                        page.open(ft.SnackBar(
                            content=ft.Text(f"Atividade Atualizada com Sucesso", size=16, color='black', weight='bold', font_family='Arial', italic=True),
                            bgcolor="green",
                            duration=ft.Duration(seconds=2),
                        ))
                        comentario_field.value = ""
                        status_atividade.value = None
                        page.update()
                        await carregar_atividade()
                    else:
                        status.value = f"Erro ao atualizar: {r.text}"
                else:
                    status.value = "Não foi possível buscar os dados da atividade."
        except Exception as ex:
            status.value = f"Erro: {ex}"
        page.update()

    async def gerar_pdf(e):
        url = f"{API_URL}/colaboradores/{cid}/atividades/{atvid}/pdf"
        # Abre o PDF no navegador padrão (o usuário pode baixar)
        webbrowser.open(url)

    layout = ft.View(
        f"/colaborador/{cid}/atividades/{atvid}",
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.AppBar(
                leading=ft.IconButton(ft.Icons.HOME, icon_color=ft.Colors.SURFACE),
                leading_width=50,
                toolbar_height=70,
                title=ft.Text(f"Detalhes da Atividade {atvid} do Colaborador {nome_colaborador.value}", size=32, color=ft.Colors.SURFACE),
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
                content=ft.Column([
                    ft.TextButton("← Voltar à Página Anterior", on_click=lambda _: page.go(f"/colaborador/{cid}/atividades")),
                    ft.Divider(),
                    ft.Container(
                        expand=True,
                        alignment=ft.alignment.center,
                        content=ft.Text("Editar Atividade:", weight="bold", size=24, text_align='center'),
                    ),
                    ft.Container(
                        padding=ft.padding.only(top=5, bottom=15),
                        content=atividades,
                    ),
                    comentario_field,
                    ft.Row([
                        status_atividade,
                        chk_colab,
                        chk_gestor,
                    ]),
                    status,
                    ft.Row([
                        ft.ElevatedButton("Salvar", on_click=salvar_edicao, on_hover=hover, bgcolor=ft.Colors.ON_SURFACE, color=ft.Colors.SURFACE),
                        ft.ElevatedButton("Gerar PDF", on_click=gerar_pdf, on_hover=hover, bgcolor=ft.Colors.ON_SURFACE, color=ft.Colors.SURFACE)
                    ])
                ]),
            ),
        ]
    )

    page.run_task(carregar_atividade)
    page.run_task(handle_admin)

    return layout