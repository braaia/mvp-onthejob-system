from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AtividadeCreate(BaseModel):
    colaborador_id: int
    descricao: str
    comentario_colaborador: Optional[str] = None
    status: str
    assinatura_colab: Optional[str] = None
    assinatura_gestor: Optional[str] = None
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
    email: str

class ColaOut(ColaIn):
    id: int
    atividades: List[AtividadeOut] = []