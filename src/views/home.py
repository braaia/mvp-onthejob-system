import flet as ft
import sqlite3, httpx, asyncio
from datetime import date
from reportlab.pdfgen import canvas # PDF generation library
from reportlab.lib.pagesizes import A4 # A4 page size for PDF
from backend.functions import formatting, temas
from backend.functions.formatting import hover
from backend.auth import get_me, get_token

API_URL = "http://localhost:8000"

def home_view(page: ft.Page):

    # FORM FIELDS - ALL CAN BE CUSTOMIZED (LABELS, SIZES, ETC.)
    campo_colab = ft.TextField(label="Nome do colaborador", border_color=ft.colors.ON_SURFACE, width=520, height=105)
    campo_matricula = ft.TextField(label="Matrícula ou CPF", border_color=ft.colors.ON_SURFACE, width=350, height=105, on_change=formatting.formatar_cpf)
    campo_admissao = ft.TextField(label="Data de admissão", border_color=ft.colors.ON_SURFACE, width=210, height=105, on_change=formatting.formatar_data)
    campo_cargo = ft.TextField(label="Cargo", width=550, border_color=ft.colors.ON_SURFACE, height=105)
    campo_departamento = ft.TextField(label="Departamento", border_color=ft.colors.ON_SURFACE, width=550, height=105)
    campo_gestor = ft.TextField(label="Nome do gestor", border_color=ft.colors.ON_SURFACE, width=550, height=105)
    campo_cargo_gestor = ft.TextField(label="Cargo do gestor", border_color=ft.colors.ON_SURFACE, width=550, height=105)

    # FORM SUBMISSION - MAIN LOGIC CAN BE MODIFIED
    async def enviar_formulario(e):
        # Get all field values
        colaborador = campo_colab.value
        cpf = campo_matricula.value
        admissao = campo_admissao.value
        cargo = campo_cargo.value
        depto = campo_departamento.value
        gestor = campo_gestor.value
        cargo_g = campo_cargo_gestor.value
        
        async with httpx.AsyncClient() as client:
            await client.post(f"{API_URL}/colaboradores", json={"colaborador": colaborador, "cpf": cpf, "data_adm": admissao, "cargo": cargo, "departamento": depto, "nome_gestor": gestor, "cargo_gestor": cargo_g})

        # Clear form - RESET LOGIC CAN BE CHANGED
        campo_colab.value = ""
        campo_matricula.value = ""
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
    botao_enviar = ft.ElevatedButton("Enviar formulário", on_click=enviar_formulario, on_hover=hover, width=170, height=40, color=ft.colors.SURFACE, bgcolor=ft.colors.ON_SURFACE)

    status = ft.Text()

    async def ver_cargo_click(e):
        if not get_token():
            status.value = "Você precisa estar logado."
            page.update()
            return

        async with httpx.AsyncClient() as client:
            r = await client.get(f"{API_URL}/me", headers={"Authorization": f"Bearer {get_token()}"})
        if r.status_code == 200:
            dados = await get_me()
            status.value = f"Você é '{dados['cargo']}' com email '{dados['email']}'"
        else:
            status.value = f"Erro: {r.json()['detail']}"
        page.update()


    # PAGE LAYOUT - CAN REORGANIZE COMPONENTS
    home_layout = ft.View(
        "/",
        vertical_alignment='center',
        horizontal_alignment='center',
        controls=[
            ft.AppBar(
                leading=ft.IconButton(ft.Icons.HOME, icon_color=ft.colors.SURFACE, on_click=lambda e: page.go("/")),
                leading_width=50,
                toolbar_height=70,
                title=ft.Text("Formulário ON THE JOB",size=32, color=ft.Colors.SURFACE),
                center_title=False,
                bgcolor=ft.Colors.ON_SURFACE,
                actions=[
                    ft.IconButton(ft.Icons.SETTINGS, icon_color=ft.colors.SURFACE, on_click=ver_cargo_click),
                    ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED, icon_color=ft.colors.SURFACE, on_click=temas.theme_change),
                    ft.PopupMenuButton(
                        icon=ft.Icons.LIST, 
                        icon_color=ft.colors.SURFACE,
                        items=[
                            ft.PopupMenuItem('USER', on_click=lambda _: print("User")),
                            ft.PopupMenuItem(),
                            ft.PopupMenuItem('Lista de Colaboradores', on_click=lambda _: page.go("/lista_cola"))
                        ]
                    ),
                ],
            ),
            ft.Text("Admissão Colaborador", size=22, weight="bold", offset=ft.Offset(x=0, y=-0.95)),
            ft.Row([campo_colab, campo_matricula, campo_admissao], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([campo_cargo, campo_departamento], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
            ft.Text("Gestor", size=22, weight="bold", offset=ft.Offset(x=0, y=-0.95)),
            ft.Row([campo_gestor, campo_cargo_gestor],spacing=20, alignment=ft.MainAxisAlignment.CENTER),
            status,
            ft.Container(
                content=botao_enviar,
            )
        ]
    )
    
    return home_layout