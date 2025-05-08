from fastapi import FastAPI, HTTPException
from backend.schemas import ColaIn, ColaOut
from backend import models, database

app = FastAPI()

@app.on_event("startup")
def startup():
    database.init_db()


@app.post("/colaboradores", response_model=ColaOut)
def criar(colaborador: ColaIn):
    return models.criar_colaborador(colaborador.colaborador, colaborador.cpf, colaborador.data_adm, colaborador.cargo, colaborador.departamento, colaborador.nome_gestor, colaborador.cargo_gestor)


@app.get("/colaboradores", response_model=list[ColaOut])
def listar():
    return models.listar_colaborador()


@app.delete("/colaboradores/{id}")
def remover(id: int):
    models.deletar_cliente(id)
    return {"ok": True}


# @app.put("/colaboradores/{id}", response_model=ColaOut)
# def editar(id: int, colaborador: ClienteIn):
#     sucesso = models.atualizar_cliente(id, colaborador.nome, colaborador.email)
#     if not sucesso:
#         raise HTTPException(status_code=404, detail="Cliente não encontrado")
#     return ColaOut(id=id, nome=colaborador.nome, email=colaborador.email)