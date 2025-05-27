from src.backend.schemas import ColaIn, ColaOut, AtividadeCreate, AtividadeOut
from src.backend import models, database
from fastapi import FastAPI, HTTPException, Depends, Header, Body
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import StreamingResponse
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from typing import List
import sqlite3

app = FastAPI(
    title="API de Colaboradores",
    description="Gerenciamento de colaboradores, suas atividades e logins.",
    version="2.2.0",
    openapi_tags=[
        {"name": "Colaboradores", "description": "Operações com colaboradores"},
        {"name": "Atividades", "description": "Gerenciamento de atividades dos colaboradores"},
        {"name": "Logins", "description": "Gerenciamento de login dos colaboradores"},
    ]
)

@app.on_event("startup")
def startup():
    """Inicializa o banco de dados na inicialização do aplicativo."""
    database.init_db()

@app.post("/colaboradores", response_model=ColaOut, name="Criar Colaborador", tags=["Colaboradores"])
def criar_colaborador(colaborador: ColaIn):
    """Cria um novo colaborador."""
    return models.criar_colaborador(
        colaborador.colaborador,
        colaborador.cpf,
        colaborador.data_adm,
        colaborador.cargo,
        colaborador.departamento,
        colaborador.nome_gestor,
        colaborador.cargo_gestor,
    )

@app.post("/colaboradores/{id}/atividades", response_model=AtividadeOut, name="Adicionar Atividade a um Colaborador", tags=["Atividades"])
def adicionar_atividade(id: int, atividade: AtividadeCreate):
    """Adiciona uma atividade a um colaborador pelo ID."""
    atividade.colaborador_id = id
    atividade_id = models.adicionar_atividade(atividade)
    return models.get_atividade_por_id(id, atividade_id)

@app.put("/colaboradores/{cid}/atividades/{atvid}", response_model=AtividadeOut, name="Editar Dados da Atividade do Colaborador", tags=["Atividades"])
def atualizar_atividade(cid: int, atvid: int, atividade: AtividadeCreate):
    """Atualiza os dados da atividade de um colaborador pelo ID."""
    success = models.atualizar_atividade(
        atvid,
        cid,
        atividade.descricao,
        atividade.comentario_colaborador,
        atividade.status
    )
    if not success:
        raise HTTPException(status_code=404, detail="Atividade ou Colaborador não encontrado")
    return models.get_atividade_por_id(cid, atvid)

@app.get("/colaboradores", response_model=List[ColaOut], name="Listar Colaboradores", tags=["Colaboradores"])
def listar_colaboradores():
    """Lista todos os colaboradores cadastrados."""
    return models.listar_colaborador()

@app.get("/colaboradores/{id}", response_model=List[ColaOut], name="Listar Colaborador Individual", tags=["Colaboradores"])
def listar_colaboradores_ind(id: int):
    """Lista todos os colaboradores cadastrados."""
    return models.listar_colaborador_individual(id)

@app.get("/colaboradores/{id}/atividades", response_model=List[AtividadeOut], name="Listar Atividades de um Colaborador Individual", tags=["Atividades"])
def listar_atividades(id: int):
    """Lista todas as atividades de um colaborador pelo ID."""
    atividades = models.listar_atividades_por_colaborador(id)
    if not atividades:
        raise HTTPException(status_code=404, detail="Nenhuma atividade encontrada para este colaborador")
    return atividades

@app.get("/colaboradores/{cid}/atividades/{atvid}", response_model=AtividadeOut, name="Detalhar Atividade de um Colaborador", tags=["Atividades"])
def detalhar_atividade(cid: int, atvid: int):
    """Retorna os detalhes de uma atividade específica de um colaborador."""
    atividade = models.get_atividade_por_id(cid, atvid)
    if not atividade:
        raise HTTPException(status_code=404, detail="Atividade não encontrada para este colaborador")
    return atividade

@app.put("/colaboradores/{id}", response_model=List[ColaOut], name="Editar Dados dos Colaboradores", tags=["Colaboradores"])
def atualizar_colaborador(id: int, colaborador: ColaIn):
    """Atualiza os dados de um colaborador pelo ID."""
    sucesso = models.atualizar_colaborador(
        id,
        colaborador.colaborador,
        colaborador.cpf,
        colaborador.data_adm,
        colaborador.cargo,
        colaborador.departamento,
        colaborador.nome_gestor,
        colaborador.cargo_gestor,
    )
    if not sucesso:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    return ColaOut(
        id=id,
        colaborador=colaborador.colaborador,
        cpf=colaborador.cpf,
        data_adm=colaborador.data_adm,
        cargo=colaborador.cargo,
        departamento=colaborador.departamento,
        nome_gestor=colaborador.nome_gestor,
        cargo_gestor=colaborador.cargo_gestor,
    )

