import httpx, asyncio
import flet as ft
from functools import partial
from backend.api import API_URL
from backend.functions.temas import theme_change
from views.loadingpage.loading import loading_view
from backend.functions.formatting import hover
from backend.auth import get_me, get_token
from datetime import datetime

def view_detalhes(page: ft.Page, colab_id: int):
    page.scroll = ft.ScrollMode.AUTO

    nome = ft.Text()
    cargo = ft.Text()
    depart = ft.Text()
    gestor = ft.Text()

    atividades_column = ft.Row(
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        height=175,
        alignment=ft.MainAxisAlignment.START,
    )
    nova_atividade = ft.TextField(label="Nova atividade", multiline=True)

    status_atividade = ft.Dropdown(
        label="Status",
        options=[
            ft.dropdown.Option("Concluída"),
            ft.dropdown.Option("Em andamento"),
            ft.dropdown.Option("Pendente"),
        ],
        width=400,
    )
    status = ft.Text(color=ft.Colors.RED)

    user_name = ft.Text("Carregando...")

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
                r = await client.get(f"{API_URL}/colaboradores/{colab_id}", headers={"Authorization": f"Bearer {get_token()}"} )
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
        ft.PopupMenuItem(content=user_name),
        ft.PopupMenuItem(),
        ft.PopupMenuItem('Lista de Colaboradores', on_click=lambda _: page.go("/lista_cola")),
    ]
    
    async def popmenu():
        dados = await get_me()  # Tenta obter os dados do usuário autenticado

        if dados and dados['cargo'] == 'admin':
            popup_items.extend([
                ft.PopupMenuItem('Formulário', on_click=lambda _: page.go("/")),
                ft.PopupMenuItem('Admin', on_click=lambda _: page.go('/admin')),
            ])
        return popup_items
    
    async def excluir_atividade(e, aid):
        # Exibe a tela de loading enquanto exclui o colaborador
        page.views.clear()
        page.views.append(loading_view())
        page.update()

        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(f"{API_URL}/colaboradores/{colab_id}/atividades/{aid}")
                if response.status_code == 200:
                    page.go(f"/colaborador/{colab_id}")
                    return
                elif response.status_code == 404:
                    page.go(f"/colaborador/{colab_id}")
                    page.open(ft.SnackBar(
                        content=ft.Text("Atividade excluída com sucesso.", color="black"),
                        bgcolor="green",
                        duration=ft.Duration(seconds=2),
                    ))
                    return
                else:
                    page.open(ft.SnackBar(
                        content=ft.Text(f"Erro ao excluir: {response.status_code}", color="black"),
                        bgcolor="red",
                        duration=ft.Duration(seconds=2),
                    ))
        except Exception as e:
            page.open(ft.SnackBar(
                content=ft.Text(f"Erro ao excluir atividade: {e}", color="black"),
                bgcolor="red",
                duration=ft.Duration(seconds=2),
            ))
        finally:
            page.update()

    async def carregar_detalhes():
        # Exibe a tela de loading
        page.views.clear()
        page.views.append(loading_view())
        page.update()

        try:
            # Faz a requisição para obter os detalhes do colaborador
            async with httpx.AsyncClient() as client:
                r = await client.get(f"{API_URL}/colaboradores/{colab_id}")
                if r.status_code == 200:
                    colab = r.json()
                    nome.value = f"Nome: {colab[0]['colaborador']}"
                    cargo.value = f"Cargo: {colab[0]['cargo']}"
                    depart.value = f"Departamento: {colab[0]['departamento']}"
                    gestor.value = f"Gestor: {colab[0]['nome_gestor']}"
                    atividades_column.controls.clear()
                    for atv in colab[0]["atividades"]:
                        atividades_column.controls.append(
                            ft.Container(
                                content=ft.Column(
                                    scroll=ft.ScrollMode.AUTO,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment='center',
                                    controls=[
                                        ft.Text(f"Atividade: {atv['descricao']}"),
                                        ft.Text(f"Status = {atv['status']}"),
                                        ft.Text(f"Data = {atv['data'][:10]}"),
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            controls=[                                            
                                            ft.ElevatedButton(
                                                "Ver Detalhes", color=ft.Colors.SURFACE, bgcolor=ft.Colors.ON_SURFACE, on_hover=hover,
                                                on_click=lambda e, cid=colab[0]['id'], aid=atv['id']: page.go(f"/colaborador/{cid}/atividades/{aid}")
                                            ),
                                            ft.ElevatedButton(
                                                "Excluir", color=ft.Colors.SURFACE, bgcolor=ft.Colors.ON_SURFACE, on_hover=hover,
                                                on_click=lambda e, cid=colab[0]['id'], aid=atv['id']: page.run_task(partial(excluir_atividade, e, aid=aid))
                                            ),
                                        ])
                                    ]),
                                padding=ft.padding.only(top=7, left=10, right=10, bottom=7),
                                width=307,
                                height=140,
                                border=ft.border.all(1),
                                border_radius=10,
                                bgcolor=ft.Colors.TRANSPARENT,
                            )
                        )
                else:
                    nome.value = "Colaborador não encontrado."
        except Exception as e:
            nome.value = f"Erro: {e}"

        # Atualiza a página com os dados carregados
        page.views.clear()
        page.views.append(layout)
        page.update()

    async def adicionar_atividade(e):
        if not nova_atividade.value.strip():
            status.value = "Digite a descrição da atividade."
            page.update()
            return

        if not status_atividade.value:
            status.value = "Selecione um status para a atividade."
            page.update()
            return

        # Exibe a tela de loading enquanto adiciona a atividade
        page.views.clear()
        page.views.append(loading_view())
        page.update()

        try:
            payload = {
                "colaborador_id": colab_id,
                "descricao": nova_atividade.value.strip(),
                "comentario_colaborador": None,
                "status": status_atividade.value.strip(),
                "data": datetime.now().isoformat(),
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(f"{API_URL}/colaboradores/{colab_id}/atividades", json=payload)
                if response.status_code == 200:
                    nova_atividade.value = ""
                    status_atividade.value = ""
                    await carregar_detalhes()
                else:
                    status.value = f"Erro ao adicionar atividade: {response.status_code} - {response.text}"
        except Exception as e:
            status.value = f"Erro ao adicionar atividade: {e}"
        finally:
            page.update()

    async def excluir_colaborador(e):
        # Exibe a tela de loading enquanto exclui o colaborador
        page.views.clear()
        page.views.append(loading_view())
        page.update()

        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(f"{API_URL}/colaboradores/{colab_id}")
                if response.status_code == 200:
                    page.go("/lista_cola")
                    return
                elif response.status_code == 404:
                    page.go("/lista_cola")
                    page.open(ft.SnackBar(
                        content=ft.Text("Colaborador excluído com sucesso.", color="black"),
                        bgcolor="green",
                        duration=ft.Duration(seconds=2),
                    ))
                    return
                else:
                    page.open(ft.SnackBar(
                        content=ft.Text(f"Erro ao excluir: {response.status_code}", color="black"),
                        bgcolor="red",
                        duration=ft.Duration(seconds=2),
                    ))
        except Exception as e:
            page.open(ft.SnackBar(
                content=ft.Text(f"Erro ao excluir colaborador: {e}", color="black"),
                bgcolor="red",
                duration=ft.Duration(seconds=2),
            ))
        finally:
            page.update()

    # Layout principal da página
    layout = ft.View(
        f"/colaborador/{colab_id}/atividades",
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.AppBar(
                leading=ft.IconButton(ft.Icons.HOME, icon_color=ft.Colors.SURFACE),
                leading_width=50,
                toolbar_height=70,
                title=ft.Text(f"Detalhes do Colaborador {nome_colaborador.value}", size=32, color=ft.Colors.SURFACE),
                center_title=False,
                bgcolor=ft.Colors.ON_SURFACE,
                actions=[
                    ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED, icon_color=ft.Colors.SURFACE, on_click=theme_change),
                    ft.PopupMenuButton(
                        icon=ft.Icons.LIST,
                        icon_color=ft.Colors.SURFACE,
                        items=popup_items,
                    ),
                ]
            ),
            ft.Container(
                content=ft.Column([
                    ft.TextButton("← Voltar à Lista", on_click=lambda _: page.go("/lista_cola")),
                    nome, cargo, depart, gestor,
                    ft.Divider(),
                    ft.Text("Atividades:", weight="bold", size=24),
                ]),
            ),
            ft.Container(
                content=atividades_column,
            ),
            ft.Container(
                content=ft.Column([
                    nova_atividade,
                    status,
                ]),
                padding=ft.padding.only(top=5),
            ),
            ft.Container(
                padding=ft.padding.only(bottom=25),
                content=ft.Row([
                    status_atividade,
                    ft.ElevatedButton("Adicionar Atividade", on_click=adicionar_atividade, on_hover=hover, bgcolor=ft.Colors.ON_SURFACE, color=ft.Colors.SURFACE),
                    ft.Container(expand=True),
                    ft.ElevatedButton("Excluir Colaborador", on_click=excluir_colaborador, on_hover=hover, bgcolor=ft.Colors.ON_SURFACE, color=ft.Colors.SURFACE),
                ])
            )
        ]
    )

    # Executa a tarefa de carregar os detalhes ao iniciar a página
    page.run_task(carregar_detalhes)
    # page.run_task(atividades)
    page.run_task(popmenu)

    return layout