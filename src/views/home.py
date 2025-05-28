import flet as ft
import httpx, asyncio
from src.backend.api import API_URL
from reportlab.pdfgen import canvas # PDF generation library
from reportlab.lib.pagesizes import A4 # A4 page size for PDF
from src.backend.functions import formatting, temas
from functools import partial
from src.backend.functions.logout import logout
from src.backend.functions.formatting import hover
from src.backend.auth import get_token

def home_view(page: ft.Page):

    field_height = 70

    campo_colab = ft.TextField(label="Nome do colaborador", border_color=ft.Colors.ON_SURFACE, width=500, height=field_height)
    campo_matricula = ft.TextField(label="Matrícula ou CPF", border_color=ft.Colors.ON_SURFACE, width=320, height=field_height, on_change=formatting.formatar_cpf)
    campo_email = ft.TextField(label="Email do Colaborador", border_color=ft.Colors.ON_SURFACE, width=500, height=field_height)
    campo_admissao = ft.TextField(label="Data de admissão", border_color=ft.Colors.ON_SURFACE, width=320, height=field_height, on_change=formatting.formatar_data)
    campo_cargo = ft.TextField(label="Cargo", border_color=ft.Colors.ON_SURFACE, width=410, height=field_height)
    campo_departamento = ft.TextField(label="Departamento", border_color=ft.Colors.ON_SURFACE, width=410, height=field_height)
    campo_gestor = ft.TextField(label="Nome do gestor", border_color=ft.Colors.ON_SURFACE, width=410, height=field_height)
    campo_cargo_gestor = ft.TextField(label="Cargo do gestor", border_color=ft.Colors.ON_SURFACE, width=410, height=field_height)

    async def enviar_formulario(e):
        colaborador = campo_colab.value
        cpf = campo_matricula.value
        email = campo_email.value
        admissao = campo_admissao.value
        cargo = campo_cargo.value
        depto = campo_departamento.value
        gestor = campo_gestor.value
        cargo_g = campo_cargo_gestor.value
        
        async with httpx.AsyncClient() as client:
            await client.post(f"{API_URL}/colaboradores", json={
                "colaborador": colaborador, 
                "cpf": cpf,
                "email": email,
                "data_adm": admissao, 
                "cargo": cargo, 
                "departamento": depto, 
                "nome_gestor": gestor, 
                "cargo_gestor": cargo_g
                }
            )

        # Clear form - RESET LOGIC CAN BE CHANGED
        campo_colab.value = ""
        campo_matricula.value = ""
        campo_email.value = ""
        campo_cargo.value = ""
        campo_departamento.value = ""
        campo_admissao.value = ""
        campo_gestor.value = ""
        campo_cargo_gestor.value = ""

        page.update()

        # Show success message - CAN MODIFY MESSAGE AND STYLING
        page.open(ft.SnackBar(
                content=ft.Text(value="Formulário Enviado", size=16, color='black', weight='bold', font_family='Arial', italic=True),
                bgcolor="green",
                duration=ft.Duration(seconds=2),
                show_close_icon=True,
                close_icon_color='black',
            ))
        page.update()

    # BUTTONS - CAN CHANGE LABELS AND STYLING
    # botao_adicionar_atividade = ft.ElevatedButton("Adicionar Atividade", on_click=adicionar_atividade)
    botao_enviar = ft.ElevatedButton("Enviar formulário", on_click=enviar_formulario, on_hover=hover, width=170, height=40, color=ft.Colors.SURFACE, bgcolor=ft.Colors.ON_SURFACE)

    status = ft.Text()

    async def ver_cargo_click(e):
        if not get_token():
            status.value = "Você precisa estar logado."
            page.update()
            return

        async with httpx.AsyncClient() as client:
            r = await client.get(f"{API_URL}/me", headers={"Authorization": f"Bearer {get_token()}"})
            if r.status_code == 200:
                dados = r.json()
                status.value = f"Você é '{dados['cargo']}' com email '{dados['email']}'"
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

    # PAGE LAYOUT - CAN REORGANIZE COMPONENTS
    home_layout = ft.View(
        "/",
        vertical_alignment='center',
        horizontal_alignment='center',
        controls=[
            ft.AppBar(
                leading=ft.IconButton(ft.Icons.HOME, icon_color=ft.Colors.SURFACE),
                leading_width=50,
                toolbar_height=70,
                title=ft.Text("Formulário ON THE JOB",size=32, color=ft.Colors.SURFACE),
                center_title=False,
                bgcolor=ft.Colors.ON_SURFACE,
                actions=[
                    ft.IconButton(ft.Icons.SETTINGS, icon_color=ft.Colors.SURFACE, on_click=ver_cargo_click),
                    ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED, icon_color=ft.Colors.SURFACE, on_click=temas.theme_change),
                    ft.PopupMenuButton(
                        icon=ft.Icons.LIST, 
                        icon_color=ft.Colors.SURFACE,
                        items=[
                            ft.PopupMenuItem(content=user_name, on_click=lambda _: print(user_name)),
                            ft.PopupMenuItem(),
                            ft.PopupMenuItem('Lista de Colaboradores', on_click=lambda _: page.go("/lista_cola")),
                            ft.PopupMenuItem('Admin', on_click=lambda _: page.go('/admin')),
                            ft.PopupMenuItem(),
                            ft.PopupMenuItem('Sair', on_click=lambda e: page.run_task(partial(logout, page, e)))
                        ]
                    ),
                ],
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Admissão Colaborador", size=22, weight="bold", text_align="center", offset=ft.Offset(x=0, y=-0.78)),
                    ft.Row([campo_colab, campo_matricula], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([campo_email, campo_admissao], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([campo_cargo, campo_departamento], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
                    ft.Text("Gestor", size=18, weight="bold", text_align="center", offset=ft.Offset(x=0, y=-0.56)),
                    ft.Row([campo_gestor, campo_cargo_gestor], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
                    status,
                    ft.Container(
                        content=botao_enviar,
                        alignment=ft.alignment.center,
                        margin=ft.margin.only(top=-18)
                    ),
                ],
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=30,
                border_radius=15,
                width=1280,
                margin=ft.margin.only(bottom=20)
            )
        ]
    )
    
    return home_layout