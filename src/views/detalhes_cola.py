import httpx
import flet as ft
from backend.functions.temas import theme_change
from views.loadingpage.loading import loading_view
from backend.functions.formatting import hover
from datetime import datetime

API_URL = "http://localhost:8000"

def view_detalhes(page: ft.Page, colab_id: int):
    page.scroll = ft.ScrollMode.AUTO

    nome = ft.Text()
    cargo = ft.Text()
    depart = ft.Text()
    gestor = ft.Text()
    atividades_column = ft.Column()
    nova_atividade = ft.TextField(label="Nova atividade")
    comentario_gestor = ft.TextField(label="Comentário")

    status_atividade = ft.Dropdown(
        label="Status",
        options=[
            ft.dropdown.Option("Concluída"),
            ft.dropdown.Option("Em andamento"),
            ft.dropdown.Option("Pendente"),
        ],
        width=400,
    )

    status = ft.Text(color=ft.colors.GREEN)

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
                        atividades_column.controls.append(ft.Text(f'- {atv['descricao']}, "Status = {atv['status']}" | ({atv['data'][:10]})'))
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
                "comentario_gestor": comentario_gestor.value.strip() if comentario_gestor.value else None,
                "status": status_atividade.value.strip(),
                "data": datetime.now().isoformat(),
            }

            print(payload)  # Para depuração

            async with httpx.AsyncClient() as client:
                response = await client.post(f"{API_URL}/colaboradores/{colab_id}/atividades", json=payload)
                if response.status_code == 200:
                    nova_atividade.value = ""
                    comentario_gestor.value = ""
                    status_atividade.value = ""
                    await carregar_detalhes()
                else:
                    status.value = f"Erro ao adicionar atividade: {response.status_code} - {response.text}"
        except Exception as e:
            status.value = f"Erro ao adicionar atividade: {e}"
        finally:
            page.update()

    # Layout principal da página
    layout = ft.View(
        f"/colaborador/{colab_id}/atividades",
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.AppBar(
                leading=ft.IconButton(ft.Icons.HOME, icon_color=ft.colors.SURFACE, on_click=lambda e: page.go("/")),
                leading_width=50,
                toolbar_height=70,
                title=ft.Text("Detalhes do Colaborador", size=32, color=ft.Colors.SURFACE),
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
                content=ft.Column([
                    ft.TextButton("← Voltar à Lista", on_click=lambda _: page.go("/lista_cola")),
                    nome, cargo, depart, gestor,
                    ft.Divider(),
                    ft.Text("Atividades:", weight="bold"),
                    atividades_column,
                    nova_atividade,
                    comentario_gestor,
                    status_atividade,
                    ft.ElevatedButton("Adicionar Atividade", on_click=adicionar_atividade, on_hover=hover),
                    ft.Divider(),
                    ft.ElevatedButton("Gerar PDF", on_click=lambda _: print("Gerar PDF"), on_hover=hover),
                ])
            )
        ]
    )

    # Executa a tarefa de carregar os detalhes ao iniciar a página
    page.run_task(carregar_detalhes)

    return layout