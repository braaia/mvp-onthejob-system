from pydantic import BaseModel

class ClienteIn(BaseModel):
    nome: str
    email: str

class ClienteOut(ClienteIn):
    id: int