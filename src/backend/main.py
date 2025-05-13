from backend.schemas import ColaIn, ColaOut, AtividadeCreate, AtividadeOut
from backend import models, database
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm
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
    return {**atividade.dict(), "id": atividade_id}

@app.get("/colaboradores", response_model=list[ColaOut], name="Listar Colaboradores", tags=["Colaboradores"])
def listar_colaboradores():
    """Lista todos os colaboradores cadastrados."""
    return models.listar_colaborador()

@app.get("/colaboradores/{id}", response_model=list[ColaOut], name="Listar Colaborador Individual", tags=["Colaboradores"])
def listar_colaboradores(id: int):
    """Lista todos os colaboradores cadastrados."""
    return models.listar_colaborador_individual(id)

@app.get("/colaboradores/{id}/atividades", response_model=list[AtividadeOut], name="Listar Atividades de um Colaborador Individual", tags=["Atividades"])
def listar_atividades(id: int):
    """Lista todas as atividades de um colaborador pelo ID."""
    atividades = models.listar_atividades_por_colaborador(id)
    if not atividades:
        raise HTTPException(status_code=404, detail="Nenhuma atividade encontrada para este colaborador")
    return atividades

@app.put("/colaboradores/{id}", response_model=ColaOut, name="Editar Dados dos Colaboradores", tags=["Colaboradores"])
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


@app.post("/register", tags=["Logins"])
def register(email: str, senha: str):
    conn = sqlite3.connect("on_the_job.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    total = cursor.fetchone()[0]
    conn.close()

    # Primeiro usuário será admin
    cargo = "admin" if total == 0 else "colaborador"
    models.create_user(email, senha, cargo)
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
    user = models.get_user(email)
    token = models.create_token(email, user[3])
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me", tags=["Logins"])
def get_me(authorization: str = Header(...)):
    token = authorization.split(" ")[1]
    dados = models.decode_token(token)

    return {
        "email": dados["sub"],
        "cargo": dados["cargo"]
    }
