from pydantic import BaseModel

class ClienteIn(BaseModel):
    nome: str
    cpf: str
    data: str
    cargo: str
    departamento: str
    nome_gestor: str
    cargo_gestor: str

class ClienteOut(ClienteIn):
    id: int