@app.delete("/colaboradores/{id}", name="Deletar Colaborador", tags=["Colaboradores"])
def remover_colaborador(id: int):
    """Remove um colaborador pelo ID."""
    sucesso = models.deletar_colaborador(id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    return {"detail": "Colaborador removido com sucesso"}

@app.delete("/colaboradores/{cid}/atividades/{atvid}", name="Deletar Atividade", tags=["Atividades"])
def remover_colaborador(cid: int, atvid: int):
    """Remove uma atividade pelo ID."""
    sucesso = models.deletar_atividade(cid, atvid)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    return {"detail": "Atividade removida com sucesso"}


@app.post("/register", tags=["Logins"])
def register(user: str, email: str, senha: str):
    conn = sqlite3.connect("on_the_job.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    total = cursor.fetchone()[0]
    conn.close()

    # Primeiro usuário será admin
    cargo = "admin" if total == 0 else "colaborador"
    models.create_user(user, email, senha, cargo)
    return {"msg": f"Usuário criado com sucesso! Cargo: {cargo}"}


@app.post("/set_cargo", tags=["Logins"])
def set_cargo(target_email: str, novo_cargo: str, authorization: str = Header(...)):
    token = authorization.split(" ")[1]
    dados = models.decode_token(token)

    if dados["cargo"] != "admin":
        raise HTTPException(status_code=403, detail="Somente administradores podem mudar cargos.")

    if novo_cargo not in ["admin", "colaborador"]:
        raise HTTPException(status_code=400, detail="Cargo inválido.")

    if not models.get_user(target_email):
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    conn = sqlite3.connect("on_the_job.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET cargo = ? WHERE email = ?", (novo_cargo, target_email))
    conn.commit()
    conn.close()

    return {"msg": f"Cargo de {target_email} alterado para {novo_cargo}."}

@app.post("/login", tags=["Logins"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username
    senha = form_data.password
    if not models.authenticate_user(email, senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")
    user_db = models.get_user(email)
    user_name = user_db[1]
    cargo = models.get_user(email)
    token = models.create_token(user_name, email, cargo[4])
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me", tags=["Logins"])
def get_me(authorization: str = Header(...)):
    token = authorization.split(" ")[1]
    dados = models.decode_token(token)

    return {
        "user": dados["user"],
        "email": dados["sub"],
        "cargo": dados["cargo"]
    }

@app.get("/colaboradores/{cid}/atividades/{atvid}/pdf", tags=["Atividades"])
def gerar_pdf_atividade(cid: int, atvid: int):
    # Busca o colaborador (retorna uma lista, pegue o primeiro)
    colaboradores = models.listar_colaborador_individual(cid)
    if not colaboradores or len(colaboradores) == 0:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    colaborador = colaboradores[0]

    atividade = models.get_atividade_por_id(cid, atvid)
    if not atividade:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(width / 2, height - 55, "Formulário On The Job")

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 110, "Colaborador:")

    p.setFont("Helvetica", 12)
    # Dados do colaborador
    p.drawString(70, height - 130, f"Nome: {colaborador.colaborador}")
    p.drawString(70, height - 150, f"Cargo: {colaborador.cargo}")
    p.drawString(70, height - 170, f"Departamento: {colaborador.departamento}")
    p.drawString(70, height - 190, f"Data de Admissão: {colaborador.data_adm}")
    p.drawString(70, height - 210, f"Gestor Responsável: {colaborador.nome_gestor}")

    # Dados da atividade
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 260, "Atividade:")

    p.setFont("Helvetica", 12)
    p.drawString(70, height - 280, f"Descrição: {atividade.descricao}")
    p.drawString(70, height - 300, f"Comentário do Colaborador: {atividade.comentario_colaborador or 'Nenhum'}")
    p.drawString(70, height - 320, f"Status: {atividade.status}")
    p.drawString(70, height - 340, f"Data da Atividade: {atividade.data.strftime('%Y-%m-%d')}")
    
    p.showPage()
    p.save()
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="application/pdf", headers={
        "Content-Disposition": f"attachment; filename=atividade_{atvid}_colab_{cid}.pdf"
    })

@app.post("/colaboradores/{cid}/atividades/pdf", tags=["Atividades"])
def gerar_pdf_multiplas_atividades(cid: int, atividade_ids: list[int] = Body(...)):
    colaboradores = models.listar_colaborador_individual(cid)
    if not colaboradores or len(colaboradores) == 0:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    colaborador = colaboradores[0]

    atividades = []
    for aid in atividade_ids:
        atv = models.get_atividade_por_id(cid, aid)
        if atv:
            atividades.append(atv)

    if not atividades:
        raise HTTPException(status_code=404, detail="Nenhuma atividade encontrada")

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(width / 2, height - 55, "Formulário On The Job - Multiplas Atividades")

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 110, "Colaborador:")

    p.setFont("Helvetica", 12)
    p.drawString(70, height - 130, f"Nome: {colaborador.colaborador}")
    p.drawString(70, height - 150, f"Cargo: {colaborador.cargo}")
    p.drawString(70, height - 170, f"Departamento: {colaborador.departamento}")
    p.drawString(70, height - 190, f"Data de Admissão: {colaborador.data_adm}")
    p.drawString(70, height - 210, f"Gestor Responsável: {colaborador.nome_gestor}")

    y = height - 260
    for idx, atv in enumerate(atividades, start=1):
        if y < 120:
            p.showPage()
            y = height - 50
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, f"Atividade {idx}:")
        y -= 20
        p.setFont("Helvetica", 12)
        p.drawString(70, y, f"Descrição: {atv.descricao}")
        y -= 20
        p.drawString(70, y, f"Comentário: {atv.comentario_colaborador or 'Nenhum'}")
        y -= 20
        p.drawString(70, y, f"Status: {atv.status}")
        y -= 20
        p.drawString(70, y, f"Data: {atv.data.strftime('%Y-%m-%d')}")
        y -= 40

    p.showPage()
    p.save()
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="application/pdf", headers={
        "Content-Disposition": f"attachment; filename=atividades_{cid}.pdf"
    })