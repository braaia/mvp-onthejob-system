from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AtividadeCreate(BaseModel):
    colaborador_id: int
    descricao: str
    comentario_colaborador: Optional[str] = None
    comentario_gestor: Optional[str] = None
    status: str
    data: datetime

class AtividadeOut(AtividadeCreate):
    id: int

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
    atividades: List[AtividadeOut] = []