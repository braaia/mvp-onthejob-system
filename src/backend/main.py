from fastapi import FastAPI, HTTPException
from backend.schemas import ColaIn, ColaOut, AtividadeCreate, AtividadeOut
from backend import models, database

app = FastAPI()

@app.on_event("startup")
def startup():
    """Inicializa o banco de dados na inicialização do aplicativo."""
    database.init_db()

@app.post("/colaboradores", response_model=ColaOut)
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

@app.post("/colaboradores/{id}/atividades", response_model=AtividadeOut)
def adicionar_atividade(id: int, atividade: AtividadeCreate):
    """Adiciona uma atividade a um colaborador pelo ID."""
    atividade.colaborador_id = id
    atividade_id = models.adicionar_atividade(atividade)
    return {**atividade.dict(), "id": atividade_id}

@app.get("/colaboradores", response_model=list[ColaOut])
def listar_colaboradores():
    """Lista todos os colaboradores cadastrados."""
    return models.listar_colaborador()

@app.get("/colaboradores/{id}", response_model=list[ColaOut])
def listar_colaboradores(id: int):
    """Lista todos os colaboradores cadastrados."""
    return models.listar_colaborador_individual(id)

@app.get("/colaboradores/{id}/atividades", response_model=list[AtividadeOut])
def listar_atividades(id: int):
    """Lista todas as atividades de um colaborador pelo ID."""
    atividades = models.listar_atividades_por_colaborador(id)
    if not atividades:
        raise HTTPException(status_code=404, detail="Nenhuma atividade encontrada para este colaborador")
    return atividades

@app.put("/colaboradores/{id}", response_model=ColaOut)
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

@app.delete("/colaboradores/{id}")
def remover_colaborador(id: int):
    """Remove um colaborador pelo ID."""
    sucesso = models.deletar_colaborador(id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    return {"detail": "Colaborador removido com sucesso"}