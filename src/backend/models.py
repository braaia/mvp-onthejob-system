import sqlite3
from src.backend.schemas import ColaOut, AtividadeCreate, AtividadeOut
from fastapi import HTTPException
from jose import jwt, JWTError
from passlib.hash import bcrypt
from datetime import datetime, timedelta

SECRET_KEY = "segredo-supersecreto"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_conn():
    return sqlite3.connect("on_the_job.db")

def criar_colaborador(nome: str, cpf: str, data_adm: str, cargo: str, depart: str, nome_gestor: str, cargo_gestor: str, email: str):
    """Insere um novo colaborador no banco de dados."""
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO admissao (
                colaborador, cpf, data_adm, cargo, departamento, nome_gestor, cargo_gestor, email)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (nome, cpf, data_adm, cargo, depart, nome_gestor, cargo_gestor, email),
        )
        conn.commit()
        cid = cursor.lastrowid
        return ColaOut(
            id=cid,
            colaborador=nome,
            cpf=cpf,
            data_adm=data_adm,
            cargo=cargo,
            departamento=depart,
            nome_gestor=nome_gestor,
            cargo_gestor=cargo_gestor,
            email=email,
            atividades=[]
        )
    finally:
        conn.close()

def listar_colaborador():
    """Retorna uma lista de todos os colaboradores cadastrados."""
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, colaborador, cpf, data_adm, cargo, departamento, nome_gestor, cargo_gestor, email FROM admissao")
        rows = cursor.fetchall()
        return [
            ColaOut(
                id=row[0],
                colaborador=row[1],
                cpf=row[2],
                data_adm=row[3],
                cargo=row[4],
                departamento=row[5],
                nome_gestor=row[6],
                cargo_gestor=row[7],
                email=row[8],
                atividades=listar_atividades_por_colaborador(row[0])
            )
            for row in rows
        ]
    finally:
        conn.close()

def listar_colaborador_individual(colab_id: int):
    """Retorna uma lista de todos os colaboradores cadastrados."""
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """SELECT id, colaborador, cpf, data_adm, cargo, departamento, nome_gestor, cargo_gestor, email
            FROM admissao 
            WHERE id = ?
            """,
            (colab_id,),
        )
        rows = cursor.fetchall()
        return [
            ColaOut(
                id=row[0],
                colaborador=row[1],
                cpf=row[2],
                data_adm=row[3],
                cargo=row[4],
                departamento=row[5],
                nome_gestor=row[6],
                cargo_gestor=row[7],
                email=row[8],
                atividades=listar_atividades_por_colaborador(row[0])
            )
            for row in rows
        ]
    finally:
        conn.close()

def listar_colaborador_por_email(email: str):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM admissao WHERE email = ?", (email,))
        row = cursor.fetchone()
        if row:
            colaborador = {
                "id": row[0],
                "colaborador": row[1],
                "cpf": row[2],
                "data_adm": row[3],
                "cargo": row[4],
                "departamento": row[5],
                "nome_gestor": row[6],
                "cargo_gestor": row[7],
                "email": row[8],
                "atividades": listar_atividades_por_colaborador(row[0])
            }
            return [colaborador]
        else:
            return []
    finally:
        conn.close()

def adicionar_atividade(atividade: AtividadeCreate):
    """Adiciona uma atividade ao banco de dados."""
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO atividades (colaborador_id, descricao, comentario_colaborador, status, assinatura_colab, assinatura_gestor, data)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (atividade.colaborador_id, atividade.descricao, atividade.comentario_colaborador, atividade.status, atividade.assinatura_colab, atividade.assinatura_gestor, atividade.data),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def listar_atividades_por_colaborador(colaborador_id: int):
    """Retorna todas as atividades associadas a um colaborador."""
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT id, colaborador_id, descricao, comentario_colaborador, status, assinatura_colab, assinatura_gestor, data
            FROM atividades
            WHERE colaborador_id = ?
            """,
            (colaborador_id,),
        )
        rows = cursor.fetchall()
        return [
            AtividadeOut(
                id=row[0],
                colaborador_id=row[1],
                descricao=row[2],
                comentario_colaborador=row[3],
                status=row[4],
                assinatura_colab=row[5],
                assinatura_gestor=row[6],
                data=row[7]
            )
            for row in rows
        ]
    finally:
        conn.close()

def atualizar_atividade(id: int, colaborador_id: int, descricao: str, comentario_colaborador: str, status: str, ass_col: str, ass_ges: str):
    """Atualiza os dados de um colaborador pelo ID."""
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE atividades
            SET descricao = ?, comentario_colaborador = ?, status = ?, assinatura_colab = ?, assinatura_gestor = ?
            WHERE id = ? AND colaborador_id = ?
            """,
            (descricao, comentario_colaborador, status, ass_col, ass_ges, id, colaborador_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def get_atividade_por_id(colaborador_id: int, atividade_id: int):
    """Retorna uma atividade específica de um colaborador."""
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT id, colaborador_id, descricao, comentario_colaborador, status, assinatura_colab, assinatura_gestor, data
            FROM atividades
            WHERE colaborador_id = ? AND id = ?
            """,
            (colaborador_id, atividade_id),
        )
        row = cursor.fetchone()
        if row:
            return AtividadeOut(
                id=row[0],
                colaborador_id=row[1],
                descricao=row[2],
                comentario_colaborador=row[3],
                status=row[4],
                assinatura_colab=row[5],
                assinatura_gestor=row[6],
                data=row[7]
            )
        return None
    finally:
        conn.close()

def atualizar_colaborador(id: int, nome: str, cpf: str, data_adm: str, cargo: str, depart: str, nome_gestor: str, cargo_gestor: str, email: str):
    """Atualiza os dados de um colaborador pelo ID."""
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE admissao
            SET colaborador = ?, cpf = ?, data_adm = ?, cargo = ?, departamento = ?, nome_gestor = ?, cargo_gestor = ?, email = ?
            WHERE id = ?
            """,
            (nome, cpf, data_adm, cargo, depart, nome_gestor, cargo_gestor, email, id),
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def get_user(email: str):
    conn = sqlite3.connect("on_the_job.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def create_user(user, email, senha, cargo):
    if get_user(email):
        raise HTTPException(status_code=400, detail="Usuário já existe.")
    conn = sqlite3.connect("on_the_job.db")
    cursor = conn.cursor()
    senha_hash = bcrypt.hash(senha)
    cursor.execute("INSERT INTO users (user, email, senha, cargo) VALUES (?, ?, ?, ?)",
                   (user, email, senha_hash, cargo))
    conn.commit()
    conn.close()

def authenticate_user(email, senha):
    user = get_user(email)
    if not user:
        return False
    return bcrypt.verify(senha, user[3])

def create_token(user, email, cargo):
    payload = {
        "user": user,
        "sub": email,
        "cargo": cargo,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    
def deletar_colaborador(id: int):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM admissao WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def deletar_atividade(cid: int, atvid: int):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM atividades WHERE id = ? AND colaborador_id = ?", (atvid, cid,))
    conn.commit()
    conn.close()