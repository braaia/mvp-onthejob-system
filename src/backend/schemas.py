from pydantic import BaseModel

class ColaIn(BaseModel):
    colaborador: str
    cpf: str
    data_adm: str
    cargo: str
    departamento: str
    nome_gestor: str
    cargo_gestor: str

class ColaOut(ColaIn):
    id: int