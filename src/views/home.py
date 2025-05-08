import flet as ft
import sqlite3
from datetime import date
from reportlab.pdfgen import canvas # PDF generation library
from reportlab.lib.pagesizes import A4 # A4 page size for PDF
from backend.formatting import formatar_cpf, formatar_data

# DATABASE CONNECTION - CAN CHANGE DATABASE NAME
conn = sqlite3.connect("on_the_job.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS formularios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        colaborador TEXT,
        matricula TEXT,
        cargo TEXT,
        departamento TEXT,
        admissao TEXT,
        gestor TEXT,
        cargo_gestor TEXT,
        data_envio TEXT
    )
""")
conn.commit()

def home_view(page: ft.Page):

    # FORM FIELDS - ALL CAN BE CUSTOMIZED (LABELS, SIZES, ETC.)
    campo_colab = ft.TextField(label="Nome do colaborador", border_color=ft.colors.ON_SURFACE, width=520, height=105)
    campo_matricula = ft.TextField(label="Matrícula ou CPF", border_color=ft.colors.ON_SURFACE, width=350, height=105, on_change=formatar_cpf)
    campo_admissao = ft.TextField(label="Data de admissão", border_color=ft.colors.ON_SURFACE, width=210, height=105, on_change=formatar_data)
    campo_cargo = ft.TextField(label="Cargo", width=550, border_color=ft.colors.ON_SURFACE, height=105)
    campo_departamento = ft.TextField(label="Departamento", border_color=ft.colors.ON_SURFACE, width=550, height=105)
    campo_gestor = ft.TextField(label="Nome do gestor", border_color=ft.colors.ON_SURFACE, width=550, height=105)
    campo_cargo_gestor = ft.TextField(label="Cargo do gestor", border_color=ft.colors.ON_SURFACE, width=550, height=105)

    # FORM SUBMISSION - MAIN LOGIC CAN BE MODIFIED
    def enviar_formulario(e):
        with sqlite3.connect("on_the_job.db") as conn:
            cursor = conn.cursor()

            # Get all field values
            colaborador = campo_colab.value
            matricula = campo_matricula.value
            cargo = campo_cargo.value
            depto = campo_departamento.value
            admissao = campo_admissao.value or ""
            gestor = campo_gestor.value
            cargo_g = campo_cargo_gestor.value

            # cons_g = cons_gestor.value
            # cons_c = cons_colab.value
            # status = status_final.value
            # ass_colab = 1 if chk_colab.value else 0
            # ass_gestor = 1 if chk_gestor.value else 0

            # Insert form data
            cursor.execute("""
                INSERT INTO formularios (
                    colaborador, matricula, cargo, departamento, admissao,
                    gestor, cargo_gestor, data_envio
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                colaborador, matricula, cargo, depto, admissao,
                gestor, cargo_g, date.today().isoformat()
            ))
            conn.commit()

        # Clear form - RESET LOGIC CAN BE CHANGED
        campo_colab.value = ""
        campo_matricula.value = ""
        campo_cargo.value = ""
        campo_departamento.value = ""
        campo_admissao.value = ""
        campo_gestor.value = ""
        campo_cargo_gestor.value = ""

        # cons_colab.value = ""
        # cons_gestor.value = ""
        # status_final.value = None
        # chk_colab.value = False
        # chk_gestor.value = False

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
    botao_enviar = ft.ElevatedButton("Enviar formulário", on_click=enviar_formulario, width=170, height=40, color=ft.colors.ON_SURFACE)

    # PAGE LAYOUT - CAN REORGANIZE COMPONENTS
    home_layout = ft.View(
        "/",
        vertical_alignment='center',
        horizontal_alignment='center',
        controls=[
            ft.AppBar(
                leading=ft.Icon(ft.Icons.HOME, color=ft.colors.SURFACE),
                leading_width=50,
                toolbar_height=70,
                title=ft.Text("Programa ON THE JOB",size=32, color=ft.Colors.SURFACE),
                center_title=False,
                bgcolor=ft.Colors.ON_SURFACE,
                actions=[
                    ft.IconButton(ft.Icons.LIST, icon_color=ft.colors.SURFACE),
                    ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED, icon_color=ft.colors.SURFACE),
                    ft.PopupMenuButton(
                        icon_color=ft.colors.SURFACE,
                        items=[
                            ft.PopupMenuItem(text="Item 1"),
                            ft.PopupMenuItem(),  # divider
                            ft.PopupMenuItem(
                                text="Checked item", checked=False,
                            ),
                        ]
                    ),
                ],
            ),
            ft.Text("Admissão Colaborador", size=22, weight="bold", offset=ft.Offset(x=0, y=-0.95)),
            ft.Row([campo_colab, campo_matricula, campo_admissao], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([campo_cargo, campo_departamento], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
            ft.Text("Gestor", size=22, weight="bold", offset=ft.Offset(x=0, y=-0.95)),
            ft.Row([campo_gestor, campo_cargo_gestor],spacing=20, alignment=ft.MainAxisAlignment.CENTER),

            ft.Container(
                content=botao_enviar,
            )
        ]
    )
    
    return home_layout